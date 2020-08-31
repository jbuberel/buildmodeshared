我是光年实验室高级招聘经理。
我在github上访问了你的开源项目，你的代码超赞。你最近有没有在看工作机会，我们在招软件开发工程师，拉钩和BOSS等招聘网站也发布了相关岗位，有公司和职位的详细信息。
我们公司在杭州，业务主要做流量增长，是很多大型互联网公司的流量顾问。公司弹性工作制，福利齐全，发展潜力大，良好的办公环境和学习氛围。
公司官网是http://www.gnlab.com,公司地址是杭州市西湖区古墩路紫金广场B座，若你感兴趣，欢迎与我联系，
电话是0571-88839161，手机号：18668131388，微信号：echo 'bGhsaGxoMTEyNAo='|base64 -D ,静待佳音。如有打扰，还请见谅，祝生活愉快工作顺利。

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
