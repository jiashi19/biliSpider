import json

import scrapy

from biliSpider.items import ArticleInfoItem


class ArticleinfoSpider(scrapy.Spider):
    name = "articleInfo"
    # allowed_domains = ["bilibili.com"]
    cvid_list = ['25450609']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    # start_urls = ["https://api.bilibili.com/x/article/viewinfo?id=" + cvid for cvid in cvid_list]

    def start_requests(self) :
        for id in self.cvid_list:
            url=f"https://api.bilibili.com/x/article/viewinfo?id={id}"
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body)
        print(result)
        item = ArticleInfoItem()

        item["view"] = result["data"]["stats"]["view"]
        item["favorite"] = result["data"]["stats"]["favorite"]
        item["like"] = result["data"]["stats"]["like"]
        item["dislike"] = result["data"]["stats"]["dislike"]
        item["reply"] = result["data"]["stats"]["reply"]
        item["share"] = result["data"]["stats"]["share"]
        item["coin"] = result["data"]["stats"]["coin"]
        item["dynamic"] = result["data"]["stats"]["dynamic"]  # 动态转发数

        item["title"] = result["data"]["title"]
        item["banner_url"] = result["data"]["banner_url"]
        item["mid"] = result["data"]["mid"]
        item["author_name"] = result["data"]["author_name"]
        item["type"] = result["data"]["type"]
        yield item
