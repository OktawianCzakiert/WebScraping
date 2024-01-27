import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes_hw9_add.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors_hw9_add.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        author_urls = response.xpath('//a[starts-with(@href, "/author/")]/@href').extract()
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        for url in author_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_author)

        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):

        yield {
            "fullname": response.xpath("/html//h3[@class='author-title']/text()").extract_first(),
            "born_date": response.xpath("/html//span[@class='author-born-date']/text()").extract_first(),
            "born_location": response.xpath("/html//span[@class='author-born-location']/text()").extract_first(),
            "description": response.xpath("/html//div[@class='author-description']/text()").extract_first()
        }



process = CrawlerProcess()
process.crawl(QuotesSpider)
process.crawl(AuthorsSpider)
process.start()
