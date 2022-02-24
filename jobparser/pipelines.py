# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pprint import pprint

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from pymongo import MongoClient

MONGO_PORT = 27017
MONGO_HOST = "localhost"


class JobParserPipeline:
    def __init__(self):
        # TODO: где закрывается соединение?
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)

    def convert_string_list_to_string(self, string_list):
        return "".join(string_list)

    def process_item(self, item, spider):
        # print("PIPELINE")
        for field in ["salary", "title"]:
            item[field] = self.convert_string_list_to_string(item[field])
        # как удалять ненужные поля
        # del item["field_name"]
        # item.pop("field_name")

        # PREPROCESSING ITEM FOR ... (WRITING TO MONGO etc)
        pprint(item)
        # self-handling _id
        item["_id"] = item["url"]
        # если abc существует в классе Item-а, то все хорошо
        # item['abc'] = 42
        # print()
        db = self.client["vacancies"]
        collection = db[spider.name]
        # UPSERT
        collection.update_one(
            {"_id": item["_id"]},
            {"$set": item},
            upsert=True,
        )
        # with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        #     db = client['vacancies']
        #     collection = db[spider.name]
        #     # collection.insert_one(item)
        #     # UPSERT
        #     collection.update_one(
        #         {"_id": item['_id']},
        #         {"$set": item},
        #         upsert=True,
        #     )
        return item
