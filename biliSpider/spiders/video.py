import json

import scrapy


class VideoSpider(scrapy.Spider):
    name = "video"
    url="https://api.bilibili.com/x/player/wbi/playurl?bvid={}&cid={}".format("BV1tw4m1i7RQ","1573359593")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def start_requests(self) :
        yield scrapy.Request(url=self.url,headers=self.headers,callback=self.parse)
    def parse(self, response):
        result=json.loads(response.body)
        print(result)
