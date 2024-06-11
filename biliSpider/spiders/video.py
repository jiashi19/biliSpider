import json

import scrapy


class VideoSpider(scrapy.Spider):
    name = "video"
    url="https://api.bilibili.com/x/player/wbi/playurl?bvid={}&cid={}".format("BV1tw4m1i7RQ","1573359593")

    start_urls = []
    start_urls.append(url)
    def parse(self, response):
        result=json.loads(response.body)
        print(result)
