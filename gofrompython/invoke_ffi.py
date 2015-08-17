"""
This is a simple, ABI in-line example of using CFFI to communicate with
a Go library.
"""

from cffi import FFI

ffi = FFI()

# You can either write these yourself, or pull them from
# $GOPATH/$ARCH/dns/dnslib.h. Note that you only need to pull out the
# definitions for the typedefs, structs, and functions that you use.
ffi.cdef("""
    typedef long long GoInt;
    typedef struct { char *p; GoInt n; } GoString;
    GoInt ReturnInt(GoInt);
    char* ReturnString(GoString);
""")

dnslib = ffi.dlopen("./mylib.so")


# Integers are easy - just call the function as normal:
print dnslib.ReturnInt(10)


# Strings are a bit harder. Go's strings are stored in a struct {char*, int},
# so we have to do conversion. This is further complicated by CFFI's ownership
# semantics - we have to ensure that the char* lives as long as the struct,
# otherwise the string will be garbage. We'll use a global weakref dictionary
# to track that.

import weakref
global_weakrefs = weakref.WeakKeyDictionary()


def toGoString(string):
    """Converts a Python string into the equivalent Go string and ensures the
    memory for the string lives as long as the struct reference."""
    string_p = ffi.new('char[]', string)
    v = ffi.new('GoString*', {
        'p': string_p,
        'n': len(string)
    })[0]
    global_weakrefs[v] = (string_p,)
    return v


# Now we can call the ReturnString function

# Note that Go strings are passed by value and not by pointer, but toGoString
# is required by CFFI to make a GoString*. We can use [0] to deference it to
# a value.
print ffi.string(dnslib.ReturnString(toGoString("golang.org")))
