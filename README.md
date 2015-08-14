# Using Go Shared Libraries

[TOC]

## Calling a Go Library from Python

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

### Creating a workspace

```
$ mkdir ~/goproj/
$ cd ~/goproj/
$ export GOPATH=`pwd`
$ mkdir bin src pkg
```

Now, setup the directory structure for the sample Go app:

```
$ cd $GOPATH
$ mkdir -p src/dns/dnscmd src/dns/dnslib
$ touch src/dns/dnscmd/dnscmd.go src/dns/dnslib/dnslib.go
```

The application is trivial. The `dns/dnslib.go` will contain two
funcitons that will be exported symbols in our shared library -
`ReturnString` and `ReturnInt`. We need to create a Go command which
will be our compile target; that is what `dns/dnscmd.go` is for. Even though
that file has a `func main()` declared, that funciton will not be called.

Set the contents of the `src/dns/dnscmd/dnscmd.go` file to this:

```
package main

import (
	"C"
	"dns/dnslib"
	"fmt"
)

func main() {
	fmt.Println(dnslib.ReturnString("golang.org"))
	fmt.Println(dnslib.ReturnInt(3))
}
```

Set the contents of the `src/dns/dnslib/dnslib.go` file to the snippet below.
Note that the spacing of the `//export` is specific - there should be no space
between the `//` and the `export` text:

```
package dnslib

import (
	"C"
	"net"
)

// export ReturnString
func ReturnString(val string) string {
	cname, err := net.LookupCNAME(val)
	if err != nil {
		return "Could not find CNAME"
	}
	return cname
}

// export ReturnInt
func ReturnInt(val int) int {
	return val + 3
}
```

### Compiling the library

You should now be ready to compile this into a working binary application,
composed of shared libraries (.so) instead of a single statically linked
binary (the Go default).

Last step is to build your shared library. We use the -o option to specify
the name of the shared object file:

```
$ cd $GOPATH
$ go install -buildmode=c-shared -o mylib.so dns/dnscmd
```

When this build completes, you will see a few new files in your workspace.
The file you'll be using is the `dnscmd.a` (not `dnslib.a`), which contains
the exported symbols:

```
$ tree
.
mylib.so
├── bin
├── pkg
└── src
    └── dns
        ├── dnscmd
        │   └── dnscmd.go
        └── dnslib
            └── dnslib.go
```

### Viewing the exported symbols

Having compiled the `dns/dnscmd/dnscmd.go` program into a `.a` file, you should be
able to extract the list of exported symbols using `nm -g`. In that output
you should see `ReturnString` and `ReturnInt`:

```
$ nm -g pkg/linux_amd64_shared/dns/dnscmd.a
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

### Using the library from Python

We have two examples that demonstrate calling the `ReturnInt` and
`ReturnString` methods from Python. Pease keep in mind that both
of these examples are very early drafts and lack many of the features
you would need to use this in production-quality code.

Memory management, function pointers and a host of potential problems are not
automatically handled. Simplifying this process will require the addition of
Python-specific support in the `gobind` tool via community contributions.

The first example uses `ctypes` - be sure to configured the correct
pathname to the generated `dnscmd.a` file in the call to `ctypes.CDLL`:

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



lib = ctypes.CDLL('./pkg/linux_amd64_shared/dns/dnscmd.a')

lib.ReturnInt.argtypes = [GoInt]
lib.ReturnInt.restype = GoInt

lib.ReturnString.argtypes = [GoString]
lib.ReturnString.restype = GoString

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
# $GOPATH/$ARCH/dns/dnslib.h. Note that you can't copy/paste the whole thing
# if you're using ABI.
ffi.cdef("""
    typedef long long GoInt;
    typedef struct { char *p; GoInt n; } GoString;
    GoInt ReturnInt(GoInt);
    GoString ReturnString(GoString);
""")

# Note - use dnscmd.a, not dnslib.a.
dnslib = ffi.dlopen("pkg/darwin_amd64/dns/dnscmd.a")


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

def toPythonString(go_string):
    return ffi.buffer(go_string.p, go_string.n)[:]


# Now we can call the ReturnString function

# Note that Go strings are passed by value and not by pointer, but toGoString
# is required by CFFI to make a GoString*. We can use [0] to deference it to
# a value.
print toPythonString(dnslib.ReturnString(toGoString("golang.org")))

```


## Calling a Go Library from Go

This section describes how you can compile a Go package as a shared object
(on linux, named \*.so typically) that can be invoked by a Go program. This
assumes you have a working go15 installation.

### Creating a workspace

```
$ mkdir ~/goproj/
$ cd ~/goproj/
$ export GOPATH=`pwd`
$ mkdir bin src pkg
```

Now, setup the directory structure for the sample Go app:

```
$ cd $GOPATH
$ mkdir -p src/dns/dnscmd src/dns/dnslib
$ touch src/dns/dnscmd/dnscmd.go src/dns/dnslib/dnslib.go
```

The application is trivial. A `main` func that just calls a simple
function exported by the `dnslib` package.

Set the contents of the `src/dns/dnscmd/dnscmd.go` file to this:

```
package main

import (
	"C"
	"dns/dnslib"
	"fmt"
)

func main() {
	fmt.Println(dnslib.ReturnString("golang.org"))
	fmt.Println(dnslib.ReturnInt(3))
}
```

Set the contents of the `src/dns/dnslib/dnslib.go` file to this:

```
package dnslib

import (
	"C"
	"net"
)

func ReturnString(val string) string {
	cname, err := net.LookupCNAME(val)
	if err != nil {
		return "Could not find CNAME"
	}
	return cname
}

func ReturnInt(val int) int {
	return val + 3
}
```



### Compiling a simple application and library

You should now be ready to compile this into a working binary application.
The result will be an executable command that is dynamically linked to a
set of shared libraries.

This command will build a shared object of the entire Go standard library:

```
$ cd $GOPATH
$ go install -buildmode=shared std
```

The resulting .so file will be found in your go15 directory:

```
$ ls -l ~/go15/pkg/linux_amd64_dynlink/libstd.so
```

Next, we're going to build the dnslib package into a library:

```
$ cd $GOPATH
$ go install -buildmode=shared -linkshared dns/dnslib
```

You should now have a .so file named `libdns-dnslib.so` located here:

```
.
├── bin
├── pkg
│   └── linux_amd64_dynlink
│       ├── dns
│       │   ├── dnslib.a
│       │   └── dnslib.shlibname
│       └── libdns-dnslib.so
└── src
    └── dns
        ├── dnscmd
        │   └── dnscmd.go
        └── dnslib
            └── dnslib.go

```

Last step is to build the a program that you can run that will be
linked to the library:

```
$ cd $GOPATH
$ go install -linkshared dns/dnscmd
```

The `dnscmd` executable will be found in your `$GOPATH/bin` directory. It is
dynamically linked to the `libdns-dnslib.so` and the `libstd.so`:

```
$ cd $GOPATH/bin
$ ./dnscmd
golang.org.
10
```

