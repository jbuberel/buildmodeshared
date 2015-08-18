# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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



lib = ctypes.CDLL('./mylib.so')

lib.ReturnInt.argtypes = [GoInt]
lib.ReturnInt.restype = GoInt

lib.ReturnString.argtypes = [GoString]
lib.ReturnString.restype = ctypes.c_char_p

print lib.ReturnInt(42)          # 45
print lib.ReturnString("golang.org")  # "Your value: World"
