from scrapy import Request, Spider

from universal_spider.tools import header


class UserAgentMiddleWare(object):
    """
    利用fake_useragent,随机生成User-Agent
    """

    def process_request(self, request: Request, spider: Spider):
        # 如果请求中有User-Agent，则不设置
        if request.headers.get("User-Agent"):
            return
        # random.choice随机的选取列表中的一个数据
        agent = header(False)
        # request.headers，设置了请求头
        request.headers["User-Agent"] = agent
