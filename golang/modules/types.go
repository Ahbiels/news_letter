package modules

type News struct {
	Title           string `json:"title"`
	Category        string `json:"category"`
	TextDescription string `json:"text_description"`
	Date            string `json:"date"`
	Source          string `json:"source"`
}