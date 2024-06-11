import json
from datetime import datetime
import requests
import scrapy

from biliSpider.items import CommentItem


class CommentinfoSpider(scrapy.Spider):

    name = "commentInfo"
    oid_list = ['1255074788']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    start_urls = []
    # start_urls = ["https://api.bilibili.com/x/v2/reply?type=12&oid="+id for id in oid_list]
    for id in oid_list:
        #获取评论总数
        count = requests.get(url="https://api.bilibili.com/x/v2/reply/count?type=1&oid=" + id, headers=headers).json()["data"][
            "count"]
        print("评论总数：",str(count))
        #翻页查询获取所有评论
        for i in range(1, int(count / 20 + 2)):
            new_url = "https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid={}&pn={}".format(id, i)
            start_urls.append(new_url)
        # start_urls.append("https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid={}&pn=1".format(id))


    def parse(self, response):
        result = json.loads(response.body)
        current_time = int(datetime.now().timestamp())
        # for reply in result.get('replies', []):
        for reply in result["data"]["replies"]:
            item = CommentItem()

            # item["parent_user_id"] = reply["member"]["uname"]
            item["platform"] = "bilibili"#
            item["create_date"] = reply["ctime"]#
            item["collect_date"] = current_time#
            item["user_id"] = reply["mid_str"]
            # item["user_id2"] = reply["mid_str"]
            item["user_name"] = reply["member"]["uname"]#
            item["content"] = reply["content"]["message"]#
            item["likes_count"] = reply["like"]#
            item["comments_count"] = reply["rcount"]

            item["is_first_level"] = 1 if reply["parent"] == 0 else 0#
            item["url"] = " TODO"
            item["comment_url"] = " TODO"
            item["user_photo"]=reply["member"]["avatar"]
            item["parent_content"] = "0"
            item["parent_create_date"] = reply["ctime"]
            item["parent_user_id"]=reply["parent"]
            item["description"]=reply["member"]["sign"]

            yield item

            for sub_reply in reply["replies"]:
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
                sub_item["url"] = " TODO"
                sub_item["comment_url"] = " TODO"
                sub_item["user_photo"] = sub_reply["member"]["avatar"]
                sub_item["parent_content"]=item["content"]
                sub_item["parent_create_date"] = item["parent_create_date"]
                sub_item["parent_user_id"] = sub_reply["parent"]
                sub_item["description"] = sub_reply["member"]["sign"]
                yield sub_item




        #pprint(result)
        # with open("comment_dianzan.json", 'w',encoding="utf-8") as json_file:
        #     json.dump(result["data"], json_file,ensure_ascii=False)

