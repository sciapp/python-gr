"""
This module ...
"""
from ctypes import c_int, c_char_p, c_uint, c_void_p
from ctypes import CFUNCTYPE
from typing import Callable, Union as UnionT, Dict, Optional

from gr import _require_runtime_version, _RUNTIME_VERSION
import grm

from . import _grm, _encode_str_to_char_p


_recv_callback_t = CFUNCTYPE(None, c_char_p, c_uint)
_send_callback_t = CFUNCTYPE(None, c_char_p, c_uint, c_char_p)


class Handle:
    def __init__(self, ptr: c_void_p):
        self.ptr = ptr

    def close(self) -> None:
        _grm.grm_close(self.ptr)

    def recv(
            self,
            args_container: UnionT[Dict[str, grm.args._ElemType], grm.args._ArgumentContainer]
    ) -> grm.args._ArgumentContainer:
        return recv(self, args_container)

    def send_args(
            self,
            args_container: UnionT[Dict[str, grm.args._ElemType], grm.args._ArgumentContainer]
    ) -> int:
        return send_args(self, args_container)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


@_require_runtime_version(0, 47, 0)
def open(
        is_receiver: bool,
        name: str,
        id: int,
        custom_recv: Optional[Callable[[str, int], None]],
        custom_send: Optional[Callable[[str, int, str], None]]
) -> Handle:
    """
    doc_string test
    """
    if not (isinstance(id, int) and id >= 0):
        raise ValueError("id is not an unsigned integer")
    if custom_recv is None:
        callback_recv = _recv_callback_t(0)
    else:
        callback_recv = _recv_callback_t(custom_recv)
    if custom_send is None:
        callback_send = _send_callback_t(0)
    else:
        callback_send = _send_callback_t(custom_send)
    # TODO check input

    return Handle(_grm.grm_open(
        c_int(is_receiver),
        _encode_str_to_char_p(name),
        c_uint(id),
        callback_recv,
        callback_send
    ))


@_require_runtime_version(0, 47, 0)
def close(handle: Handle) -> None:
    """

    """
    _grm.grm_close(handle.ptr)


@_require_runtime_version(0, 47, 0)
def recv(
        handle: Handle,
        args_container: UnionT[Dict[str, grm.args._ElemType], grm.args._ArgumentContainer]
) -> grm.args._ArgumentContainer:
    """

    """
    if isinstance(args_container, dict):
        args_container = grm.args.new(args_container)
    if not isinstance(args_container, grm.args._ArgumentContainer):
        raise ValueError("args_container is not a valid Dict or ArgumentContainer")
    return _grm.grm_recv(handle.ptr, args_container.ptr)


@_require_runtime_version(0, 47, 0)
def send(
        handle: Handle,
        args_container: UnionT[Dict[str, grm.args._ElemType], grm.args._ArgumentContainer]
) -> int:
    """

    """
    return send_args(handle, args_container)


@_require_runtime_version(0, 47, 0)
def send_args(
        handle: Handle,
        args_container: UnionT[Dict[str, grm.args._ElemType], grm.args._ArgumentContainer]
) -> int:
    """

    """
    if isinstance(args_container, dict):
        args_container = grm.args.new(args_container)
    if not isinstance(args_container, grm.args._ArgumentContainer):
        raise ValueError("args_container is not a valid Dict or ArgumentContainer")
    return _grm.grm_send_args(handle.ptr, args_container.ptr)


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_open.argtypes = [c_int, c_char_p, c_uint, _recv_callback_t, _send_callback_t]
    _grm.grm_open.restype = c_void_p

    _grm.grm_close.argtypes = [c_void_p]
    _grm.grm_close.restype = None

    _grm.grm_send_args.argtypes = [c_void_p, c_void_p]
    _grm.grm_send_args.restype = c_int

    _grm.grm_recv.argtypes = [c_void_p, c_void_p]
    _grm.grm_recv.restype = c_void_p

__all__ = [
    "open", "close", "send", "send_args", "recv"
]
