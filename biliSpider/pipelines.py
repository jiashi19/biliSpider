# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BilispiderPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            self.items = []

    def process_item(self, item, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            items=self.items
            print("本次爬取获取到视频下评论共{}条".format(len(items)))
            with open('result/comments.json', 'w', encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False)
