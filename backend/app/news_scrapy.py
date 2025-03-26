import scrapy
from scrapy.crawler import CrawlerProcess

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    # Add your URLs here
    start_urls = [
        "https://www.auswaertiges-amt.de/en/aussenpolitik/themen/klimaenergie/petersberg-climate-dialogue-2707198",
        # Add more URLs here as needed
    ]

    def parse(self, response):

        # Extract content (modify selectors based on site structure)
        title = response.css("h1::text").get()
        paragraphs = response.css("p::text").getall()
        article_text = " ".join(paragraphs)

        yield {
            "url": response.url,
            "title": title,
            "text": article_text
        }

process = CrawlerProcess(settings={
    "FEEDS": {"articles.json": {"format": "json"}}
})
process.crawl(NewsSpider)
process.start()