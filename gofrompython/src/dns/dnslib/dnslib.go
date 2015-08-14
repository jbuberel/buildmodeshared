package dnslib

import (
	"C"
	"net"
	"fmt"
)

//export ReturnString
func ReturnString(val string) string {
	buf := C.malloc(C.size_t(100))
	fmt.Printf("[%t]\n", buf)
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
