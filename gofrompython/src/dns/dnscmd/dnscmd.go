package main

import (
	"C"
	"dns/dnslib"
)

func main() {
	dnslib.ReturnString("golang.org")

}
