package dnslib

import (
	"C"
	"net"
)

//export ReturnString
func ReturnString(val string) *C.char {
	cname, err := net.LookupCNAME(val)
	if err != nil {
		C.CString("Could not find CNAME")
	}
	return C.CString(cname)
}

//export ReturnInt
func ReturnInt(val int) int {
	return val + 3
}
