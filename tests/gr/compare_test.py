import os
import shutil
import platform

from nose import with_setup

from gr_test import CompareResult, test_data


base_path = os.path.abspath(os.path.dirname(os.path.realpath(__name__)) + '/../../test_result/')
results_path = os.path.abspath(base_path + '/' + platform.python_version())

def setup_func():
    try:
        os.mkdir(base_path)
    except FileExistsError:
        pass

    try:
        os.mkdir(results_path)
    except FileExistsError:
        pass

@with_setup(setup_func)
def test():
    test_data.create_files('TEST')
    for dir, ext, ref_name, test_name in test_data.get_file_pairs():
        yield compare, dir, ext, ref_name, test_name

def compare(dir, ext, ref_name, test_name):
    result = CompareResult(ref_name, test_name)

    if not result.is_equal():
        out_name = '%s/%s_%s_diff.png' % (results_path, dir, ext)
        result.make_diff_png(out_name)
        shutil.copy(test_name, '%s/%s.%s' % (results_path, dir, ext))
        print("diff png: %s" % out_name)

    assert result.is_equal()
