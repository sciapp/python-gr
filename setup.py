#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

import glob
import hashlib
import re
import sys
import os
import tarfile
import shutil
import platform

try:
    from io import BytesIO
    from urllib.request import urlopen, URLError
except ImportError:
    from StringIO import StringIO as BytesIO
    from urllib2 import urlopen, URLError

import vcversioner


sys.path.insert(0, os.path.abspath('gr'))
import runtime_helper
sys.path.pop(0)

_runtime_version = os.environ.get('GR_VERSION', 'stable')
if _runtime_version == 'stable':
    try:
        _runtime_version = runtime_helper.latest_runtime_version()
    except runtime_helper.GitHubAPIError:
        print(
            'Failed to fetch latest runtime version from GitHub API, falling back to the minimum required version',
            file=sys.stderr
        )
        _runtime_version = 'minimum'
if _runtime_version == 'minimum':
    _runtime_version = runtime_helper.required_runtime_version()
elif _runtime_version == 'master':
    # allow 'master' as alias for 'latest'
    _runtime_version = 'latest'


__author__ = "Florian Rhiem <f.rhiem@fz-juelich.de>, Christian Felder <c.felder@fz-juelich.de>"
__version__ = vcversioner.find_version(version_module_paths=[os.path.join("gr", "_version.py")]).version
__copyright__ = """Copyright (c) 2012-2017: Josef Heinen, Florian Rhiem,
Christian Felder and other contributors:

http://gr-framework.org/credits.html

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The GR framework can be built with plugins that use code from the
following projects, which have their own licenses:

- MuPDF - a lightweight PDF and XPS viewer (AFPL)
- Ghostscript - an interpreter for the PostScript language and for PDF (AFPL)
- FFmpeg - a multimedia framework (LGPL / GPLv2)

"""

_long_description = None
try:
    with open("README.rst", 'r') as fd:
        _long_description = fd.read()
except IOError as e:
    print("WARNING: long_description could not be read from file. Error message was:\n",
          e, file=sys.stderr)


def find_packages_py2_or_py3(*args, **kwargs):
    kwds = dict(kwargs)
    if sys.version_info[0] == 2:
        kwds.setdefault('exclude', []).extend(['grm'])
    return find_packages(*args, **kwds)

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None


class DownloadHashes(sdist):
    def run(self):
        """
        Download hashes for binary distributions during sdist creation

        This step prepares the actual downloading of the binary distribution
        during the build_py step by making sure the hashes of the individual
        tar files will be available.

        """
        DownloadBinaryDistribution.get_expected_hashes(_runtime_version)
        sdist.run(self)


class DownloadBinaryDistribution(build_py):
    SUPPORTED_LINUX_DISTRIBUTIONS = (
        'ArchLinux',
        'CentOS',
        'Debian',
        'Ubuntu',
    )

    @staticmethod
    def get_file_from_mirrors(file_name, version, schema):
        mirrors = [
            '{schema}://gr-framework.org/downloads/'.format(schema=schema)
        ]
        if version != 'latest':
            # GitHub only hosts release builds
            # GitHub should be preferred
            # GitHub enforces HTTPS
            mirrors.insert(0, 'https://github.com/sciapp/gr/releases/download/v{version}/'.format(version=version))
        urls = []
        for mirror in mirrors:
            urls.append(mirror + file_name)
        for url in urls:
            try:
                response = urlopen(url)
            except Exception:
                continue
            if response.getcode() == 200:
                return response.read()
        raise URLError('Failed to download file from: ' + ', '.join(urls))

    @staticmethod
    def detect_os():
        if sys.platform == 'darwin':
            return 'Darwin'
        if sys.platform == 'win32':
            return 'Windows'
        if sys.platform.startswith('linux'):
            release_file_names = glob.glob('/etc/*-release')
            release_file_names = [release_file_name for release_file_name in release_file_names if
                                  os.path.isfile(release_file_name) and os.access(release_file_name, os.R_OK)]
            release_info = '\n'.join([open(release_file_name).read() for release_file_name in release_file_names])
            if '/etc/os-release' in release_file_names:
                if 'ID=ubuntu' in release_info or 'ID=linuxmint' in release_info:
                    return 'Ubuntu'
                if 'ID=debian' in release_info or 'ID=raspbian' in release_info:
                    return 'Debian'
                if 'ID=arch' in release_info:
                    return 'ArchLinux'
                if 'ID="opensuse-tumbleweed"' in release_info:
                    return 'CentOS'
            if '/etc/redhat-release' in release_file_names:
                if 'release 7' in release_info:
                    return 'CentOS'
            return 'Linux'
        if sys.platform.startswith('freebsd'):
            if os.access('/etc/os-release', os.R_OK):
                with open('/etc/os-release', 'r') as f:
                    release_info = {key: value for key, value in (re.split(r"=[\"']?", line)[:2] for line in f)}
                if 'VERSION' in release_info:
                    major_version_str = release_info['VERSION'].split('.')[0]
                    if major_version_str.isdigit():
                        major_version = int(major_version_str)
                        if major_version >= 13:
                            return 'FreeBSD'
        return None

    @staticmethod
    def detect_architecture():
        if 'armv7' in platform.machine():
            return 'armhf'
        if 'aarch64' in platform.machine() or 'arm64' in platform.machine():
            return 'aarch64'
        is_64bits = sys.maxsize > 2**32
        if is_64bits:
            return 'x86_64'
        return 'i686'

    @staticmethod
    def get_expected_hashes(version):
        hash_file_name = 'gr-{version}.sha512.txt'.format(version=version)
        local_hash_file_name = os.path.join(os.path.dirname(__file__), hash_file_name)
        try:
            with open(local_hash_file_name, 'r') as hash_file:
                hash_file_content = hash_file.read()
        except IOError:
            hash_file_content = DownloadBinaryDistribution.get_file_from_mirrors(hash_file_name, version, 'https').decode('utf-8')
            # store hashes for later use
            with open(local_hash_file_name, 'w') as hash_file:
                hash_file.write(hash_file_content)
        expected_hashes = {}
        for line in hash_file_content.split('\n'):
            if ' *' in line:
                expected_hash, hashed_file_name = line.split(' *')
                expected_hashes[hashed_file_name] = expected_hash
        return expected_hashes

    @staticmethod
    def get_expected_hash(version, file_name):
        expected_hashes = DownloadBinaryDistribution.get_expected_hashes(version)
        if file_name not in expected_hashes:
            raise RuntimeError('No hash known for file: ' + file_name)
        return expected_hashes[file_name]

    def finalize_options(self):
            build_py.finalize_options(self)
            self.root_is_pure = False



    def run(self):
        """
        Downloads, unzips and installs GKS, GR and GR3 binaries.
        """
        build_py.run(self)
        base_path = os.path.realpath(self.build_lib)
        if os.environ.get('GR_FORCE_DOWNLOAD') or runtime_helper.load_runtime(silent=True) is None:
            version = _runtime_version
            operating_system = DownloadBinaryDistribution.detect_os()
            if operating_system is not None:
                arch = DownloadBinaryDistribution.detect_architecture()
                if arch == 'i686' and (
                    operating_system == 'Linux' or operating_system in self.SUPPORTED_LINUX_DISTRIBUTIONS
                ):
                    operating_system, arch = 'Linux', 'i386'

                # check for desired build variant (e.g. "mingw" or "msvc")
                variant = os.environ.get('GR_BUILD_VARIANT', '')
                if operating_system == 'Windows' and variant == '':
                    variant = 'msvc'
                suffix = ('-' + variant) if variant and variant != 'mingw' else ''

                # download binary distribution for system
                file_name = 'gr-{version}-{os}-{arch}{suffix}.tar.gz'.format(
                    version=version,
                    os=operating_system,
                    arch=arch,
                    suffix=suffix
                )

                tar_gz_data = DownloadBinaryDistribution.get_file_from_mirrors(file_name, version, 'http')
                # wrap response as file-like object
                tar_gz_data = BytesIO(tar_gz_data)
                expected_hash = DownloadBinaryDistribution.get_expected_hash(version, file_name)
                calculated_hash = hashlib.sha512(tar_gz_data.read()).hexdigest()
                tar_gz_data.seek(0)
                if calculated_hash != expected_hash:
                    raise RuntimeError("Downloaded binary distribution of GR runtime does not match expected hash")

                # extract shared libraries from downloaded .tar.gz archive
                tar_gz_file = tarfile.open(fileobj=tar_gz_data)
                try:
                    for member in tar_gz_file.getmembers():
                        tar_gz_file.extract(member, base_path)
                finally:
                    tar_gz_file.close()

        if sys.platform == 'win32':
            search_dir = os.path.join(base_path, 'gr', 'bin')
        else:
            search_dir = os.path.join(base_path, 'gr', 'lib')
        if runtime_helper.load_runtime(search_dirs=[search_dir], silent=False) is None:
            raise RuntimeError("Unable to install GR runtime")


setup(
    name="gr",
    version=__version__,
    description="Python visualization framework",
    author="Scientific IT Systems",
    author_email="j.heinen@fz-juelich.de",
    maintainer="Josef Heinen",
    license="MIT License",
    keywords="gr",
    url="http://gr-framework.org",
    platforms=["Linux", "OS X", "Windows"],
    install_requires=[
        'numpy >= 1.6',
    ],
    packages=find_packages_py2_or_py3(exclude=["tests", "tests.*"]),
    include_package_data=True,
    long_description=_long_description,
    classifiers=[
        'Framework :: IPython',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    cmdclass={
        'sdist': DownloadHashes,
        'build_py': DownloadBinaryDistribution,
        'bdist_wheel': bdist_wheel,
    }
)
