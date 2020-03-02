import numpy as np
from numpy import array, ndarray, float64, int32, empty, prod
from ctypes import c_int, c_double, c_char_p, c_void_p, c_uint8, c_uint
from ctypes import byref, POINTER, addressof, CDLL, CFUNCTYPE
from ctypes import create_string_buffer, cast
from gr import _require_runtime_version, _RUNTIME_VERSION, char

from . import _grm, args

_c_int_p = POINTER(c_int)

@_require_runtime_version(0, 47, 0)
def input(args_container):
    """
    ???
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("args_container must be an ArgumentContainer!")

    return _grm.grm_input(args_container.ptr)

@_require_runtime_version(0, 47, 0)
def get_box(x1, y1, x2, y2, keep_aspect_ratio):
    """
    ???
    """
    if not isinstance(x1, int) or not isinstance(y1, int) or not isinstance(x2, int) or not isinstance(y2, int):
        raise TypeError("x1, x2, y1 and y2 is not an int")

    if not isinstance(keep_aspect_ratio, bool):
        raise TypeError("keep_aspect_ratio must be a bool")

    x = c_int()
    y = c_int()
    w = c_int()
    h = c_int()

    retval = _grm.grm_get_box(c_int(x1), c_int(y1), c_int(x2), c_int(y2), c_int(1 if keep_aspect_ratio else 0),
                              byref(x), byref(y), byref(w), byref(h))
    if retval == 0:
        raise ValueError("Was not able to execute grm_get_box!")

    return (x.value, y.value, w.value, h.value)

if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_input.argtypes = [c_void_p]
    _grm.grm_input.restype = c_int

    _grm.grm_get_box.argtypes = [c_int, c_int, c_int, c_int, c_int, _c_int_p, _c_int_p, _c_int_p, _c_int_p]
    _grm.grm_get_box.restype = c_int

__all__ = ['input', 'get_box']
