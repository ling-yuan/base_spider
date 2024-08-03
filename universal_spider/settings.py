BOT_NAME = "universal_spider"

# 指定Scrapy项目中的爬虫模块
SPIDER_MODULES = ["universal_spider.spiders"]
NEWSPIDER_MODULE = "universal_spider.spiders"

# 机器人协议
ROBOTSTXT_OBEY = False

# Scrapy执行的最大并发请求数 (默认值: 16)
CONCURRENT_REQUESTS = 8

# 下载延迟
# DOWNLOAD_DELAY = 3
# 下载延迟设置将仅遵循以下之一:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# 禁用cookie (默认启用)
COOKIES_ENABLED = False

# 禁用Telnet控制台 (默认启用)
# TELNETCONSOLE_ENABLED = False

# 覆盖默认请求头
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",  # 部分网站根据这个字段返回不同的内容
    "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Accept-Encoding": "gzip, deflate",
    "cache-control": "no-cache",
}

# 爬虫中间件 小->大
# SPIDER_MIDDLEWARES = {
#    "universal_spider.middlewares.UniversalSpiderSpiderMiddleware": 543,
# }

# 参数
## 重定向
REDIRECT_ENABLED = False
REDIRECT_MAX_TIMES = 5
## 响应正常码
ALLOWED_STATUS_LIST = []
## 随机延时
### 开启状态
RANDOM_DELAY = False
### 范围
RANDOM_DELAY_RANGE = (0, 3)

# 额外所需参数 (中间件，扩展，管道)
from universal_spider.Info import *

# 下载中间件 小->大
DOWNLOADER_MIDDLEWARES = {
    # "universal_spider.middlewares.UniversalSpiderDownloaderMiddleware": 543,
    # process request
    "universal_spider.middlewares.UserAgentMiddleWare": 100,
    "universal_spider.middlewares.ProxyMiddleware": 200,
    "universal_spider.middlewares.RandomDelayMiddleware": 300,
    # process response
    # "universal_spider.middlewares.StatisticsMiddleware": 1,
    "universal_spider.middlewares.CookiesRedirectMiddleware": 600,
}

# 扩展
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# 管道
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # "universal_spider.pipelines.UniversalSpiderPipeline": 300,
    "universal_spider.pipelines.MongoPipeline": 100,
    "universal_spider.pipelines.MySQLPipeline": 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True

# 初始下载延迟
# AUTOTHROTTLE_START_DELAY = 5

# 在高延迟情况下设置的最大下载延迟
# AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# 启用和配置HTTP缓存 (默认情况下禁用)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 命令模块
COMMANDS_MODULE = "universal_spider.commands"
