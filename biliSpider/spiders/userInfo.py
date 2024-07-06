import json
import random

import scrapy

from biliSpider.items import UserInfoItem

'''
使用示例：scrapy crawl userInfo -a mid=446430908 、
对应pipeline: UserInfoJsonWriterPipeline
'''
class UserinfoSpider(scrapy.Spider):
    name = "userInfo"


    def start_requests(self):
        # 通过命令行参数-a 传参mid=xxxx
        yield scrapy.Request(url=f'https://api.bilibili.com/x/web-interface/card?mid={self.mid}',headers={"User-Agent":random.choice(self.settings.get("FAKE_UA_LIST"))})

    def parse(self, response):
        result = json.loads(response.body)
        item=UserInfoItem()
        card = result["data"]["card"]
        item["mid"]= card["mid"]
        item["name"]= card["name"]
        item["sex"]= card["sex"]
        item["user_photo"]= card["face"]
        item["fans"]= card["fans"]
        item["attention"]=card["attention"]
        item["sign"]=card["sign"]
        item["level"]=card["level_info"]["current_level"]
        item["type"]=int(card["official_verify"]["type"])
        item["official_verify"]=card['official_verify']["desc"]
        item["vip"]=card["vip"]["type"]
        item["like_num"]=result["data"]["like_num"]
        yield item
