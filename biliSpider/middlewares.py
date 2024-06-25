# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import time
import requests
from scrapy import signals, crawler
from biliSpider.settings import COOKIE_SESSDATA_LIST
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

    #统一为请求添加cookies
    def process_request(self, request, spider):
        #从settings中导入
        cookie_list=COOKIE_SESSDATA_LIST
        cookies = {
            'SESSDATA': random.choice(cookie_list),
        }
        request.cookies.update(cookies)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        code=int(json.loads(response.body)["code"])
        if code<0:
            logging.warning(json.loads(response.body))
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

