from asyncio import Event
import asyncio
import logging
from typing import Any, Callable
from scrapy import Request, Spider, signals
from scrapy.crawler import Crawler
from scrapy.http import Response
from scrapy.http.headers import Headers
from scrapy.utils.defer import deferred_from_coro  # 异步转同步
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler

from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler
from scrapy_playwright.handler import _attach_page_event_handlers, DEFAULT_CONTEXT_NAME

from playwright.async_api import Browser, Page, BrowserType
from playwright.async_api._context_manager import PlaywrightContextManager

from twisted.internet.defer import Deferred

from universal_spider.tools import logger
from universal_spider.tools.request import header


class PlaywrightDownloadHandler(ScrapyPlaywrightDownloadHandler):
    """
    若请求meta中包含playwright字段则使用playwright下载
    """

    def __init__(self, crawler: Crawler):
        logging.getLogger("scrapy-playwright").setLevel(logging.WARNING)
        self.settings = crawler.settings
        super().__init__(crawler)
        self.default_options = {
            "headless": True,
            "devtools": False,
            "args": [
                "--disable-extensions",
                "--disable-sync",
                "--disable-setuid-sandbox",
                "--no-first-run",
                "--no-sandbox",
                "--ignore-certificate-errors",
                # 隐藏webdriver特征
                "--disable-blink-features=AutomationControlled",
                # 设置默认user-agent，默认headless模式下user-agent为HeadlessChrome
                f"--user-agent={header(False)}",
            ],
        }

    async def _maybe_launch_browser(self) -> None:
        async with self.browser_launch_lock:
            if not hasattr(self, "browser"):
                logger("PlaywrightDownloadHandler").info("Launching browser %s", self.browser_type.name)
                launch_options = {
                    **self.default_options,
                    **self.config.launch_options,
                }
                self.browser: Browser = await self.browser_type.launch(**launch_options)
                logger("PlaywrightDownloadHandler").info("Browser %s launched", self.browser_type.name)
                self.browser.on("disconnected", self._browser_disconnected_callback)
