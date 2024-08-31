import random
import time
from scrapy import Request, Spider
from scrapy.crawler import Crawler

from universal_spider.tools.logger import logger


class RandomDelayMiddleware(object):
    def __init__(self, use: bool, delay: tuple):
        self.use = use
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        # 获取是否使用随机延时, 默认为False
        use_random_delay = crawler.spider.settings.getbool("RANDOM_DELAY", False)
        # 获取延时范围, 默认为(0, 0)
        delay = crawler.spider.settings.getlist("RANDOM_DELAY_RANGE", (0, 0))
        return cls(use_random_delay, delay)

    def process_request(self, request: Request, spider: Spider):
        if self.use:
            delay = random.uniform(*self.delay)
            # logger("RandomDelayMiddleware").debug(f"Random delay: {delay:.3f}")
            time.sleep(delay)
        # 不能返回请求, 否则会导致请求被重复处理（即多次随机延时进入死循环）
