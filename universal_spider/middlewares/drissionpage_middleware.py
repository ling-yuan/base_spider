import asyncio
import logging
from DrissionPage import ChromiumOptions, ChromiumPage
from DrissionPage._pages.chromium_tab import ChromiumTab
from scrapy import Request, Spider, signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.http import Response

from universal_spider.tools import logger


class DrissionPageMiddleware(object):

    def __init__(self, settings: Settings):
        # 设置日志不显示mongodb的日志
        logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
        self.max_page = settings.getint("MAX_PAGE", 5)
        self.page: ChromiumPage = None
        self.option = ChromiumOptions()

        # 设置默认选项
        # self.option.incognito()  # 匿名模式
        # self.option.set_argument('--no-sandbox')  # 无沙盒模式
        self.option.set_argument("--window-size", "1920,1080")
        if settings.getbool("HEADLESS", True):
            self.option.headless()

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    @property
    def all_tabs(self):
        if self.page is not None:
            return self.page.get_tabs()
        else:
            raise Exception("Browser is not open")

    @property
    def tabs_num(self):
        return len(self.all_tabs) - 1

    def open_browser(self):
        logger("DrissionPageMiddleware").info("Open browser")
        self.page = ChromiumPage(self.option)
        self.page.get("about:blank")

    def create_tab(self, url):
        tab: ChromiumTab = self.page.new_tab(url)
        return tab

    async def process_request(self, request: Request, spider: Spider):
        if request.meta.pop("drission", False):
            if self.page is None:
                self.open_browser()
            while self.tabs_num >= self.max_page:
                logger("DrissionPageMiddleware").info("Sleep 0.5s")
                await asyncio.sleep(1)
            # 构造Response
            tab: ChromiumTab = self.create_tab(request.url)
            request.meta["page"] = tab
            response = Response(
                url=tab.url,
                status=200,
                body=tab.html.encode(),
                request=request,
            )
            return response

    def spider_closed(self, spider: Spider):
        try:
            logger("DrissionPageMiddleware").info("Close browser")
            self.page.quit()
        except:
            logger("DrissionPageMiddleware").info("Browser is not open")
            pass
