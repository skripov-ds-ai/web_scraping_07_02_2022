# import mypy
# import typing
# from typing import Optional
import scrapy
from scrapy.http import TextResponse

from jobparser.items import JobParserItem

HH_URL_TEMPLATE = (
    "https://omsk.hh.ru/search/vacancy"
    "?search_field=name&search_field=company_name"
    "&search_field=description&text="
)


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    # start_urls = [
    #     'https://omsk.hh.ru/search/vacancy'
    #     '?search_field=name&search_field=company_name'
    #     '&search_field=description&text=python'
    # ]
    field_to_xpath_for_parse = {
        "url": './/a[contains(@data-qa, "-title") and @href]/@href',
        "title": './/a[contains(@data-qa, "-title") and @href]/text()',
    }
    field_to_xpath_for_parse_item = {
        "title": ".//h1//text()",
        "salary": ".//div[@data-qa='vacancy-salary']//text()",
    }
    field_preprocessing_for_parse_item = {
        "title": lambda r: r.xpath(".//h1//text()").getall(),
        "salary": lambda r: r.xpath(
            ".//div[@data-qa='vacancy-salary']//text()"
        ).getall(),
    }

    def __init__(self, query_text: str, **kwargs):
        super().__init__(**kwargs)
        # TODO: какие нюансы возникают с URL и query_text?
        start_url = HH_URL_TEMPLATE + query_text
        self.start_urls = [start_url]

    # def parse(self, response: TextResponse, a: int = 1):
    #     pass

    def parse_item(self, response: TextResponse):
        # print("PARSE_ITEM")
        item = JobParserItem()
        item["url"] = response.url
        # TODO: вернуть xpath
        # for field_name, xpath_string in
        # self.field_to_xpath_for_parse_item.items():
        #     item[field_name] = response.xpath(xpath_string).getall()
        #     в некоторых случаях есть смысл делать .get()
        for field_name, fun in self.field_preprocessing_for_parse_item.items():
            item[field_name] = fun(response)
        # item['abc'] = 42
        # print()
        yield item

    def parse(self, response: TextResponse):
        items = response.xpath(
            '//div[@data-qa="vacancy-serp__results"]'
            '/div[contains(@data-qa, "vacancy-serp__vacancy")]'
        )
        # print()
        for item in items:
            url = item.xpath(self.field_to_xpath_for_parse["url"]).get()
            yield response.follow(url, callback=self.parse_item)
        # все элементы, но проверьте типы
        # items.extract()
        # items.getall()
        # первый элемент
        # items.extract_first()
        # TODO: research parameters!
        # items.get()

        next_url = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

        # walrus operator for Python3.8+
        # if next_url := response.xpath(
        #         "//a[@data-qa='pager-next']/@href"
        # ).get():
        #     yield response.follow(next_url, callback=self.parse)
        # print()
