package dnslib

import (
	"C"
	"net"
)

//export ReturnString
func ReturnString(val string) string {
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
