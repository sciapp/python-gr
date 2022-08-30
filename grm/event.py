"""
This module provides functions to manage callbacks for the events which can happen in grm.
"""
from ctypes import c_int, c_char_p
from ctypes import POINTER, CFUNCTYPE
from ctypes import Union, Structure
from enum import Enum
from typing import Callable, Union as UnionT

from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm


class EventType(Enum):
    """
    This class contains the event types which are passed to register/unregister.
    """

    NEW_PLOT = 0
    UPDATE_PLOT = 1
    SIZE = 2
    MERGE_END = 3


class EVENT_NEW_PLOT(Structure):
    """
    This class is used to carry event data for the new plot event.

    Instances of this class have the following members:

    * ``type`` (type: c_int): The event type (should be EventType.NEW_PLOT)
    * ``plot_id`` (type: c_int): The plot id which has a new size
    """

    _fields_ = [("type", c_int), ("plot_id", c_int)]


class EVENT_UPDATE_PLOT(Structure):
    """
    This class is used to carry event data for the update plot event.

    Instances of this class have the following members:

    * ``type`` (type: c_int): The event type (should be EventType.UPDATE_PLOT)
    * ``plot_id`` (type: c_int): The plot id which has a new size
    """

    _fields_ = [("type", c_int), ("plot_id", c_int)]


class EVENT_SIZE(Structure):
    """
    This class is used to carry event data for the size event.

    Instances of this class have the following members:

    * ``type`` (type: c_int): The event type (should be EventType.SIZE)
    * ``plot_id`` (type: c_int): The plot id which has a new size
    * ``width`` (type: c_int): The new width
    * ``height`` (type: c_int): The new height
    """

    _fields_ = [("type", c_int), ("plot_id", c_int), ("width", c_int), ("height", c_int)]


class EVENT_MERGE_END(Structure):
    """
    This class is used to carry event data for the merge end event.

    Instances of this class have the following members:

    * ``type`` (type: c_int): The event type (should be EventType.MERGE_END)
    * ``identificator`` (type: c_char_p): The optional identificator which was given using merge_named or merge_extended
    """

    _field_ = [("type", c_int), ("identificator", c_char_p)]


class EVENT(Union):
    _fields_ = [
        ("new_plot_event", EVENT_NEW_PLOT),
        ("size_event", EVENT_SIZE),
        ("update_plot_event", EVENT_UPDATE_PLOT),
        ("merge_end_event", EVENT_MERGE_END),
    ]


_event_callback_t = CFUNCTYPE(None, POINTER(EVENT))
_registered_events = {}  # type: Dict[EventType, Callable[[EVENT], None]]


@_require_runtime_version(0, 47, 0)
def register(
    event_type: EventType,
    callback: UnionT[
        Callable[[EVENT_NEW_PLOT], None],
        Callable[[EVENT_SIZE], None],
        Callable[[EVENT_UPDATE_PLOT], None],
        Callable[[EVENT_MERGE_END], None],
    ],
) -> int:
    """
    Register a callback for the specified event type.

    This eventually replaces an already set callback.
    Internally stores a reference to the callback.
    The callback receives a class specific to the event type, one of:
     * :py:class:`~grm.event.EVENT_NEW_PLOT`
     * :py:class:`~grm.event.EVENT_UPDATE_PLOT`
     * :py:class:`~grm.event.EVENT_SIZE`
     * :py:class:`~grm.event.EVENT_MERGE_END`

    :param event_type: The EventType to register a callback for.
    :param callback: The callback to be called if the event occurs.

    :raises TypeError: if event_type is not an EventType.
    """
    if not isinstance(event_type, EventType):
        raise TypeError("event_type must be a value out of EventType!")

    if event_type == EventType.NEW_PLOT:
        def i_callback(ev: EVENT) -> None:
            callback(ev.contents.new_plot_event)

    elif event_type == EventType.UPDATE_PLOT:
        def i_callback(ev: EVENT) -> None:
            callback(ev.contents.update_plot_event)

    elif event_type == EventType.SIZE:
        def i_callback(ev: EVENT) -> None:
            callback(ev.contents.size_event)

    else:
        def i_callback(ev: EVENT) -> None:
            callback(ev.contents.merge_end_event)

    c_func = _event_callback_t(i_callback)
    _registered_events[event_type] = c_func
    return _grm.grm_register(c_int(event_type.value), c_func)


@_require_runtime_version(0, 47, 0)
def unregister(event_type: EventType) -> int:
    """
    Deregister the callback for the given event type.

    :param event_type: The EventType to deregister the callback from.

    :raises TypeError: if event_type is not an EventType.
    """
    if not isinstance(event_type, EventType):
        raise TypeError("event_type must be a value out of EventType!")

    del _registered_events[event_type]
    return _grm.grm_unregister(c_int(event_type.value))


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_register.argtypes = [c_int, _event_callback_t]
    _grm.grm_register.restype = c_int

    _grm.grm_unregister.argtypes = [c_int]
    _grm.grm_unregister.restype = c_int

__all__ = [
    "register",
    "unregister",
    "EventType",
    "EVENT_NEW_PLOT",
    "EVENT_UPDATE_PLOT",
    "EVENT_SIZE",
    "EVENT_MERGE_END",
]
