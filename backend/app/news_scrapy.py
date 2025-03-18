import scrapy
from scrapy.crawler import CrawlerProcess

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    # Add your URLs here
    start_urls = [
        "https://www.finanzen.net/nachricht/aktien/abfallende-metallteile-neuer-gegenwind-fuer-tesla-aktie-cybertruck-auslieferungen-wohl-vorerst-gestoppt-14321253",
        # Add more URLs here as needed
    ]

    def parse(self, response):
        # Define common paywall indicators
        paywall_keywords = ["subscribe", "premium", "membership", "login to read"]
        page_text = response.text.lower()

        # Skip if paywall detected
        if any(keyword in page_text for keyword in paywall_keywords):
            self.logger.info(f"Skipping paywalled article: {response.url}")
            return

        # Extract content (modify selectors based on site structure)
        title = response.css("h1::text").get()
        paragraphs = response.css("article p::text").getall()
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