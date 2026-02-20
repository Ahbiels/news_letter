package modules

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/gocolly/colly"
)

const url_tecno_blog string = "https://tecnoblog.net/"

func TecnoBlog(jobs chan News) {
	allow_domains := strings.Split(url_tecno_blog, "/")[2]
	c := colly.NewCollector(
		colly.AllowedDomains(allow_domains),
		colly.MaxDepth(3),
		colly.Async(true),
	)

	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 10})

	NewsCollector := c.Clone()
	NewsCollector.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 10})

	c.OnHTML("div.container div.row article", func(h *colly.HTMLElement) {
		new_url := h.Request.AbsoluteURL(h.ChildAttr("a", "href"))
		ctx := colly.NewContext()
		NewsCollector.Request("GET", new_url, nil, ctx, nil)
	})

	NewsCollector.OnHTML("main", func(h *colly.HTMLElement) {
		category := h.ChildText("article:nth-of-type(1) nav span span:nth-of-type(2) a")
		title := h.ChildText("article:nth-of-type(1) header h1")
		sub_title := h.ChildText("article:nth-of-type(1) header p")
		re_date := regexp.MustCompile(`\d{2}/\d{2}/\d{4}`)
		date := re_date.FindString(h.ChildText("article:nth-of-type(1) header div.time time"))
		text_description := h.ChildText("article:nth-of-type(2) div p")
		text_description = fmt.Sprintf("%v. %v", sub_title, text_description)
		new := News{
			Title:           title,
			Category:        category,
			TextDescription: text_description,
			Date:            date,
			Source:          "TecnoBlog",
		}
		jobs <- new
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println(r.URL.String())
	})

	c.Visit(url_tecno_blog)
	c.Wait()
	NewsCollector.Wait()
}
