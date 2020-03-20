"""
This is a procedural interface to the GRM plotting part of the GR framework.

The complete module requires runtime version 0.47.0, and is only supported on Python 3.
"""

from ctypes import create_string_buffer, cast, c_char_p
from gr.runtime_helper import load_runtime

_grm = load_runtime(lib_name="libGRM")
if _grm is None:
    raise ImportError("Failed to load GRM runtime!")


def _encode_str_to_char_p(string: str) -> c_char_p:
    return cast(create_string_buffer(string.encode("utf-8")), c_char_p)


from . import args  # noqa E402
from . import event  # noqa E402
from . import interaction  # noqa E402
from . import plot  # noqa E402

__all__ = ["args", "event", "interaction", "plot"]
