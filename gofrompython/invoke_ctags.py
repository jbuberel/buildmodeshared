import ctypes

GoInt = ctypes.c_int64

class GoString(ctypes.Structure):
    _fields_ = [('p', ctypes.c_char_p),
                ('n', GoInt)]

    # Convenience functions to convert from a Python string
    @classmethod
    def from_param(cls, value):
        return cls(value, len(value))

    def __str__(self):
        return ctypes.string_at(self.p, self.n)



lib = ctypes.CDLL('mylib.so')

lib.ReturnInt.argtypes = [GoInt]
lib.ReturnInt.restype = GoInt

lib.ReturnString.argtypes = [GoString]
lib.ReturnString.restype = GoString

print lib.ReturnInt(42)          # 45
print lib.ReturnString("golang.org")  # "Your value: World"
