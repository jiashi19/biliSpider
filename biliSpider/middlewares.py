# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BilispiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("爬虫启动: %s" % spider.name)


class BilispiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # request.headers[
        #     'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        if spider.name in ["articleInfo", "commentInfo", "video"]:
            # request.cookies='SESSDATA=2dd02df1%2C1733119747%2C004dd%2A62CjBrUgO_PKD0hjXSoULcnieaZy8awe7jfsU-uVjhSO9WPRfrKPCvhvCoiQRmJ0ziwd4SVlFCRi1VMC14QUtxZkhWN0dGR3BReU5SWWowY3l3ZHNxZWktTDZRTFZiNV8ydnVrbEVQbXZRYWIxUWNNa0kzVHhUNVdlUUF5cHBoTHpqdjY2UnlIUWd3IIEC'
            cookies = {
                'SESSDATA': '43584b8a%2C1733647539%2C9dbf7%2A62CjA7Tc35-CRnTE06LfRxW-oB5xDElZV2Fp-0VEd0RbaWJh38zy4Nx4u5lNAfUe8EtwASVnQzOW5fTGJXUDBtUnhSZ0NobVQ3Uk5lQnZYMGRvc1h4NDdKMDdCbURoa2ZNMFNGNjBuZUxfLW5VUWltdFF5WFFQckdScTVvUjZyVzJxV2pKWVdfT3R3IIEC',
            }
            request.cookies.update(cookies)
        if spider.name in ["video"]:
            print(1)
            parsed_url = urllib.parse.urlparse(request.url)
            # 获取 URL 中的 GET 参数
            q_params = urllib.parse.parse_qs(parsed_url.query)
            params = {key: value[0] for key, value in q_params.items()}
            print(params)
            if params:
                img_key, sub_key = self.getWbiKeys()
                # 调用 encWbi 函数计算新的参数
                new_params = self.encWbi(params, img_key, sub_key)
                # 创建新的 URL 并设置给请求
                new_query = urllib.parse.urlencode(new_params)
                new_url = request.url.split('?')[0] + '?' + new_query
                request = request.replace(url=new_url)
                print(new_url)

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if spider.name=="commentInfo":
            print(request.url)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.warning("已访问网页获取原始数据: %s" % spider.name)

    # 鉴权函数
    mixinKeyEncTab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
                      "Safari/537.36",
    }

    def getMixinKey(self, orig: str):
        # 对 imgKey 和 subKey 进行字符顺序打乱编码
        return reduce(lambda s, _i: s + orig[_i], self.mixinKeyEncTab, '')[:32]

    def encWbi(self, params: dict, _img_key: str, _sub_key: str):
        # 为请求参数进行 wbi 签名
        mixin_key = self.getMixinKey(_img_key + _sub_key)
        curr_time = round(time.time())
        params['wts'] = curr_time  # 添加 wts 字段
        params = dict(sorted(params.items()))  # 按照 key 重排参数
        # 过滤 value 中的 "!'()*" 字符
        params = {
            k: ''.join(filter(lambda _chr: _chr not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        _query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((_query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        params['w_rid'] = wbi_sign
        return params

    def getWbiKeys(self) -> tuple[str, str]:
        # 获取最新的 img_key 和 sub_key
        resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=self.headers)
        resp.raise_for_status()
        json_content = resp.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        _img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        _sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return _img_key, _sub_key
