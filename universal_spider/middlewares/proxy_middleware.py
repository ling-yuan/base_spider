from scrapy import Request, Spider

from universal_spider.tools import logger


class ProxyMiddleware(object):

    def process_request(self, request: Request, spider: Spider):
        # 获取设置
        settings = spider.settings
        # 获取请求配置的代理
        proxy: str = request.meta.pop("proxy", "")

        # 根据配置设置代理
        if proxy.lower() == "short":
            # 设置短效代理
            proxy = settings.get("SHORT_PROXY", "")
        elif proxy.lower() == "dynamic":
            # 设置动态代理
            proxy = settings.get("DYNAMIC_PROXY", "")
        elif proxy.lower() == "fixed":
            # 设置固定代理
            proxy = settings.get("FIXED_PROXY", "")
        elif proxy.startswith("http://") or proxy.startswith("https://"):
            # 设置自定义代理
            proxy = proxy
        elif proxy:
            # 代理无效
            logger("ProxyMiddleware").error(f"request_config: proxy configuration are incorrect")
            raise Exception(f"proxy {proxy} is invalid")
        else:
            # 不使用代理
            proxy = None

        # 设置代理
        if proxy:
            request.meta["proxy"] = proxy
