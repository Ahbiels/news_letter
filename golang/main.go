package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/Ahbiels/news_letter/modules"
)

func main() {
	http.HandleFunc("/run", func(w http.ResponseWriter, r *http.Request) {
		news := modules.Scrapping()
		w.Header().Set("Content-Type", "application/json")
		err := json.NewEncoder(w).Encode(news)
		if err != nil {
			http.Error(w, "Error to encoder news", http.StatusInternalServerError)
			return
		}
	})
	fmt.Println("Server Begin...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
