# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def clean_string(s):
    return s.strip()


def clean_strings(string_array):
    return [s.strip() for s in string_array]


def get_big_image_urls(img_url):
    return img_url.replace("/s/", "/b/").replace("/m/", "/b/")


class OtparserItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=Compose(clean_strings),
        # input_processor=MapCompose(clean_string),
        output_processor=TakeFirst(),
    )
    img_urls = scrapy.Field(input_processor=MapCompose(get_big_image_urls))
    img_info = scrapy.Field()
