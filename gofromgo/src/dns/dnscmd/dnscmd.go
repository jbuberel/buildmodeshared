package main

import (
	"C"
	"dns/dnslib"
)

func main() {
	fmt.Println(dnslib.ReturnString("golang.org"))
	fmt.Println(dnslib.ReturnInt(42))
}
