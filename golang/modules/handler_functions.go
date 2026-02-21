package modules

import (
	"fmt"
	"sync"
	"time"
)

func Scrapping() (news []News) {
	start := time.Now()
	var (
		jobs        = make(chan News)
		results     = make(chan News)
		wgWorkers   sync.WaitGroup
		wgProducers sync.WaitGroup
	)

	for x := 1; x < 10; x++ {
		wgWorkers.Go(func() {
			worker(jobs, results)
		})
	}

	SitesToScrapping := 2

	wgProducers.Add(SitesToScrapping)
	go func() { CanalTech(jobs); defer wgProducers.Done() }()
	go func() { TecnoBlog(jobs); defer wgProducers.Done() }()

	go func() {
		wgProducers.Wait()
		close(jobs)
	}()
	go func() {
		wgWorkers.Wait()
		close(results)
	}()

	for result := range results {
		news = append(news, result)
	}

	end := time.Since(start)
	fmt.Println(end)
	return news

}

func worker(jobs, results chan News) {
	for job := range jobs {
		results <- job
	}
}
