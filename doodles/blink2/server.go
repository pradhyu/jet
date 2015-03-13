package main

import (
	"log"
	"net/http"
)

func main() {
	log.Println("listening on port 8000")
	log.Fatal(http.ListenAndServe(":8000", http.FileServer(http.Dir("."))))
}
