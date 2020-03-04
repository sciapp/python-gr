import numpy as np
from ctypes import c_int, c_double, c_char_p, c_void_p
from ctypes import POINTER, create_string_buffer
from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm, _encode_str_to_char_p


class _ArgumentContainer:
    def __init__(self, ptr, params=None):
        self._ptr = ptr
        self._bufs = {}
        self._is_child = False
        if params is not None:
            self.update(params)

    def update(self, params):
        """
        Updates the argument container with the given dictionary params, by calling self.push(k, v) on each item
        """
        for k, v in params.items():
            self[k] = v

    @property
    def ptr(self):
        """
        Returns the internal pointer of the argument container. Should not be modified or otherwise dealt with,
        primarily for use of internal classes
        """
        if self._ptr is None:
            raise ValueError("Pointer already dead!")
        return self._ptr

    def clear(self):
        """
        Clears the argument container and frees all resources held by bufs
        """
        _grm.grm_args_clear(self.ptr)
        self._bufs = {}

    def remove(self, name):
        """
        Removes the given key `name` from the argument container, and frees the ressource held by it.
        """
        _grm.grm_args_remove(self.ptr, _encode_str_to_char_p(name))
        del self._bufs[name]

    def contains(self, name):
        """
        Returns true, if the given key `name` is set in the container
        """
        return _grm.grm_args_contains(self.ptr, _encode_str_to_char_p(name)) == 1

    def __setitem__(self, key, value):
        self.push(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.contains(key)

    def delete(self):
        """
        De-Initialises a argument container (e.g. clear and destroy)
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

        if isinstance(values, (int, float, str, dict, _ArgumentContainer)):
            values = [values]

        if not isinstance(values, (list, np.ndarray)):
            raise TypeError("Values must be int/int-array, float/float-array or string/string-array")

        values_orig = values

        if isinstance(values, np.ndarray):
            if values.ndim != 1:
                raise TypeError("The numpy ndarray must be one-dimensional")

            if values.dtype.name == "float64":
                type_spec = create_string_buffer(b"nD")
                values = values.ctypes.data_as(POINTER(c_double))
            elif values.dtype.name == "int32":
                type_spec = create_string_buffer(b"nI")
                values = values.ctypes.data_as(POINTER(c_int))
            else:
                raise TypeError("The given ndarray does not have the correct type.")
            self._bufs[name] = values
        else:
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
                elif typ == dict and isinstance(x, _ArgumentContainer):
                    pass
                elif typ == _ArgumentContainer and isinstance(x, dict):
                    typ = dict
                else:
                    raise TypeError("All values in the array must be of the same type!")

            if typ == int:
                type_spec = create_string_buffer(b"nI")
                values = (c_int * len(values))(*values)
                self._bufs[name] = values
            elif typ == float:
                type_spec = create_string_buffer(b"nD")
                values = (c_double * len(values))(*values)
                self._bufs[name] = values
            elif typ == str:
                type_spec = create_string_buffer(b"nS")
                values = (c_char_p * len(values))(*[_encode_str_to_char_p(x) for x in values])
                self._bufs[name] = values
            elif typ == _ArgumentContainer or typ == dict:
                values_orig = [new(x) if isinstance(x, dict) else x for x in values_orig]
                for x in values_orig:
                    if x._is_child:
                        raise ValueError("This ArgumentContainer is already a child of another!")
                    x._is_child = True

                type_spec = create_string_buffer(b"nA")
                values = (c_void_p * len(values_orig))(*[x.ptr for x in values_orig])

                self._bufs[name] = (
                    values,
                    values_orig,
                )  # This also stores the ArgumentContainers, so if 'self' is destructed, they loose a reference, and can be destructed, too.
            else:
                raise TypeError("Unsupported type: " + repr(typ))
        length = c_int(len(values_orig))

        result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, length, values)
        if result == 0:
            return False  # TODO: Exceptions?
        return True

    def __del__(self):
        """
        Destructor to optionally free resources and destroy the c container, if not already done
        """
        if self._ptr is not None:
            self.delete()


@_require_runtime_version(0, 47, 0)
def new(params=None):
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


__all__ = ["new"]
