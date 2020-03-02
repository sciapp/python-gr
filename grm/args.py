import numpy as np
from numpy import array, ndarray, float64, int32, empty, prod
from ctypes import c_int, c_double, c_char_p, c_void_p, c_uint8, c_uint
from ctypes import byref, POINTER, addressof, CDLL, CFUNCTYPE
from ctypes import create_string_buffer, cast
from gr import _require_runtime_version, _RUNTIME_VERSION, char

from . import _grm

class _ArgumentContainer:
    def __init__(self, ptr, params = None):
        self._ptr = ptr
        self._bufs = {}
        self._is_child = False
        if params is not None:
            self.update(params)

    def update(self, params):
        for k, v in params.items():
            self[k] = v

    @property
    def ptr(self):
        if self._ptr is None:
            raise ValueError("Pointer already dead!")
        return self._ptr

    def clear(self):
        _grm.grm_args_clear(self.ptr)
        self._bufs = {}

    def remove(self, name):
        _grm.grm_args_remove(self.ptr, char(name))
        del self._bufs[name]

    def contains(self, name):
        return _grm.grm_args_contains(self.ptr, char(name)) == 1

    def __setitem__(self, key, value):
        self.push(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.contains(key)

    def delete(self):
        """
        De-Initialises a argument container
        """
        if not self._is_child:
            _grm.grm_args_delete(self.ptr)
        self._delete()

    def _delete(self):
        """
        Frees the internal bufs and passes _delete to subcontainers.
        """
        if self._bufs is None:
            return
        for x in self._bufs.values():
            if isinstance(x, tuple):
                for y in x[1]:
                    y._delete()
        self._ptr = None
        self._bufs = None

    def push(self, name, values):
        """
        Pushes the argument with name to the argument container args_ptr, which should have been created using args_new.
        values is either:
            int, int-array
            float, float-array,
            string, string-array,
            arg container, arg container-array
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string!")

        if isinstance(values, int) or isinstance(values, float) or isinstance(values, str) or isinstance(values, dict) or isinstance(values, _ArgumentContainer):
            values = [values]

        if not isinstance(values, list):
            raise TypeError("Values must be int/int-array, float/float-array or string/string-array")

        length = c_int(len(values))

        typ = None
        for x in values:
            if typ is None:
                typ = type(x)
            elif typ == type(x):
                pass
            elif typ == int and isinstance(x, float):
                typ = float
            elif typ == float and isinstance(x, int):
                pass
            else:
                raise TypeError("All values in the array must be of the same type!")

        values_orig = values

        if typ == int:
            type_spec = create_string_buffer(b'nI')
            values = (c_int * len(values))(*values)
            self._bufs[name] = values
        elif typ == float:
            type_spec = create_string_buffer(b'nD')
            values = (c_double * len(values))(*values)
            self._bufs[name] = values
        elif typ == str:
            type_spec = create_string_buffer(b'nS')
            values = (c_char_p * len(values))(*[char(x) for x in values])
            self._bufs[name] = values
        elif typ == _ArgumentContainer:
            values_orig = [ new(x) if isinstance(x, dict) else x for x in values_orig]
            for x in values_orig:
                x._is_child = True

            type_spec = create_string_buffer(b'nA')
            values = (c_void_p * len(values_orig))(*[x.ptr for x in values_orig])

            self._bufs[name] = (values, values_orig) # This also stores the ArgumentContainers, so if 'self' is destructed, they loose a reference, and can be destructed, too.
        else:
            raise TypeError("Unsupported type: " + typ)
        args = (self.ptr, char(name), type_spec, length, values)

        print(args)
        result = _grm.grm_args_push(*args)
        if result == 0:
            return False # TODO: Exceptions?
        return True

    def __del__(self):
        if self._ptr is not None:
            self.delete()

@_require_runtime_version(0, 47, 0)
def new(params = None):
    """
    Initialises a new argument container
    """
    return _ArgumentContainer(_grm.grm_args_new(), params)


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_args_new.argtypes = []
    _grm.grm_args_new.restype = c_void_p

    _grm.grm_args_push.argtypes = [c_void_p, c_char_p, c_char_p, c_int, c_void_p]
    _grm.grm_args_push.restype = c_int

    _grm.grm_args_clear.argtypes = [c_void_p]
    _grm.grm_args_clear.restype = None

    _grm.grm_args_remove.argtypes = [c_void_p, c_char_p]
    _grm.grm_args_remove.restype = None

    _grm.grm_args_contains.argtypes = [c_void_p, c_char_p]
    _grm.grm_args_contains.restype = c_int

    _grm.grm_args_delete.argtypes = [c_void_p]
    _grm.grm_args_delete.restype = None


__all__ = ['new']
