package dnslib

import (
	"C"
	"fmt"
	"net"
	"unsafe"
)

//export ReturnString
func ReturnString(val string) unsafe.Pointer {
	cname, err := net.LookupCNAME(val)
	if err != nil {
		msg := "Could not find CNAME"
		// Create a n unsafe pointer, buf, that referes
		buf := C.malloc(C.size_t(len(msg) +1 ))
		s := (*[01 << 30]byte)(buf)[:len(msg)+ 1]
		copy(s[:], msg)
		fmt.Printf("[%v]\n", s )
		return buf
	}

	buf := C.malloc(C.size_t(len(cname) +1 ))
	s := (*[01 << 30]byte)(buf)[:len(cname)+ 1]
	copy(s[:], cname)
	fmt.Printf("[%v]\n", s )

	return buf
}

//export ReturnInt
func ReturnInt(val int) int {
	return val + 3
}
