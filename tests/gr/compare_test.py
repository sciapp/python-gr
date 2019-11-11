import os
import shutil

from nose import with_setup

from gr_test import CompareResult, create_files
from gr_test.entry_points import get_file_pairs

base_path = os.path.abspath(os.path.dirname(os.path.realpath(__name__)) + '/../../test_result')

def setup_func():
    try:
        os.mkdir(base_path)
    except FileExistsError:
        pass

@with_setup(setup_func)
def test():
    create_files('TEST')
    for dir, ext, ref_name, test_name in get_file_pairs():
        yield compare, dir, ext, ref_name, test_name

def compare(dir, ext, ref_name, test_name):
    result = CompareResult(ref_name, test_name)

    if not result.is_equal():
        out_name = f'{base_path}/{dir}_{ext}_diff.png'
        result.make_diff_png(out_name)
        shutil.copy(test_name, f'{base_path}/{dir}.{ext}')

    assert result.is_equal()
