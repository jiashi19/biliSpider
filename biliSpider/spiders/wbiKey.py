import json

import scrapy


class WbikeySpider(scrapy.Spider):
    name = "wbiKey"
    start_url= 'https://api.bilibili.com/x/web-interface/nav'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        json_content = response.json()
        img_url = json_content['data']['wbi_img']['img_url']
        sub_url = json_content['data']['wbi_img']['sub_url']
        _img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        _sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]

        wbi_key={
            'img_key': _img_key,
            'sub_key': _sub_key
        }
        with open("biliSpider/wbi_key.json","w",encoding="utf-8") as f:
            json.dump(wbi_key,f,ensure_ascii=False)

