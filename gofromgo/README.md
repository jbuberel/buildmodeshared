# Go from GO

This section describes how you can compile a Go package as a shared object
(on linux, named `.so` typically) that can be invoked by a Go program. This
assumes you have a working go15 installation. 

NOTE: This has only been tested on Linux.

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
$ ls -la ~/go15/pkg/linux_amd64_dynlink/libstd.so 
-rw-r----- 1 jbuberel eng 38356768 Aug 14 13:42 /usr/local/google/home/jbuberel/go15/pkg/linux_amd64_dynlink/libstd.so

$ file ~/go15/pkg/linux_amd64_dynlink/libstd.so 
/usr/local/google/home/jbuberel/go15/pkg/linux_amd64_dynlink/libstd.so: ELF 64-bit LSB  shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=f58f09cda800bd276b52492c85470aefad2c8fb8, not stripped
```

Next, we're going to build the dnslib package into a library, but this time we're going to tell the compiler to dynamically link our library against the `libstd.so` that we created in the previous step:

```
$ cd $GOPATH
$ go install -buildmode=shared -linkshared dns/dnslib
```

You should now have a .so file named `libdns-dnslib.so` located in `./pkg/linux_amd64_dynlink`:

```
$ tree 
.
├── pkg
│   └── linux_amd64_dynlink
│       ├── dns
│       │   ├── dnslib.a
│       │   └── dnslib.shlibname
│       └── libdns-dnslib.so
├── README.md
└── src
    └── dns
        ├── dnscmd
        │   └── dnscmd.go
        └── dnslib
            └── dnslib.go

```

Last step is to build the `dnscmd` program that you can run. It will be
linked to the library:

```
$ cd $GOPATH
$ go install -linkshared dns/dnscmd
```

The `dnscmd` executable will be found in your `$GOPATH/bin` directory. It is
dynamically linked to the `libdns-dnslib.so` and the `libstd.so`. You can verify this from the size of the `dnscmd` binary (just 17k):

```
$ ./bin/dnscmd
golang.org.
45

$ file ./bin/dnscmd
./bin/dnscmd: ELF 64-bit LSB  executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=207aeb60eb5c4b67c8ba14975be3f99a7d504511, not stripped

$ ls -la ./bin/dnscmd
-rwxr-x--- 1 jbuberel eng 17550 Aug 14 13:53 ./bin/dnscmd

```

And just to prove that this is dynamically linked, delete the `dnscmd` binary, and rebuild it without the `-linkshared` option. Size is now 3.3Mb:

```
$ rm ./bin/dnscmd
$ go install dns/dnscmd
$ ls -lha ./bin/dnscmd 
-rwxr-x--- 1 jbuberel eng 3.3M Aug 14 13:56 ./bin/dnscmd

```

If you do move the `dnslib.so` file to a different directly, you'll need to ensure that the new location is in your `$LD_LIBRARY_PATH` environment variable.
