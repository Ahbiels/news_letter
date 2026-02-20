package modules

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"
)

func handler_err(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func Scrapping() {
	start := time.Now()
	var (
		news       []News
		jobs       = make(chan News)
		results    = make(chan News)
		wgWorkers sync.WaitGroup
		wgProducers sync.WaitGroup
	)

	for x := 1; x < 10; x++ {
		wgWorkers.Go(func() {
			worker(jobs, results)
		})
	}
	
	SitesToScrapping := 2

	wgProducers.Add(SitesToScrapping)
	go func() { CanalTech(jobs); defer wgProducers.Done()}()
	go func() { TecnoBlog(jobs); defer wgProducers.Done() }()

	go func(){
		wgProducers.Wait()
		close(jobs)
	}()
	go func(){
		wgWorkers.Wait()
		close(results)
	}()

	for result := range results {
		news = append(news, result)
	}

	SaveLocal(news, "filename.json")
	end := time.Since(start)
	fmt.Println(end)

}

func worker(jobs, results chan News) {
	for job := range jobs {
		results <- job
	}
}

func SaveLocal(news []News, filename string) {
	toJSON, err := json.Marshal(news)
	handler_err(err)
	if err := os.WriteFile(filename, toJSON, 0644); err != nil {
		log.Fatal(err)
	}
}
