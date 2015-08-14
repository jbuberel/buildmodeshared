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
