package main

import (
	"C"
	_ "dns/dnslib"
)

// main in this case is a no-op. It will never be called, but it is
// required in order for the symbols to be exported.
func main() {
}
