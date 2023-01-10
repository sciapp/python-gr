from __future__ import print_function

import os
import shutil
import platform
import sys

import numpy as np
import pytest

if sys.version_info.major < 3:
    pytest.skip(allow_module_level=True)

from gr_test import CompareResult
from gr_test import PythonTestCase, WSType
from gr_test.entry_points import safe_mkdirs


@pytest.fixture(scope="session")
def base_dir():
    base_path = os.path.abspath(os.path.dirname(os.path.realpath(__name__)) + "/../../test_result/")

    if "GR_TEST_BASE_PATH" in os.environ:
        base_path = os.path.abspath(os.environ["GR_TEST_BASE_PATH"])

    try:
        os.mkdir(base_path)
    except OSError:
        pass
    return base_path


@pytest.fixture(scope="session")
def results_dir(base_dir):
    results_path = os.path.abspath(base_dir + "/" + platform.python_version())

    try:
        os.mkdir(results_path)
    except OSError:
        pass
    return results_path


test_cases = [
    (test_case, wstype)
    for x in PythonTestCase.gather_test_cases().values()
    for test_case in x
    for wstype in test_case.plugin.get_ws_types()
]


def idfn(x):
    return x.dst_ext if isinstance(x, WSType) else x.name


@pytest.mark.parametrize("test_case, wstype", test_cases, ids=idfn)
def test_python_test_case(test_case, wstype, results_dir):
    test_case.generate("TEST", wstype)

    p = test_case.get_pairs("REFERENCE", "TEST", wstype)

    errors = []

    for x, y in p:
        err = compare(test_case, wstype, x, y, results_dir)
        if err:
            errors.append(err)

    if errors:
        pytest.fail("Comparing failed: " + ", ".join(errors), pytrace=False)


def compare(test_case, wstype, ref, test, results_dir):
    base_name = test_case.get_base_name(wstype, test)

    try:
        result = CompareResult(ref, test)

        if result.is_equal():
            return None
    except FileNotFoundError as ex:
        this_out_dir = os.path.join(results_dir, test_case.name, wstype.dst_ext)
        safe_mkdirs(this_out_dir)

        # Conversion might have failed, copy base file
        if base_name is not None:
            shutil.copy(base_name, os.path.join(this_out_dir, os.path.basename(base_name)))

        return "%s/%s/%s (missing)" % (test_case.name, wstype.dst_ext, file_name)

    this_out_dir = os.path.join(results_dir, test_case.name, wstype.dst_ext)
    safe_mkdirs(this_out_dir)

    # diff was found, make diff and copy base & generated test file

    file_name = os.path.basename(test)
    diff_path = os.path.join(this_out_dir, "%s_diff.png" % file_name)
    result.make_diff_png(diff_path)
    print(
        "FAIL! Not equal: %s %s View diffs in: %s" %
        (os.path.relpath(ref, results_dir), os.path.relpath(test, results_dir), os.path.relpath(diff_path, results_dir))
    )

    # copy base
    if base_name is not None:
        shutil.copy(base_name, os.path.join(this_out_dir, os.path.basename(base_name)))

    # copy test file
    shutil.copy(test, os.path.join(this_out_dir, file_name))

    stats = result.diff_stats()
    with np.printoptions(precision=3, suppress=True):
        print(" max  %s" % stats[0])
        print(" mean %s" % stats[1])
        print(" std  %s" % stats[2])
        print(" sum  %s" % stats[3])

    return "%s/%s/%s" % (test_case.name, wstype.dst_ext, file_name)
