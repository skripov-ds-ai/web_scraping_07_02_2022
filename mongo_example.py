from pprint import pprint

# pip install bson pymongo
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, MongoClient

print()


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "posts"
MONGO_COLLECTION = "news_posts"
MONGO_COLLECTION_NEW = "social_network_posts"
# d = dict(a=1)
# something like
# URI = "mongodb://localhost:port@username:password"

# client = MongoClient(MONGO_HOST, MONGO_PORT)
# # ...
# client.close()
#
# with MongoClient(MONGO_HOST, MONGO_PORT) as client:
#     pass


def print_mongo_docs(cursor):
    for doc in cursor:
        pprint(doc)


# CRUD
# 1. Create - INSERT?
# 2. Read - SELECT?
# 3. Update - UPDATE?
# 4. Delete - DELETE?

with MongoClient(MONGO_HOST, MONGO_PORT) as client:
    # posts
    # db = client.posts
    # db = client['posts']
    db = client[MONGO_DB]

    # collection = db.social_network_posts
    # MONGO_COLLECTION_NEW
    collection = db[MONGO_COLLECTION_NEW]

    # 4. Delete for collection/database
    # delete all documents of current collection
    # collection.drop()
    # delete collection with name
    # db.drop_collection(MONGO_COLLECTION_NEW)

    # 1. Create
    post_doc = {
        "title": "Something with Biden",
        "rating": 70,
        "count_of_comments": 4,
    }
    post_doc_0 = {
        "title": "Something with Biden",
        "rating": -1,
        "count_of_comments": 4,
    }
    post_doc_1 = {"title": "Trump elections"}
    # collection.insert_one(post_doc_0)
    # collection.insert_one(post_doc)
    # collection.insert_many([post_doc, post_doc_1])
    # print()

    # 2. Read
    # cursor = collection.find()
    # cursor = collection.find({})
    # exact matching
    # cursor = collection.find({
    #     # "title": "Trump elections",
    #     "title": "Something with Biden",
    # })
    # cursor = collection.find({
    #     # "title": "Trump elections",
    #     "title": "Something with Biden",
    # }).limit(3)
    # cursor = collection.find({
    #     # "title": "Trump elections",
    #     "title": "Something with Biden",
    # }).sort("rating", direction=ASCENDING).limit(3)
    # multiple key sorting
    cursor = collection.find(
        {
            # "title": "Trump elections",
            "title": "Something with Biden",
        }
    ).sort(
        [
            ("rating", ASCENDING),
            ("count_of_comments", DESCENDING),
        ]
    )
    # cursor = collection.find({
    #     "title": {"$eq": "Trump elections"}
    # })
    # cursor = collection.find({
    #     "title": {"$ne": "Trump elections"}
    # })
    # $gt - > ; $gte - >= ; $lt - < ; $lte - <=
    # cursor = collection.find({
    #     "rating": {"$gt": 0},
    #     "count_of_comments": 4,
    # })
    # $and ; $or ; $not - logic operations
    # cursor = collection.find({
    #     # $and
    #     "$or": [
    #         {
    #             "rating": {"$lt": 0}
    #         },
    #         {
    #             "rating": {"$eq": 0}
    #         }
    #     ]
    # })
    # $not - https://docs.mongodb.com/manual/reference/operator/query/not/
    # $nor - https://docs.mongodb.com/manual/reference/operator/query/nor/
    cursor = collection.find({"rating": {"$not": {"$lt": 0}}})
    # print_mongo_docs(cursor)
    # $in
    cursor = collection.find(
        {
            # filter!
            "rating": {"$in": [-1, 1]}
        }
    )
    # regex
    # https://docs.mongodb.com/manual/reference/operator/query/regex/
    # print("=" * 15)
    # print_mongo_docs(cursor)
    # если данных немного, то можно считать их все в RAM
    # retrieved_data = list(cursor)

    # 3. Update
    collection.update_one(
        {"_id": ObjectId("620a8bb4e4dafa81d06d8ab1")},
        {
            "$set": {
                "title": "not Biden",
                "rating_1": 90,
            },
            "$unset": {
                "rating": None,
            },
        },
    )
    # title1 -> title1_1 ; title2 -> title2_1 - not this way
    # title1 -> titleX ; title2 -> titleX
    # collection.update_many(
    #     {
    #         # "rating": 70,
    #         "rating": 71,
    #     },
    #     {
    #         # "$inc": {"rating": 1},
    #         "$inc": {"rating": -1},
    #     }
    # )
    #
    # UPSERT
    collection.update_one(
        {
            "rating": 60,
        },
        {
            "$set": {
                "title": "no",
                "rating_1": 99,
            },
        },
        upsert=True,
    )
    collection.replace_one(
        {
            "rating": 60,
        },
        {
            "title": "no",
            "rating_1": 99,
        },
    )

    cursor = collection.find(
        {
            "rating": 60,
        },
    )
    print_mongo_docs(cursor)

    # 4. Delete
    # ?
    # collection.delete_one({})
    # collection.delete_many()
    #
    collection.delete_one(
        {
            "title": "no",
            "rating_1": 99,
        }
    )
    collection.delete_many(
        {
            "rating": {"$gt": 0},
        }
    )
