from urllib.parse import urljoin, urlparse
from scrapy import Request, Spider
from scrapy.http import Response
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.downloadermiddlewares.redirect import _build_redirect_request
from scrapy.exceptions import IgnoreRequest
from w3lib.url import safe_url_string
from universal_spider.tools import logger


class CookiesRedirectMiddleware(RedirectMiddleware):
    """
    重定向中间件，支持cookies传递
    """

    def __init__(self, settings):
        # 重定向次数
        self.max_redirect_times = settings.getint("REDIRECT_MAX_TIMES")
        # 重定向优先级调整
        self.priority_adjust = settings.getint("REDIRECT_PRIORITY_ADJUST")
        # 允许的通过的响应码
        self.allowed_status_list = settings.getlist("ALLOWED_STATUS_LIST")

    def process_response(self, request: Request, response: Response, spider: Spider):
        # 响应码
        statue_code = response.status
        # 根据请求中设置是否重定向
        if request.meta.get("dont_redirect", False):
            return response

        # 如果响应中不包含重定向信息，则直接返回响应
        if ("Location" not in response.headers) or (statue_code not in (301, 302, 303, 307, 308)):
            return response

        # 获取重定向地址
        location = safe_url_string(response.headers["Location"])
        # 如果重定向地址以//开头，则添加协议（补全）
        if response.headers["Location"].startswith(b"//"):
            # 获取请求的协议
            request_scheme = urlparse(request.url).scheme
            # 拼接重定向地址
            location = request_scheme + "://" + location.lstrip("/")

        # 如果重定向地址不包含协议，则返回响应
        redirect_url = urljoin(request.url, location)
        if urlparse(redirect_url).scheme not in {"http", "https"}:
            return response

        # 生成重定向请求
        redirected = _build_redirect_request(request, url=redirect_url)
        # 返回处理后的重定向请求
        return self._redirect(redirected, request, spider, response)

    def _redirect(self, redirected: Request, request: Request, spider: Spider, response: Response):
        # 响应码
        reason = response.status
        # 最大重定向次数
        ttl = request.meta.setdefault("redirect_ttl", self.max_redirect_times)
        # 当前重定向次数
        redirects = request.meta.get("redirect_times", 1)
        # 如果重定向次数小于最大重定向次数
        if ttl and redirects <= self.max_redirect_times:
            # 设置当前重定向次数
            redirected.meta["redirect_times"] = redirects
            # redirected.meta["redirect_ttl"] = ttl - 1
            # 重定向url
            redirected.meta["redirect_urls"] = request.meta.get("redirect_urls", []) + [request.url]
            # 重定向响应码
            redirected.meta["redirect_reasons"] = request.meta.get("redirect_reasons", []) + [reason]
            # 设置过滤
            redirected.dont_filter = request.dont_filter
            # 设置重定向优先级
            redirected.priority = request.priority + self.priority_adjust
            # 日志
            logger("CookiesRedirectMiddleware").debug(f"Redirecting {reason} to {redirected} from {request}")
            # 移除请求头中的键
            purged_headers = ("Content-Length", "Content-Type", "Transfer-Encoding")
            for header in purged_headers:
                redirected.headers.pop(header, None)

            # 获取当前响应的cookies
            cookies = {}
            if origin_cookies := redirected.headers.get("Cookie"):
                cookies_list = origin_cookies.decode().split(";")
                for cookie in cookies_list:
                    key, value = cookie.split("=")[0:2]
                    cookies[key] = value

            # 获取响应中设置的cookies
            if set_cookies := response.headers.getlist("Set-Cookie"):
                cookies_list = [cookie.decode().split(";")[0] for cookie in set_cookies]
                for cookie in cookies_list:
                    key, value = cookie.split("=")[0:2]
                    cookies[key] = value

            # 设置重定向请求的cookies
            redirected.headers["Cookie"] = "; ".join([f"{key}={value}" for key, value in cookies.items()])
            return redirected

        # 重定向次数达到最大，抛出异常
        logger("CookiesRedirectMiddleware").debug(f"ignore {request}: max redirections reached")
        raise IgnoreRequest("max redirections reached")
