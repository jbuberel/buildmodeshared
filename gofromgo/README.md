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



# Go from Go

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
