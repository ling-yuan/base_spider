from universal_spider.middlewares.user_agent_middleware import UserAgentMiddleWare
from universal_spider.middlewares.proxy_middleware import ProxyMiddleware
from universal_spider.middlewares.redirect_middlewares import CookiesRedirectMiddleware
from universal_spider.middlewares.random_delay_middleware import RandomDelayMiddleware

__all__ = [
    "UserAgentMiddleWare",  # 随机User-Agent
    "ProxyMiddleware",  # 代理
    "CookiesRedirectMiddleware",  # 带cookies重定向
    "RandomDelayMiddleware",  # 随机延时
]
