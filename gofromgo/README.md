# Go from GO

This section describes how you can compile a Go package as a shared object
(on linux, named `.so` typically) that can be invoked by a Go program. This
assumes you have a working go15 installation.

## Creating a workspace

From the root of the directory where you cloned this repository:

```
$ cd gofromgo
$ export GOPATH=`pwd`
```

Our library, `dnslib` will export two functions - `ReturnString` and `ReturnInt`. You can [view the source here](./src/dns/dnslib/dnslib.go) and below:

```
package dnslib

import (
    "C"
    "net"
)

//export ReturnString
func ReturnString(val string) string {
    cname, err := net.LookupCNAME(val)
    if err != nil {
        return "Could not find CNAME"
    }
    return cname
}

//export ReturnInt
func ReturnInt(val int) int {
    return val + 3
}
```

The command - `dnscmd` - is trival. It contains a simple main function that invokes the two methods from the `dnslib` package.

You can [view the source here](./src/dns/dnscmd/dnscmd.go) and below:

```
package main

import (
    "C"
    "dns/dnslib"
)

func main() {
    fmt.Println(dnslib.ReturnString("golang.org"))
    fmt.Println(dnslib.ReturnInt(42))
}
```

## Building

You should now be ready to compile this into a working binary application.
The result will be an executable command that is dynamically linked to a
set of shared libraries. 

The first step is to create a shared object of the Go standard library:

```
$ cd $GOPATH
$ go install -buildmode=shared std
```

The resulting .so file will be found in your go15 directory. The exact location you see may differ depending on where you have go15 installed:

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
