# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class BilispiderPipeline:
#     def process_item(self, item, spider):
#         return item

class DataProcessingPipeline:
    def process_item(self, item, spider):
        if spider.name == "commentInfo":
            item["content"]=item["content"].replace("\n"," ")
            item["description"] = item["description"].replace("\n", " ")
            # 继续处理其他字段
            return item
class JsonWriterPipeline:
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
                print(f"爬取获取到oid为 {oid} 的评论共 {len(items)} 条")
                if items:
                    filename = f'result/comments_{oid}_{int(datetime.now().timestamp())}.json'
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(items, f, ensure_ascii=False)
                else:
                    logging.warning(f"爬取出现错误，未获取到oid为 {oid} 的结果")