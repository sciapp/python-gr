"""
This module provides access to the various plotting-related functions.
"""

from ctypes import c_int, c_char_p, c_void_p, c_uint
from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm, _encode_str_to_char_p, args


@_require_runtime_version(0, 47, 0)
def plot(args_container):
    """
    Update the internal data container with the given data and draw the plot after it.

    :param args._ArgumentContainer args_container: The argument container with the data to plot
    :rtype: int
    """
    if args_container is None:
        return _grm.grm_plot(c_void_p(0x0))
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("Given parameter is not a valid ArgumentContainer!")
    return _grm.grm_plot(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def clear():
    """
    Clear all plots.

    :rtype: int
    """
    return _grm.grm_clear()


@_require_runtime_version(0, 47, 0)
def max_plotid():
    """
    Index of the highest active plot.

    :rtype: int
    """
    return _grm.grm_max_plotid()


@_require_runtime_version(0, 47, 0)
def merge(args_container):
    """
    Store the args_container into the internal, possibly clearing the internal values.

    :param args._ArgumentContainer args_container: The argument container with the data to merge
    :rtype: int
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer")
    return _grm.grm_merge(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def merge_extended(args_container, hold, identificator):
    """
    Merge the args_container into the internal, like merge_named, but hold specifies if the internal container should not be cleared.

    :param args._ArgumentContainer args_container: The argument container with the data to merge
    :param bool hold: When True, does not clear the internal data.
    :param str identificator: The identificator to pass to the MERGE_END event
    :rtype: int
    """
    if (
        not isinstance(args_container, args._ArgumentContainer)
        or not isinstance(hold, int)  # noqa W503
        or not isinstance(identificator, str)  # noqa W503
    ):
        raise TypeError("The given parameters do not match the types required.")

    return _grm.grm_merge_extended(args_container.ptr, c_int(1 if hold else 0), _encode_str_to_char_p(identificator))


@_require_runtime_version(0, 47, 0)
def merge_hold(args_container):
    # type: (args._ArgumentContainer) -> int
    """
    Merge the container while preserving the internally stored values.

    :param args._ArgumentContainer args_container: The argument container with the data to merge
    :rtype: int
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    return _grm.grm_merge_hold(args_container.ptr)


@_require_runtime_version(0, 47, 0)
def merge_named(args_container, identificator):
    """
    Merge the container, and the MERGE_END event is called with identificator set to the argument.

    :param args._ArgumentContainer args_container: The argument container with the data to merge
    :param str identificator: The identificator to pass to the MERGE_END event
    :rtype: int
    """
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    if not isinstance(identificator, str):
        raise TypeError("The given identificator is not a valid string.")

    return _grm.grm.merge_named(args_container.ptr, _encode_str_to_char_p(identificator))


@_require_runtime_version(0, 47, 0)
def switch(plot_id):
    """
    Switches the default plot id.

    :param int plot_id: The plot id to switch to
    :rtype: int
    """
    if not isinstance(plot_id, int):
        raise TypeError("Given parameter is not a valid integer!")
    if plot_id < 0:
        raise TypeError("Given parameter is not unsigned.")
    return _grm.grm_switch(c_uint(plot_id))


@_require_runtime_version(0, 47, 0)
def finalize():
    """
    Finalize the grm framework and frees resources.
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

__all__ = ["plot", "clear", "max_plotid", "merge", "merge_extended", "merge_hold", "merge_named", "switch", "finalize"]
