import logging
from scrapy import Item, Spider
from pymongo import MongoClient
from universal_spider.tools.logger import logger


class MongoPipeline:

    def open_spider(self, spider: Spider):
        # 设置日志不显示mongodb的日志
        logging.getLogger("pymongo").setLevel(logging.WARNING)
        # 获取设置
        self.settings = spider.settings
        # 获取MongoDB的信息并连接
        self.mongo_uri = self.settings.get("MONGO_URI")
        self.connection = MongoClient(self.mongo_uri)
        self.db = self.connection[self.settings.get("MONGO_DB_NAME")]
        self.collection = self.db[self.settings.get("MONGO_COLLECTION_NAME")]
        logger("MongoPipeline").info(f"MongoDB: {self.mongo_uri}")

        # 根据设置选择是否清空原数据
        if self.settings.get("MONGO_CLEAR_DB", False):
            self.collection.drop()
            logger("MongoPipeline").info(f"MongoDB collection {self.settings.get('MONGO_COLLECTION_NAME')} cleared")

        logger("MongoPipeline").info(f"MongoPipeline is opened")

    def close_spider(self, spider: Spider):
        self.connection.close()
        logger("MongoPipeline").info(f"MongoPipeline is closed")

    def process_item(self, item: Item, spider: Spider):
        # 插入数据，不显示日志
        self.collection.insert_one(dict(item))
        item_info = str(dict(item))
        item_info = item_info[:100] + "..." if len(item_info) > 100 else item_info
        logger("MongoPipeline").debug(f"Item: {item_info} is inserted into MongoDB")
        return item
