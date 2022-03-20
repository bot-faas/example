import os
import pymongo


def MongoDB():
    client = pymongo.MongoClient(os.environ.get("BOT_FAAS_MONGODB_URI"))
    return client[os.environ.get("BOT_FAAS_MONGODB_DBNAME")]
