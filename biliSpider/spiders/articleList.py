import random

import scrapy
import json

from biliSpider.items import ArticleListItem
from utils.getSignedParam import BiliWbiSigner

'''
使用示例：scrapy crawl articleList -a keyword=KEYWORD
对应pipeline: ArticleListJsonWriterPipeline
'''
class articleListSpider(scrapy.Spider):
    name = "articleList"

    def start_requests(self):
        self.headers = {
            'User-Agent': random.choice(self.settings.get("FAKE_UA_LIST")),
        }
        img_key, sub_key = BiliWbiSigner.getWbiKeys()

        params = {
            'search_type': 'article',
            'keyword': self.keyword,
            'order_sort': '0',
            'user_type': '0',
            'page': '1',
            'pagesize': '36'
        }
        signed_params = BiliWbiSigner.getSignedQuery(params)
        url = f"https://api.bilibili.com/x/web-interface/search/type?{signed_params}"
        # print(url)
        yield scrapy.Request(url, headers=self.headers, callback=self.parse_search_results,
                             meta={'params': params, 'img_key': img_key, 'sub_key': sub_key})

    def parse_search_results(self, response):
        data = json.loads(response.text)
        total_pages = data['data']['numPages']
        all_results = []

        for page_num in range(1, total_pages + 1):
            params = response.meta['params']
            params['page'] = str(page_num)
            signed_params = BiliWbiSigner.getSignedQuery(params)
            url = f"https://api.bilibili.com/x/web-interface/search/type?{signed_params}"
            all_results.append(scrapy.Request(url, headers=self.headers, callback=self.parse_page))
            # print(all_results)
        for request in all_results:
            yield request

    def parse_page(self, response):
        data = json.loads(response.text)
        result=data['data']['result']
        for r in result:
            item=ArticleListItem()
            item["id"]=r["id"]
            item["mid"]=r["mid"]
            item["title"]=r["title"]
            yield item
        # # print(item)
        # yield item
