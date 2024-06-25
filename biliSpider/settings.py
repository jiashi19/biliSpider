# Scrapy settings for biliSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "biliSpider"

SPIDER_MODULES = ["biliSpider.spiders"]
NEWSPIDER_MODULE = "biliSpider.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "biliSpider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "biliSpider.middlewares.BilispiderSpiderMiddleware": 543,
# }

#scrapy 下载器中间件，在该处启用
# 代理ip中间件未启用，需配合对应代理池程序进行使用（https://github.com/jhao104/proxy_pool）
DOWNLOADER_MIDDLEWARES = {
	# "biliSpider.middlewares.MyproxyMiddleware":544,
    "biliSpider.middlewares.BilispiderDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "biliSpider.pipelines.DataProcessingPipeline": 300,
    "biliSpider.pipelines.CommentJsonWriterPipeline": 302,
    "biliSpider.pipelines.UserInfoJsonWriterPipeline": 303,
    "biliSpider.pipelines.NewVideoJsonWriterPipeline": 304,
    "biliSpider.pipelines.UserListJsonWriterPipeline": 305,
    "biliSpider.pipelines.ArticleListJsonWriterPipeline":306

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
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
# 日志等级,warning级别只会输出警告信息
LOG_LEVEL = 'WARNING'

# redis中存放视频id的set
VIDEO_ID_SET = "video_id_set"
# 自定义的user agent list
FAKE_UA_LIST = [
    "Opera/8.15.(Windows NT 11.0; fi-FI) Presto/2.9.179 Version/11.00",
    "Mozilla/5.0 (Windows; U; Windows 98) AppleWebKit/535.47.2 (KHTML, like Gecko) Version/4.0.1 Safari/535.47.2",
    "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_9_3 rv:4.0; ce-RU) AppleWebKit/535.15.5 (KHTML, like Gecko) Version/4.0.1 Safari/535.15.5",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Win 9x 4.90; Trident/3.0)",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/5.0)"
]
COOKIE_SESSDATA_LIST = [
    "0ce3ab5e%2C1734606013%2C23ff7%2A62CjD0fLF-2EmHT_DIkbQtLE0QOlWOqwtlsMFEiO1uB-p7_ZFv5ovIm0g2SpPwEpiRj6ASVnB6VDJwc3ZRU214Sm5KLTE5Wnc2VUFuZnFiVU9aLWRIVncwYlRweUV0MDM1Yk5iRlNHVVBuWmxONEtSNVF5RUFEclYtUTdJMTVjbFpnQVFpbUVWS1ZRIIEC",
    "93f1d14a%2C1734602191%2C171bc%2A61CjDVD0lRzk4F31NPgU559jGE8GlXg9mazw548jdXYTBqdyEFNgC6uasURCn5wCa6iS0SVlRHbE5lUmtCdElEN3NDaERxZGNtOUp5UWdhVFRaR0Y4WURNZ0JwVFcteDB2aHdVYVFSSlczbU5PUlNLRnlBZkxqQ2syZnlFTzhRQmJVeEFyUWV1cUhRIIEC",
    "8313e71f%2C1733139833%2Cfcd5e%2A61CjA8Tf3I8NnNLmmkBqt8jqydCIszX3u1TPgQFzD69VJlLKXv6IS2L6WU0-ehYlkiBT0SVnBORDRVd0JpTVVNYzVZb3A1MTE2QkVCSV9mMy1hTkh0aTd6OTR5eWM2U3o4ZV83Y2QtQVhnV1gzNUtTSXpVVm0wSHNIY09DS1Jfd0JIQ1VhM2VqSjJnIIEC"
]
