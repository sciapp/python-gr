from __future__ import print_function

import os
import shutil
import platform

import pytest

from gr_test import CompareResult
from gr_test import python_image as image_data
from gr_test import python_video as video_data
from gr_test.entry_points import safe_mkdir


@pytest.fixture(scope='session')
def base_dir():
    base_path = os.path.abspath(os.path.dirname(os.path.realpath(__name__)) + '/../../test_result/')

    if 'GR_TEST_BASE_PATH' in os.environ:
        base_path = os.path.abspath(os.environ['GR_TEST_BASE_PATH'])

    try:
        os.mkdir(base_path)
    except OSError:
        pass
    return base_path


@pytest.fixture(scope='session')
def results_dir(base_dir):
    results_path = os.path.abspath(base_dir + '/' + platform.python_version())

    try:
        os.mkdir(results_path)
    except OSError:
        pass
    return results_path


def test_images(results_dir):
    image_data.create_files('TEST')
    consistency, pairs = image_data.get_test_data()
    for x in consistency:
        assert x is None
    for dir, _, ref_name, test_name, base_name in pairs:
        compare(dir, ref_name, test_name, base_name, results_dir)


def test_video(results_dir):
    video_data.create_files('TEST')
    consistency, pairs = video_data.get_test_data()
    for x in consistency:
        assert x is None
    for dir, _, ref_name, test_name, base_name in pairs:
        compare(dir, ref_name, test_name, base_name, results_dir)


def compare(dir, ref_name, test_name, base_name, results_dir):
    this_path = os.path.join(results_dir, dir)
    # e.g. REFERENCE.pdf.png or frame-1.mov.png
    file_name = os.path.basename(test_name)

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
