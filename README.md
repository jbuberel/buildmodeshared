# Using Go Shared Libraries

This project demonstrates a few new features that were added or improved 
in the Go 1.5 release:

* **-buildmode=shared** - The ability to create a `.so` file from 
a Go package that can be called by other Go programs.
* **-linkshared** - The ability to compile and link a Go program aginst
previously compiled shared libraries.
* **-buildmode=c-shared** - The ability to create a c-style `.so` file
from a Go package that can be called by other languages.

This work is based on the [Execmodes proposal found here](https://docs.google.com/document/d/1nr-TQHw_er6GOQRsF6T43GGhFDelrAP0NqSS_00RgZQ/edit). Keep in mind that this has only been tested on Linux. Certain
features are not yet available on all Go platforms.

To get started, you'll need a working Go 1.5 installation. If you haven't already
upgraded, follow the [download and install instructions here]
(https://golang.org/dl).

To use these examples locally, I suggest you clone this repo:

```
$ mkdir buildmodeshared
$ git clone https://github.com/jbuberel/buildmodeshared buildmodeshared
```

Once you have the repo cloned, see the [gofromgo](./gofromgo) and 
[gofrompython](./gofrompython) directories for next steps.


*  [Go from Go](./gofromgo) - The ability to compile a Go program that is 
dynamically linked to other Go libraries.
* [Go from Python](./gofrompython) - The ability to compile a set of Go 
packages into a C-style shared library that can be invoked from other 
languages, such as Pyhon.



## Contributing

For details, see [CONTRIBUTING](./CONTRIBUTING.md).

## LICENSE

For details, see [LICENSE](./LICENSE.md).

## NOTE

This is not an official Google project.
