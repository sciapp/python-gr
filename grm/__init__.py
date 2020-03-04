"""
This is a procedural interface to the GRM plotting part of the GR framework,
which may be imported directly, e.g.:

import grm
"""

from ctypes import c_int, c_char_p, c_void_p, c_uint
from ctypes import create_string_buffer, cast
from gr.runtime_helper import load_runtime
from gr import _require_runtime_version, _RUNTIME_VERSION

_grm = load_runtime(lib_name="libGRM")
if _grm is None:
    raise ImportError("Failed to load GRM runtime!")

def _encode_str_to_char_p(string):
    return cast(create_string_buffer(string.encode("utf-8")), c_char_p)

@_require_runtime_version(0, 47, 0)
def plot(args_container):
    """
    Plots the given args_container
    """
    if args_container is None:
        return _grm.grm_plot(c_void_p(0x0))
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("Given parameter is not a valid ArgumentContainer!")
    return _grm.grm_plot(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def clear():
    """
    Clears all plots
    """
    return _grm.grm_clear()


@_require_runtime_version(0, 47, 0)
def max_plotid():
    """
    Returns the index of the highest active plot
    """
    return _grm.grm_max_plotid()


@_require_runtime_version(0, 47, 0)
def merge(args_container):
    """
    Same as plot() but without drawing
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer")
    return _grm.grm_merge(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def merge_extended(args_container, hold, identificator):
    """
    ???
    """
    if (
            not isinstance(args_container, args._ArgumentContainer)
            or not isinstance(hold, int)
            or not isinstance(identificator, str)
    ):
        raise TypeError("The given parameters do not match the types required.")

    return _grm.grm_merge_extended(args_container.ptr, c_int(hold), _encode_str_to_char_p(identificator))


@_require_runtime_version(0, 47, 0)
def merge_hold(args_container):
    """
    ???
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    return _grm.grm_merge_hold(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def merge_named(args_container, identificator):
    """
    ???
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    if not isinstance(identificator, str):
        raise TypeError("The given identificator is not a valid string.")

    return _grm.grm.merge_named(args_container.ptr, _encode_str_to_char_p(identificator))


@_require_runtime_version(0, 47, 0)
def switch(plot_id):
    """
    Switches the default plot id
    """
    if not isinstance(plot_id, int):
        raise TypeError("Given parameter is not a valid integer!")
    if plot_id < 0:
        raise TypeError("Given parameter is not unsigned.")
    return _grm.grm_switch(c_uint(plot_id))


@_require_runtime_version(0, 47, 0)
def finalize():
    """
    Finalizes the grm framework and frees resources
    """
    _grm.grm_finalize()


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_plot.argtypes = [c_void_p]
    _grm.grm_plot.restype = c_int

    _grm.grm_clear.argtypes = []
    _grm.grm_clear.restype = c_int

    _grm.grm_max_plotid.argtypes = []
    _grm.grm_max_plotid.restype = c_uint

    _grm.grm_merge.argtypes = [c_void_p]
    _grm.grm_merge.restype = c_int

    _grm.grm_merge_extended.argtypes = [c_void_p, c_int, c_char_p]
    _grm.grm_merge_extended.restype = c_int

    _grm.grm_merge_hold.argtypes = [c_void_p]
    _grm.grm_merge_hold.restype = c_int

    _grm.grm_merge_named.argtypes = [c_void_p, c_char_p]
    _grm.grm_merge_named.restype = c_int

    _grm.grm_switch.argtypes = [c_uint]
    _grm.grm_switch.restype = c_int

    _grm.grm_finalize.argtypes = []
    _grm.grm_finalize.restype = None

from . import args
from . import event
from . import interaction

__all__ = [
    "args",
    "event",
    "interaction",
    "plot",
    "clear",
    "max_plotid",
    "merge",
    "merge_extended",
    "merge_hold",
    "merge_named",
    "switch",
    "finalize",
]
