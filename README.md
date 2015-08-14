# Using Go Shared Libraries

This project demonstrates two new features that were added in the Go 1.5
release.

* The ability to compile a Go program that is dynamically linked to other
Go libraries.
* The ability to compile a set of Go packages into a C-style shared library
that can be invoked from other languages, such as Pyhon.

First, you'll need a working Go 1.5 installation. If you haven't already
upgraded, follow the [download and install instructions here]
(https://golang.org/dl).

To use these examples locally, we suggest you clone this repo locally:

```
$ mkdir buildmodeshared
$ git clone https://github.com/jbuberel/buildmodeshared buildmodeshared
```

Once you have the repo cloned, see the [gofromgo](./gofromgo) and 
[gofrompython](./gofrompython) directories for next steps.

## Warning - Linux Only

Keep in mind that this has only been tested on Linux. Certain
features are not available on all Go platforms.