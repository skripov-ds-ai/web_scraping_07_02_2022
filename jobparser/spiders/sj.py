import scrapy


class SuperJobSpider(scrapy.Spider):
    name = "superjob"
    allowed_domains = ["superjob.ru"]
    start_urls = ["http://superjob.ru/"]

    def parse(self, response):
        pass
