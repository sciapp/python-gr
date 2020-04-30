"""
This module provides functions to combine gui and graphs.
"""

from ctypes import c_int, c_void_p
from ctypes import byref, POINTER

from typing import Tuple

from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm, args

_c_int_p = POINTER(c_int)


@_require_runtime_version(0, 47, 0)
def input(args_container: args._ArgumentContainer) -> int:
    """
    Perform specific actions based on user interaction with the gui.

    All coordinates are integers and workstation coordinates
    It supports the following operation modes with the arguments needed:
        reset_ranges:
         * ``x`` mouse cursor x
         * ``y`` mouse cursor y
         * ``key`` the pressed key, f.e. 'r' for the right button
        zoom:
         * ``x`` start point x
         * ``y`` start point y
         * one of:
            - ``angle_delta``: mouse wheel rotation angle in eights of a degree
            - ``factor``: zoom factor
        box zoom (Zooms the subplot to the selection made):
         * ``x1``: fixed corner x
         * ``y1``: fixed corner y
         * ``x2``: other corner x
         * ``y2``: other corner y
         * ``keep_aspect_ratio``: if 1, the aspect ratio of the window is preserved
        pan:
         * ``x``: start point x
         * ``y``: start point y
         * ``xshift``: shift in x direction
         * ``yshift``: shift in y direction

    :param args_container: The container with one of the data sets described above set.

    :raises TypeError: if args_container is not a valid :class:`grm.args._ArgumentContainer`
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("args_container must be an ArgumentContainer!")

    return _grm.grm_input(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def get_box(x1: int, y1: int, x2: int, y2: int, keep_aspect_ratio: bool) -> Tuple[int, int, int, int]:
    """
    Translate a x1, y1, x2, y2 in workstation coordinates into a box.

    :raises TypeError: if the arguments have invalid types.
    :raises ValueError: if the c call failed.
    """
    if not isinstance(x1, int) or not isinstance(y1, int) or not isinstance(x2, int) or not isinstance(y2, int):
        raise TypeError("x1, x2, y1 and y2 is not an int")

    if not isinstance(keep_aspect_ratio, bool):
        raise TypeError("keep_aspect_ratio must be a bool")

    x = c_int()
    y = c_int()
    w = c_int()
    h = c_int()

    retval = _grm.grm_get_box(
        c_int(x1),
        c_int(y1),
        c_int(x2),
        c_int(y2),
        c_int(1 if keep_aspect_ratio else 0),
        byref(x),
        byref(y),
        byref(w),
        byref(h),
    )
    if retval == 0:
        raise ValueError("Was not able to execute grm_get_box!")

    return (x.value, y.value, w.value, h.value)


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_input.argtypes = [c_void_p]
    _grm.grm_input.restype = c_int

    _grm.grm_get_box.argtypes = [c_int, c_int, c_int, c_int, c_int, _c_int_p, _c_int_p, _c_int_p, _c_int_p]
    _grm.grm_get_box.restype = c_int

__all__ = ["input", "get_box"]
