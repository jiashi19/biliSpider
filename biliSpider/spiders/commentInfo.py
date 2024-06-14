import json
import random
import re
from datetime import datetime
import requests
import scrapy
from biliSpider.items import CommentItem
from utils.av2bv import *
class CommentInfoSpider(scrapy.Spider):
    name = "commentInfo"
    oid_list = ['BV1FJ4m1376p']
    # fake = Faker()
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    # }
    fake_ua_list=[
        "Opera/8.15.(Windows NT 11.0; fi-FI) Presto/2.9.179 Version/11.00",
        "Mozilla/5.0 (Windows; U; Windows 98) AppleWebKit/535.47.2 (KHTML, like Gecko) Version/4.0.1 Safari/535.47.2",
        "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_9_3 rv:4.0; ce-RU) AppleWebKit/535.15.5 (KHTML, like Gecko) Version/4.0.1 Safari/535.15.5",
        "Mozilla/5.0 (compatible; MSIE 5.0; Windows 98; Win 9x 4.90; Trident/3.0)",
        "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/5.0)"
    ]
    # 首先获取总个数
    def start_requests(self):
        for oid in self.oid_list:
            if oid.startswith("BV1"):
                oid=bv2av(oid)
            count_url = f"https://api.bilibili.com/x/v2/reply/count?type=1&oid={oid}"
            yield scrapy.Request(url=count_url, headers={"User-Agent":random.choice(self.fake_ua_list)}, callback=self.parse_comment_count)

    # 然后生成访问页数的request
    def parse_comment_count(self, response):
        oid = re.search(r'oid=([^&]+)', response.url).group(1)
        count = json.loads(response.body)["data"]["count"]
        self.logger.warning(f"评论总数：{count}")

        for i in range(1, int(count / 20 + 2)):
            new_url = f"https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid={oid}&pn={i}"
            yield scrapy.Request(url=new_url, headers={"User-Agent":random.choice(self.fake_ua_list)}, callback=self.parse, meta={'oid': oid})

    # 解析结果，并生成访问二级评论的request
    def parse(self, response):
        result = json.loads(response.body)
        current_time = int(datetime.now().timestamp())
        oid=response.meta["oid"]
        video_url="https://www.bilibili.com/video/"+av2bv(int(oid))
        # for reply in result.get('replies', []):
        for reply in result["data"]["replies"]:
            item = CommentItem()
            comment_url = "https://api.bilibili.com/x/v2/reply/reply?type=1&oid={}&root={}".format(
                oid,
                reply["rpid"])
            # item["parent_user_id"] = reply["member"]["uname"]
            item["platform"] = "bilibili"  #
            item["create_date"] = reply["ctime"]  #
            item["collect_date"] = current_time  #
            item["user_id"] = reply["mid_str"]
            # item["user_id2"] = reply["mid_str"]
            item["user_name"] = reply["member"]["uname"]  #
            item["content"] = reply["content"]["message"]  #
            item["likes_count"] = reply["like"]  #
            item["comments_count"] = reply["rcount"]

            item["is_first_level"] = 1 if reply["parent"] == 0 else 0  #
            item["url"] = video_url
            item["comment_url"] = comment_url
            item["user_photo"] = reply["member"]["avatar"]
            item["parent_content"] = "0"
            item["parent_create_date"] = reply["ctime"]
            item["parent_user_id"] = reply["parent"]
            item["description"] = reply["member"]["sign"]
            item["reqNo"]=reply["rpid"]
            item["oid"]=oid
            yield item
            if int(reply["rcount"]) > 0:
                for i in range(1, int(reply["rcount"] / 20 + 2)):
                    yield scrapy.Request(url=comment_url+f"&pn={i}", headers={"User-Agent":random.choice(self.fake_ua_list)},
                                     callback=self.parse_reply,meta={'oid': oid})

    # 解析二级评论的结果
    def parse_reply(self, response):
        result = json.loads(response.body)
        current_time = int(datetime.now().timestamp())
        parent_content = result["data"]["root"]["content"]["message"]
        parent_create_date = result["data"]["root"]["ctime"]
        video_url="https://www.bilibili.com/video/"+av2bv(int(response.meta["oid"]))
        for sub_reply in result["data"]["replies"]:
            sub_item = CommentItem()
            # item["parent_user_id"] = reply["member"]["uname"]
            sub_item["platform"] = "bilibili"  #
            sub_item["create_date"] = sub_reply["ctime"]  #
            sub_item["collect_date"] = current_time  #
            sub_item["user_id"] = sub_reply["mid_str"]
            # sub_item["user_id2"] = sub_reply["mid_str"]
            sub_item["user_name"] = sub_reply["member"]["uname"]  #
            sub_item["content"] = sub_reply["content"]["message"]  #
            sub_item["likes_count"] = sub_reply["like"]  #
            sub_item["comments_count"] = sub_reply["rcount"]

            sub_item["is_first_level"] = 1 if sub_reply["parent"] == 0 else 0  #
            sub_item["url"] = video_url
            sub_item["comment_url"] = response.url
            sub_item["user_photo"] = sub_reply["member"]["avatar"]
            # sub_item["parent_content"] = response.meta["p_content"]
            sub_item["parent_content"] = parent_content

            # sub_item["parent_create_date"] = response.meta["p_create_date"]
            sub_item["parent_create_date"] = parent_create_date
            sub_item["parent_user_id"] = sub_reply["parent"]
            sub_item["description"] = sub_reply["member"]["sign"]
            sub_item["reqNo"]=sub_reply["rpid"]
            sub_item["oid"]=response.meta["oid"]
            yield sub_item

        # print(response.url + "  " + str(len(result["data"]["replies"])))

        # if len(result["data"]["replies"])>20:
        #     next_url = re.sub(r'pn=\d+', 'pn=' + str(response.meta["pn"] + 1), response.url)
        #     yield scrapy.Request(url=next_url, headers=self.headers, callback=self.parse_reply,
        #                          meta={"p_content": response.meta["p_content"],
        #                                "p_create_date": response.meta["p_create_date"], "pn": response.meta["pn"] + 1})
