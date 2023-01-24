# coding: utf-8
"""

"""

import ctypes
import os
import sys


def required_runtime_version():
    # TODO: load runtime version from file
    return '0.71.5'


def version_string_to_tuple(version_string):
    if not isinstance(version_string, str):
        version_string = version_string.decode('utf-8')
    if version_string.startswith('v'):
        version_string = version_string[1:]
    if '-' in version_string:
        version_string = version_string.split('-', 1)[0]
    version_string = version_string.replace('.post', '.')
    return tuple(int(v) for v in version_string.split('.'))


def load_runtime(search_dirs=(), silent=False, lib_name='libGR'):
    if sys.platform == "win32":
        library_extensions = (".dll",)
        library_directory = "bin"
    elif sys.platform == "darwin":
        library_extensions = (".dylib", ".so")
        library_directory = "lib"
    else:
        library_extensions = (".so",)
        library_directory = "lib"

    search_directories = list(search_dirs)
    search_directories.extend([
        os.environ.get('GRLIB'),
        os.path.realpath(os.path.join(os.path.dirname(__file__), library_directory)),
        os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'build', 'lib', 'gr')),
    ])
    if sys.platform != "win32":
        search_directories.extend(
            [
                os.path.join(os.path.expanduser('~'), 'gr', 'lib'),
                '/usr/local/gr/lib',
                '/usr/gr/lib',
            ]
        )

    search_path = os.environ.get('PATH', '')
    for directory in search_directories:
        if directory is None:
            continue
        if not os.path.isdir(directory):
            continue
        directory = os.path.abspath(directory)
        for library_extension in library_extensions:
            library_filename = os.path.join(directory, lib_name + library_extension)
            if os.path.isfile(library_filename):
                if sys.platform == "win32":
                    os.environ["PATH"] = search_path + ";" + directory
                try:
                    library = ctypes.CDLL(library_filename)
                except OSError:
                    # library exists but could not be loaded (e.g. due to missing dependencies)
                    if silent:
                        return None
                    else:
                        raise
                if lib_name == 'libGR':
                    library.gr_version.argtypes = []
                    library.gr_version.restype = ctypes.c_char_p
                    library_version_string = library.gr_version()
                    library_version = version_string_to_tuple(library_version_string)
                    required_version = version_string_to_tuple(required_runtime_version())
                    version_compatible = library_version[0] == required_version[0] and library_version >= required_version
                    if version_compatible:
                        return library
                # TODO: other libraries, such as libGRM, require some form of
                # validation as well, but currently no mechanism for this has
                # been implemented
                return library
    if not silent:
        sys.stderr.write("""GR runtime not found.
Please visit https://gr-framework.org and install at least the following version of the GR runtime:
{}

Also, please ensure that you have all required dependencies:
Debian/Ubuntu: apt install libxt6 libxrender1 libgl1-mesa-glx libqt5widgets5
CentOS 7: yum install libXt libXrender libXext mesa-libGL qt5-qtbase-gui
Fedora 28: dnf install -y libXt libXrender libXext mesa-libGL qt5-qtbase-gui
openSUSE 42.3 / 15: zypper install -y libXt6 libXrender1 libXext6 Mesa-libGL1 libQt5Widgets5
FreeBSD: pkg install libXt libXrender libXext mesa-libs qt5
""".format(required_runtime_version()))
    return None


def register_gksterm():
    if sys.platform == 'darwin':
        # register GKSTerm.app on macOS
        for app in [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GKSTerm.app')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'Applications', 'GKSTerm.app'))
        ]:
            if os.path.isdir(app):
                os.system('/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f {}'.format(app))
                return
