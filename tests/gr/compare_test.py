from __future__ import print_function

import os
import shutil
import platform

from nose import with_setup

from gr_test import CompareResult
from gr_test import python_image as image_data
from gr_test import python_video as video_data
from gr_test.entry_points import safe_mkdir
base_path = os.path.abspath(os.path.dirname(os.path.realpath(__name__)) + '/../../test_result/')

if 'GR_TEST_BASE_PATH' in os.environ:
    base_path = os.path.abspath(os.environ['GR_TEST_BASE_PATH'])

results_path = os.path.abspath(base_path + '/' + platform.python_version())

def setup_func():
    try:
        os.mkdir(base_path)
    except OSError:
        pass

    try:
        os.mkdir(results_path)
    except OSError:
        pass

@with_setup(setup_func)
def test_images():
    image_data.create_files('TEST')
    consistency, pairs = image_data.get_test_data()
    for x in consistency:
        yield succeed_if_none, x
    for dir, ext, ref_name, test_name, base_name in pairs:
        yield compare, dir, ext, ref_name, test_name, base_name

@with_setup(setup_func)
def test_video():
    video_data.create_files('TEST')
    consistency, pairs = video_data.get_test_data()
    for x in consistency:
        yield succeed_if_none, x
    for dir, ext, ref_name, test_name, base_name in pairs:
        yield compare, dir, ext, ref_name, test_name, base_name

def succeed_if_none(x):
    assert x is None

def compare(dir, ext, ref_name, test_name, base_name):
    this_path = os.path.join(results_path, dir)
    file_name = os.path.basename(test_name) # f.e. REFERENCE.pdf.png or frame-1.mov.png

    result = CompareResult(ref_name, test_name)

    if not result.is_equal():
        safe_mkdir(this_path)

        out_name = '%s/%s_diff.png' % (this_path, file_name)
        result.make_diff_png(out_name)

        # Copy generated files to output directory
        shutil.copy(test_name, '%s/%s' % (this_path, file_name))
        if base_name is not None:
            shutil.copy(base_name, '%s/%s' % (this_path, os.path.basename(base_name)))
        print("diff png: %s" % out_name)

    assert result.is_equal()
