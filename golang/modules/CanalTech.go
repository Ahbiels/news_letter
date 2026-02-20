package modules

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/gocolly/colly"
)

const url_canal_tech string = "https://canaltech.com.br/ultimas/"

func CanalTech(jobs chan News) {
	allow_domains := strings.Split(url_canal_tech, "/")[2]
	c := colly.NewCollector(
		colly.AllowedDomains(allow_domains),
		colly.MaxDepth(3),
		colly.Async(true),
	)

	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 10})

	NewsCollector := c.Clone()
	NewsCollector.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 10})

	c.OnHTML("div#NewsContainer article", func(h *colly.HTMLElement) {
		// fmt.Println(h.ChildText("a div:nth-of-type(2) span:nth-of-type(1)"))
		time := h.ChildText("a div:nth-of-type(2) span:nth-of-type(1)")
		category := h.ChildText("a div:nth-of-type(2) span:nth-of-type(2)")
		time_unit := strings.Split(time, " ")[1]
		if time_unit == "dias" || time_unit == "dia" || category == "CT Eletro" {
			return
		} else {
			new_url := h.Request.AbsoluteURL(h.ChildAttr("a", "href"))
			ctx := colly.NewContext()
			ctx.Put("category", category)
			NewsCollector.Request("GET", new_url, nil, ctx, nil)
		}
	})

	NewsCollector.OnHTML("main", func(h *colly.HTMLElement) {
		category := h.Request.Ctx.Get("category")
		re_date := regexp.MustCompile(`\d{2}/\d{2}/\d{4}`)
		date := re_date.FindString(h.ChildText("section h1 + p"))
		text := h.ChildText("div#content-news p")
		new := News{
			Title:           h.ChildText("h1"),
			Category:        category,
			TextDescription: text,
			Date:            date,
			Source:          "CanalTech",
		}
		// news = append(news, new)
		jobs <- new
	})

	c.OnHTML("div.pg-article", func(h *colly.HTMLElement) {
		new_url := h.Request.AbsoluteURL(fmt.Sprintf("%vp/%v/", url_canal_tech, 2))
		c.Visit(new_url)
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println(r.URL.String())
	})
	c.Visit(url_canal_tech)
	// SaveLocal(news, "canaltech.json")
	c.Wait()
	NewsCollector.Wait()

}
