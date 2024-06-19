# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
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


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        cookie_list=[
           "56295b54%2C1734247815%2C4ac44%2A62CjBU7BY-AJz81NP6QL99xVqmDCPlUF2TtPOoTdI8pOu2SzVy8nEXfLvr1L_5SdbnWJkSVnFHMVYwcm1wQkxiX3c5M0VWQTM2Y0lPNlo0MmFyay1MTXI2amhBOVNuaWNWSGNyZDJla2xmQWtKYW1BcmR4aGFhV1puSHl0N2tfb00zeFFkTkVualVnIIEC"
        ]
        # request.headers[
        #     'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        # if spider.name in ["articleInfo", "commentInfo", "vids_by_up"]:
            # request.cookies='SESSDATA=2dd02df1%2C1733119747%2C004dd%2A62CjBrUgO_PKD0hjXSoULcnieaZy8awe7jfsU-uVjhSO9WPRfrKPCvhvCoiQRmJ0ziwd4SVlFCRi1VMC14QUtxZkhWN0dGR3BReU5SWWowY3l3ZHNxZWktTDZRTFZiNV8ydnVrbEVQbXZRYWIxUWNNa0kzVHhUNVdlUUF5cHBoTHpqdjY2UnlIUWd3IIEC'
        cookies = {
            'SESSDATA': random.choice(cookie_list),
        }
        request.cookies.update(cookies)
            #添加代理IP
            # proxy = self.get_proxy()
            # while not proxy:
            #     # 如果没有成功获取代理，则等待一段时间再尝试
            #     time.sleep(1)
            #     proxy = self.get_proxy()
            #
            # request.meta['proxy'] = proxy

        # if spider.name in ["videoaa"]:
        #     print(1)
        #     parsed_url = urllib.parse.urlparse(request.url)
        #     # 获取 URL 中的 GET 参数
        #     q_params = urllib.parse.parse_qs(parsed_url.query)
        #     params = {key: value[0] for key, value in q_params.items()}
        #     # print(params)
        #     if params:
        #         # img_key, sub_key = self.read_wbi_keys("biliSpider/wbi_key.json")
        #         img_key,sub_key=self.getWbiKeys()
        #         # 调用 encWbi 函数计算新的参数
        #         new_params = self.encWbi(params, img_key, sub_key)
        #         # 创建新的 URL 并设置给请求
        #         new_query = urllib.parse.urlencode(new_params)
        #         new_url = request.url.split('?')[0] + '?' + new_query
        #         request = request.replace(url=new_url)
        #         print(new_url)

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        code=int(json.loads(response.body)["code"])
        if code<0:
            logging.warning(json.loads(response.body))
            # proxy_used = request.meta.get('proxy').split("http://")[1]
            # self.delete_proxy(proxy_used)
            return request.copy()
        return response

    def process_exception(self, request, exception, spider):
        # proxy_used = request.meta.get('proxy').split("http://")[1]
        # self.delete_proxy(proxy_used)
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.warning("已访问网页获取数据: %s" % spider.name)




#添加代理IP
class MyproxyMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        proxy = self.get_proxy()
        while not proxy:
            # 如果没有成功获取代理，则等待一段时间再尝试
            time.sleep(1)
            proxy = self.get_proxy()

        request.meta['proxy'] = proxy
        return None


    def get_proxy(self):
        data = requests.get('http://127.0.0.1:5010/get/').json()
        if data['last_status'] and data["https"]:  # 确保代理最近可用且为https
            protocol="https"
            proxy = data['proxy']
            return f'{protocol}://{proxy}'
        return None


    def delete_proxy (self,proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

