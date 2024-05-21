"""
This module gives access to the ArgumentContainers exposed by GRM.

It is used to pass plotting data, settings and other data to GRM.
"""
import ctypes
import sys

import numpy as np
from ctypes import c_int, c_uint, c_double, c_char_p, c_void_p, c_char
from ctypes import CFUNCTYPE, POINTER, Structure, create_string_buffer, cast

from typing import Union, Tuple, Dict, Optional, Any, Iterable, Mapping

from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm, _encode_str_to_char_p


_ElemType = Union[
    np.ndarray,
    int,
    float,
    str,
    "_ArgumentContainer",
    Mapping[str, "_ElemType"],
    Iterable[Union[int, float]],
    Iterable[str],
    Iterable[Union[Mapping[str, "_ElemType"], "_ArgumentContainer"]],
    Tuple[Union[int, float], ...],
    Tuple[str, ...],
    Tuple[Union[Mapping[str, "_ElemType"], "_ArgumentContainer"], ...]
]


class _ArgumentContainer:
    def __init__(self, ptr: Union[c_void_p, int], params: Optional[Mapping[str, _ElemType]] = None, is_weak_ref: bool = True) -> None:
        """
        Initialize the class using the given pointer and optional params to insert directly.

        :param ptr: The pointer returned by grm_args_new
        :param params: The data to set after init
        """
        if isinstance(ptr, int):
            ptr = c_void_p(ptr)
        self._ptr: Optional[c_void_p] = ptr
        self._bufs: Dict[str, Any] = {}
        self._is_child = not is_weak_ref
        if params is not None:
            self.update(params)

    def update(self, params: Mapping[str, _ElemType]) -> None:
        """
        Update the argument container with the given dictionary params, by calling self.push(k, v) on each item.

        :param params: The data to set. On each element, self[k] = v is called, inserting the element.
        """
        for k, v in params.items():
            self[k] = v

    @property
    def ptr(self) -> c_void_p:
        """
        Return the internal pointer of the argument container. Should not be modified or otherwise dealt with, primarily for use of internal classes.

        :raises ValueError: if the container was already deleted.
        """
        if self._ptr is None:
            raise ValueError("Pointer already dead!")
        return self._ptr

    def clear(self) -> None:
        """
        Clear the argument container and frees all resources held by bufs.

        :raises ValueError: if the container was already deleted.
        """
        _grm.grm_args_clear(self.ptr)
        self._bufs = {}

    def remove(self, name: str) -> None:
        """
        Remove the given key `name` from the argument container, and frees the ressource held by it.

        `name in self` should be false after that.

        :param name: the key to remove

        :raises ValueError: if the container was already deleted.
        """
        _grm.grm_args_remove(self.ptr, _encode_str_to_char_p(name))
        del self._bufs[name]

    def contains(self, name: str) -> bool:
        """
        If the key `name` is contained in the argument, then return true.

        :param name: the key to check for.

        :raises ValueError: if the container was already deleted.
        """
        return bool(_grm.grm_args_contains(self.ptr, _encode_str_to_char_p(name)))

    def __setitem__(self, key: str, value: _ElemType) -> None:
        self.push(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove(key)

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def delete(self) -> None:
        """
        De-Initialises a argument container (e.g. clear and destroy).
        """
        if not self._is_child:
            _grm.grm_args_delete(self.ptr)
        self._delete()

    def _delete(self) -> None:
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
        del self._bufs

    def dump(self) -> None:
        if not hasattr(_grm, "grm_dump"):
            raise NotImplementedError("grm_dump is not included in this build")
        libc = ctypes.cdll.LoadLibrary('libSystem.dylib')
        cfdopen = libc.fdopen
        cfdopen.argtypes = [c_int, c_char_p]
        cfdopen.restype = c_void_p
        cstdout = cfdopen(sys.stdout.fileno(), b'w')
        _grm.grm_dump(self.ptr, cstdout)

    def push(self, name: str, values_to_insert: _ElemType) -> bool:
        """
        Pushes the argument with name to the argument container args_ptr, which should have been created using args_new.

        This function also silently overwrites entries with the same name.

        You can always mix int values and float values, but they will then all be converted to floats.

        One-dimensional numpy.ndarray with either Float64 or Int32 can also be passed.

        Multi-dimensional numpy.ndarrays with either Float64 or Int32 can also be passed, they will be passed flattened,
        but :code:`name` _dims is populated with the shape beforehand.

        The exception is if the name is `absolute`, `relative` or `error` where ndarrays with a shape of [2, N] are
        passed as :code:`nDD`.

        :param name: The key to insert.
        :param values_to_insert: The data to insert.

        :raises TypeError: if name or values (or the child elements of values) are of no correct type.
        :raises ValueError: if one of the _ArgumentContainer elements is already a child of another or the container is already deleted.
        """
        # Remove type annotation to silence mypy
        values: Any = values_to_insert
        if not isinstance(name, str):
            raise TypeError("Name must be a string!")

        if isinstance(values, int):
            type_spec = create_string_buffer(b"i")
            values = c_int(values)
            # self._bufs[name] = values
            result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, values)
            return bool(result)
        if isinstance(values, float):
            type_spec = create_string_buffer(b"d")
            values = c_double(values)
            # self._bufs[name] = values
            result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, values)
            return bool(result)
        if isinstance(values, str):
            type_spec = create_string_buffer(b"s")
            values = _encode_str_to_char_p(values)
            # self._bufs[name] = values
            result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, values)
            return bool(result)
        if isinstance(values, dict):
            values = new(values)
        if isinstance(values, _ArgumentContainer):
            type_spec = create_string_buffer(b"a")
            # self._bufs[name] = values

            values._is_child = True
            result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, values.ptr)
            return bool(result)

        if isinstance(values, (int, float, str, bool, dict, _ArgumentContainer)):
            values = [values]

        if not isinstance(values, (tuple, list, np.ndarray)):
            raise TypeError(
                "Values must be int/int-array, float/float-array or string/string-array or dict/dict-array, _ArgumentContainer/_ArgumentContainer-array"
            )

        values_orig = values

        if isinstance(values, np.ndarray):
            values = np.ascontiguousarray(values)
            if values.ndim > 1:
                if values.ndim == 2 and values.shape[0] == 2 and name in ["error", "relative", "absolute"]:
                    if values.dtype == np.float64:
                        values_1 = values[0].ctypes.data_as(POINTER(c_double))
                        values_2 = values[1].ctypes.data_as(POINTER(c_double))
                        type_spec = create_string_buffer(b"nDD")
                    else:
                        raise TypeError(
                            "The ndarray has type " + values.dtype.name + ", but it must be float64"
                        )

                    self._bufs[name] = [values_1, values_2]
                    result = int(_grm.grm_args_push(
                        self.ptr, _encode_str_to_char_p(name), type_spec, c_uint(values.shape[1]), values_1, values_2
                    ))
                    return bool(result)  # TODO: Exceptions

                self[name + "_dims"] = values.shape
                values_orig = values = values.ravel()

            if values.dtype == np.float64:
                type_spec = create_string_buffer(b"nD")
                values = values.ctypes.data_as(POINTER(c_double))
            elif values.dtype == np.int32:
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
                elif typ is type(x):
                    pass
                elif typ is int and isinstance(x, float):
                    typ = float
                elif typ is float and isinstance(x, int):
                    pass
                elif typ is dict and isinstance(x, _ArgumentContainer):
                    pass
                elif typ is _ArgumentContainer and isinstance(x, dict):
                    typ = dict
                else:
                    raise TypeError("All values in the array must be of the same type!")

            if name in ["relative", "absolute"] and (typ == list or typ == tuple):
                typ = None
                for v in values:
                    for x in v:
                        if typ is None:
                            typ = type(x)
                        elif typ is type(x):
                            pass
                        else:
                            raise TypeError("All values in the array must be of the same type!")
                values_1 = (c_double * len(values[0]))(*values[0])
                values_2 = (c_double * len(values[1]))(*values[1])
                type_spec = create_string_buffer(b"nDD")
                self._bufs[name] = [values_1, values_2]
                result = int(_grm.grm_args_push(
                    self.ptr, _encode_str_to_char_p(name), type_spec, c_uint(len(values_1)), values_1, values_2
                ))
                return bool(result)

            if typ == int or typ == bool:
                type_spec = create_string_buffer(b"nI")
                values = (c_int * len(values))(*values)
                self._bufs[name] = values
            elif typ == float or typ == np.float64:
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

        length = c_uint(len(values_orig))

        result = _grm.grm_args_push(self.ptr, _encode_str_to_char_p(name), type_spec, length, values)
        if result == 0:
            return False  # TODO: Exceptions?
        return True

    def __del__(self) -> None:
        """
        Destructor to optionally free resources and destroy the c container, if not already done.
        """
        if self._ptr is not None:
            self.delete()

    def __iter__(self) -> "_ArgsIter":
        return _ArgsIter(_grm.grm_args_iter(self.ptr))

    def as_dict(self) -> Dict[str, _ElemType]:
        return {k: v for k, v in self}


class _ArgsIterStruct(Structure):
    pass


class _ArgStruct(Structure):
    _fields_ = [
        ("key", c_char_p),
        ("value_ptr", c_void_p),
        ("value_format", c_char_p)
    ]


_ArgsIterStruct._fields_ = [
    ("next", CFUNCTYPE(POINTER(_ArgStruct), POINTER(_ArgsIterStruct))),
    ("arg", c_void_p)
]


class _ArgValueIterStruct(Structure):
    pass


_ArgValueIterStruct._fields_ = [
    ("next", CFUNCTYPE(c_void_p, POINTER(_ArgValueIterStruct))),
    ("value_ptr", c_void_p),
    ("format", c_char),
    ("is_array", c_int),
    ("array_length", c_void_p),
    ("priv", c_void_p)
]


class _ArgsIter:
    def __init__(self, ptr: POINTER(_ArgsIterStruct)) -> None:  # type: ignore[valid-type]
        self.ptr = ptr

    def __next__(self) -> Tuple[str, _ElemType]:
        arg_ptr = self.ptr.contents.next(self.ptr)
        if not arg_ptr:
            raise StopIteration

        key: str = arg_ptr.contents.key.decode()

        value_iter = _ArgValueIter(_grm.grm_arg_value_iter(arg_ptr))

        res = []
        for val in value_iter:
            if val is None:
                raise ValueError(f"No data found for key {key}")
            res.append(val)

        if len(res) == 1:
            return key, res[0]

        # TODO fix mypy without type ignore
        return key, res  # type: ignore


class _ArgValueIter:
    def __init__(self, ptr: POINTER(_ArgValueIterStruct)) -> None:  # type: ignore[valid-type]
        self.ptr = ptr

    def __iter__(self) -> "_ArgValueIter":
        return self

    def __next__(self) -> Optional[_ElemType]:
        val = self.ptr.contents.next(self.ptr)
        if val is None:
            raise StopIteration

        f = self.ptr.contents.format.decode()

        value: Optional[_ElemType]
        if self.ptr.contents.is_array:
            val = cast(c_void_p(val), POINTER(c_void_p)).contents

            value = []
            if f == "d":
                buffer_as_ctypes_array = cast(val, POINTER(c_double * self.ptr.contents.array_length))[0]
                buffer_as_numpy_array = np.frombuffer(buffer_as_ctypes_array, np.float64)
                value = list(buffer_as_numpy_array)
            if f == "i":
                buffer_as_ctypes_array = cast(val, POINTER(c_int * self.ptr.contents.array_length))[0]
                buffer_as_numpy_array = np.frombuffer(buffer_as_ctypes_array, np.int32)
                value = list(buffer_as_numpy_array)
            if f == "s":
                s = cast(val, POINTER(c_char_p * self.ptr.contents.array_length))[0]
                value = [i.decode() for i in s]
            if f == "a":
                buffer_as_ctypes_array = cast(val, POINTER(c_void_p * self.ptr.contents.array_length))[0]
                value = [_ArgumentContainer(buffer_as_ctypes_array[i], is_weak_ref=False).as_dict() for i in range(len(buffer_as_ctypes_array))]
        else:
            value = None
            if f == "d":
                val = cast(c_void_p(val), POINTER(c_double))
                value = val.contents.value
            if f == "i":
                val = cast(c_void_p(val), POINTER(c_int))
                value = val.contents.value
            if f == "s":
                val = cast(c_void_p(val), POINTER(c_char_p))
                value = val.contents.value.decode()
            if f == "a":
                val = cast(c_void_p(val), POINTER(c_void_p))
                value = _ArgumentContainer(val.contents, is_weak_ref=False).as_dict()

        return value


@_require_runtime_version(0, 47, 0)
def new(params: Optional[Mapping[str, _ElemType]] = None) -> _ArgumentContainer:
    """
    Initialise a new argument container with optional initialization data.

    :param params: Each element in this dictionary is written into the container at initialization time.
    """
    return _ArgumentContainer(_grm.grm_args_new(), params)


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_args_new.argtypes = []
    _grm.grm_args_new.restype = c_void_p

    # Import note: `grm_args_push` is a variadic function and only non-variadic function arguments must be specified in
    # the `argtypes` attribute. The variadic part must not be declared here! Otherwise, calling `grm_args_push` will
    # fail on some platforms, e.g. Apple Silicon. For more information see
    # <https://docs.python.org/3/library/ctypes.html#calling-variadic-functions>.
    _grm.grm_args_push.argtypes = [c_void_p, c_char_p, c_char_p]
    _grm.grm_args_push.restype = c_int

    _grm.grm_args_clear.argtypes = [c_void_p]
    _grm.grm_args_clear.restype = None

    _grm.grm_args_remove.argtypes = [c_void_p, c_char_p]
    _grm.grm_args_remove.restype = None

    _grm.grm_args_contains.argtypes = [c_void_p, c_char_p]
    _grm.grm_args_contains.restype = c_int

    _grm.grm_args_delete.argtypes = [c_void_p]
    _grm.grm_args_delete.restype = None

    _grm.grm_args_iter.argtypes = [c_void_p]
    _grm.grm_args_iter.restype = POINTER(_ArgsIterStruct)

    _grm.grm_arg_value_iter.argtypes = [c_void_p]
    _grm.grm_arg_value_iter.restype = POINTER(_ArgValueIterStruct)

    if hasattr(_grm, "grm_dump"):
        _grm.grm_dump.argtypes = [c_void_p, c_void_p]
        _grm.grm_dump.restype = c_void_p

__all__ = ["new", "_ElemType"]
