# -*- coding: utf-8 -*-

import pymongo
from ui.mongoutils.memex_mongo_utils import MemexMongoUtils

class MongoPipeline(object):
    """ Scrapy item pipeline that stores items to MongoDB. """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if hasattr(item, 'mongo_collection'):
            collection_name = item.mongo_collection
            self.db[collection_name].insert(dict(item))
        return item

class SourcePinPipeline(object):

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
        )

    def open_spider(self, spider):
        self.mongo_address, self.mongo_port = self.mongo_uri.split(":")
        self.mmu = MemexMongoUtils(address = self.mongo_address, port = int(self.mongo_port))

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.mmu.insert_url(**dict(item))