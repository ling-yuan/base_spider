from universal_spider.middlewares.user_agent_middleware import UserAgentMiddleWare
from universal_spider.middlewares.proxy_middleware import ProxyMiddleware
from universal_spider.middlewares.redirect_middlewares import CookiesRedirectMiddleware

__all__ = [
    "UserAgentMiddleWare",
    "ProxyMiddleware",
    "CookiesRedirectMiddleware",
]
