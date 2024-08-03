import random
import time
from scrapy import Request, Spider
from scrapy.crawler import Crawler


class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        # 获取延时范围, 默认为(0, 0)
        delay = crawler.spider.settings.getlist("RANDOM_DELAY_RANGE", (0, 0))
        return cls(delay)

    def process_request(self, request: Request, spider: Spider):
        delay = random.uniform(*self.delay)
        time.sleep(delay)
        # logger("RandomDelayMiddleware").debug(f"Random delay: {delay:.3f}")
        # 不能返回请求, 否则会导致请求被重复处理（即多次随机延时进入死循环）
