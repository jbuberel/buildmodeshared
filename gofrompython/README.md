# Go from Python

CAUTION: This is still a very manual process that requires a thorough
understanding of both Python and Go.  This also requires experience working
with the Python CTAGS or CFFI libraries. This could be made simpler with the
addition of Python-language support to the `gobind` command, and we would
welcome community contributions to make this happen.

A big thanks to Jon Parrott <jonwayne@google.com> for providing the
CFFI Python example, and to Amaury Forgeot d'Arc <amauryfa@google.com> for the
ctypes Python example.

To start the tutorial, we're going to setup a Go workspace. We'll
then create a simple library with two exported functions. After compiling the
library into the appropriate shared object, you'll see two methods for
calling those funcitons from Python (CTAGS, CFFI).

## Install the prerequisites

For these two examples, you'll need a working Python installation that includes the `ctypes` and `cffi` libraries.

The `ctypes` support should be part of your Python installation. To install the `cffi` package on an Ubuntu-like system, do the following:

```
$ sudo apt-get install libffi-dev
...
$ sudo pip install cffi
```

## Setup a workspace

Starting in the top-level directoy in which you cloned this repo:

```
$ cd gofrompython
$ export GOPATH=`pwd`
```

The application is trivial. The `dns/dnslib.go` will contain two
funcitons that will be exported symbols in our shared library -
`ReturnString` and `ReturnInt`. We need to create a Go command which
will be our compile target; that is what `dns/dnscmd.go` is for. Even though
that file has a `func main()` declared, that funciton will not be called.

You can [view the source here](./src/dns/dnscmd/dnscmd.go), and below:

```
package main

import (
    "C"
    _ "dns/dnslib"
)

func main() {
}

```


You can [view the source of the library here](./src/dns/dnslib/dnslib.go) and below. Note that the spacing of the `//export` is specific - there should be no space between the `//` and the `export` text:

```
package dnslib

import (
    "C"
    "net"
)

//export ReturnString
func ReturnString(val string) *C.char {
    cname, err := net.LookupCNAME(val)
    if err != nil {
        C.CString("Could not find CNAME")
    }
    return C.CString(cname)
}

//export ReturnInt
func ReturnInt(val int) int {
    return val + 3
}
```

## Compiling the library

You should now be ready to compile this into a working binary application,
composed of shared libraries (.so) instead of a single statically linked
binary (the Go default).

Last step is to build your shared library. We use the -o option to specify
the name of the shared object file:

```
$ cd $GOPATH
$ go build -buildmode=c-shared -o mylib.so dns/dnscmd
```

When this build completes, you will see a few new files in current directory named `mylib.so`.

## Viewing the exported symbols

Having compiled the `dns/dnscmd/dnscmd.go` program into a `.so` file, you should be
able to extract the list of exported symbols using `nm -g`. In that output
you should see `ReturnString` and `ReturnInt`:

```
$ nm -g mylib.so
                 U abort@@GLIBC_2.2.5
0000000000466348 B __bss_start
...
00000000001268f0 T ReturnInt
00000000001268a0 T ReturnString
...
0000000000128a30 T crosscall2
00000000000d2b97 T crosscall_amd64
...

```

## Using the library from Python

We have two examples that demonstrate calling the `ReturnInt` and
`ReturnString` methods from Python. Pease keep in mind that both
of these examples are very early drafts and lack many of the features
you would need to use this in production-quality code.

Memory management, function pointers and a host of potential problems are not
automatically handled. Simplifying this process will require the addition of
Python-specific support in the `gobind` tool via community contributions.

The first example uses `ctypes` - be sure to configured the correct
pathname to the generated `dnscmd.so` file in the call to `ctypes.CDLL`:

```python
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
print lib.ReturnString("golang.org")  # "golang.org."
```

The second example uses `FFI` - be sure to configured the correct
pathname to the generated `dnscmd.a` file in the call to `ffi.dlopen`:

```python
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

```
