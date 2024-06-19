# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
from datetime import datetime


class DataProcessingPipeline:
    official_verify_map = [" ", "知名UP主", "大V达人", "企业", "组织", "媒体", "政府", "高能主播",
                           "社会知名人士", "社会知名人士"]
    vip_type_map = ["无会员", "月度大会员", '年度及以上大会员']

    def process_item(self, item, spider):
        if spider.name == "commentInfo":
            item["content"] = item["content"].replace("\n", " ")
            item["description"] = item["description"].replace("\n", " ")
            # 继续处理其他字段
            return item
        if spider.name == "userInfo":
            item["official_verify"] = self.official_verify_map[item["type"]] + " " + item["official_verify"]
            item["vip"] = self.vip_type_map[int(item["vip"])]
            return item

class UserInfoJsonWriterPipeline:

    def process_item(self, item, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "userInfo":
            if item:
                logging.warning(f"爬取到用户 {item['mid']} 的信息")
                filename = f'result/user_{item["mid"]}.json'
                item_dict = dict(item)
                with open(filename, 'w', encoding="utf-8") as f:
                    json.dump(item_dict, f, ensure_ascii=False)
            else:
                logging.warning(f'爬取出现错误，未获取到当前用户的信息')
        return item



class CommentJsonWriterPipeline:
    def open_spider(self, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            self.items = {}

    def process_item(self, item, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            oid = item['oid']
            if oid:
                if oid not in self.items:
                    self.items[oid] = []
                self.items[oid].append(dict(item))
        return item

    def close_spider(self, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            for oid, items in self.items.items():
                logging.warning(f"爬取获取到oid为 {oid} 的评论共 {len(items)} 条")
                if items:
                    filename = f'result/comments_{oid}_{int(datetime.now().timestamp())}.json'
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(items, f, ensure_ascii=False)
                else:
                    logging.warning(f"爬取出现错误")
