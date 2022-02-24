from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hh import HhSpider

# from jobparser.spiders.sj import SuperJobSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # TODO: customize it
    spider_hh_init_kwargs = {"query_text": "python"}
    spider_sj_init_kwargs = {}

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider, **spider_hh_init_kwargs)
    # process.crawl(SuperJobSpider, **spider_sj_init_kwargs)
    process.start()
