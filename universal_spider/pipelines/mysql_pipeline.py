import uuid
import pymysql
from scrapy import Item, Spider
from universal_spider.tools.logger import logger


class MySQLPipeline:

    def open_spider(self, spider: Spider):
        # 获取设置
        self.settings = spider.settings
        self.mysql_host = self.settings.get("MYSQL_HOST")
        self.mysql_port = self.settings.get("MYSQL_PORT")
        self.mysql_user = self.settings.get("MYSQL_USER")
        self.mysql_password = self.settings.get("MYSQL_PASSWORD")
        self.mysql_database = self.settings.get("MYSQL_DATABASE")
        self.mysql_table = self.settings.get("MYSQL_TABLE")
        self.mysql_charset = self.settings.get("MYSQL_CHARSET")

        # 连接数据库
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            charset=self.mysql_charset,
        )
        # 链接日志
        logger("MySQLPipeline").info(f"MySQL: {self.mysql_host}:{self.mysql_port}")

        # 判断数据库是否存在，不存在则创建
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {self.mysql_database} DEFAULT CHARACTER SET {self.mysql_charset}"
        )
        self.cursor.execute(f"USE {self.mysql_database}")
        # 判断表是否存在，不存在则创建
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.mysql_table} (id VARCHAR(36) PRIMARY KEY, data TEXT)")

        # 根据设置选择是否清空原数据
        if self.settings.get("MYSQL_CLEAR_DB", False):
            self.cursor.execute(f"TRUNCATE TABLE {self.mysql_table}")
            self.conn.commit()
            logger("MySQLPipeline").info(f"MySQL: {self.mysql_table} is cleared")

        logger("MySQLPipeline").info(f"MySQLPipeline is opened")

    def close_spider(self, spider: Spider):
        self.cursor.close()

    def process_item(self, item: Item, spider: Spider):
        id = uuid.uuid4().hex
        data = dict(item)
        self.cursor.execute(f"INSERT INTO {self.mysql_table} (id, data) VALUES (%s, %s)", (id, str(data)))
        self.conn.commit()

        logger("MySQLPipeline").debug(f"Item: {dict(item)} is inserted into Mysql")
        return item
