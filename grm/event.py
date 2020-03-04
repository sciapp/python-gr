from ctypes import c_int, c_char_p
from ctypes import POINTER, CFUNCTYPE
from ctypes import Union, Structure
from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm


class EventType(object):
    NEW_PLOT = 0
    UPDATE_PLOT = 1
    SIZE = 2
    MERGE_END = 3


class EVENT_NEW_PLOT(Structure):
    _fields_ = [("type", c_int), ("plot_id", c_int)]


class EVENT_UPDATE_PLOT(Structure):
    _fields_ = [("type", c_int), ("plot_id", c_int)]


class EVENT_SIZE(Structure):
    _fields_ = [("type", c_int), ("plot_id", c_int), ("width", c_int), ("height", c_int)]


class EVENT_MERGE_END(Structure):
    _field_ = [("type", c_int), ("identificator", c_char_p)]


class EVENT(Union):
    _fields_ = [
        ("new_plot_event", EVENT_NEW_PLOT),
        ("size_event", EVENT_SIZE),
        ("update_plot_event", EVENT_UPDATE_PLOT),
        ("merge_end_event", EVENT_MERGE_END),
    ]


_event_callback_t = CFUNCTYPE(None, POINTER(EVENT))
_registered_events = [None, None, None, None]  # One dict for each eventtype


@_require_runtime_version(0, 47, 0)
def register(event_type, callback):
    """
    Registers a callback for the specified event type
    """
    if not isinstance(event_type, int) or event_type < 0 or event_type > EventType.MERGE_END:
        raise TypeError("event_type must be a value out of EventType!")

    if callback == _registered_events[event_type]:
        raise ValueError("The specified callback is already registered")
    c_func = _event_callback_t(callback)
    _registered_events[event_type] = c_func
    return _grm.grm_register(c_int(event_type), c_func)


@_require_runtime_version(0, 47, 0)
def unregister(event_type):
    """
    Deregisters the callback for the given event type
    """
    if not isinstance(event_type, int) or event_type < 0 or event_type > EventType.MERGE_END:
        raise TypeError("event_type must be a value out of EventType!")

    _event_callback_t[event_type] = None
    return _grm.grm_unregister(c_int(event_type))


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_register.argtypes = [c_int, _event_callback_t]
    _grm.grm_register.restype = c_int

    _grm.grm_unregister.argtypes = [c_int]
    _grm.grm_unregister.restype = c_int

__all__ = ["register", "unregister", "EventType"]
