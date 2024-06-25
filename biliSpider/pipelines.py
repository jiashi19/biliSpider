# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import os
import re
from datetime import datetime
from utils.av2bv import av2bv


class DataProcessingPipeline:
    def remove_html_tags(self,text):
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)


    official_verify_map = [" ", "知名UP主", "大V达人", "企业", "组织", "媒体", "政府", "高能主播",
                           "社会知名人士", "社会知名人士"]
    vip_type_map = ["无会员", "月度大会员", '年度及以上大会员']

    def process_item(self, item, spider):
        if spider.name == "commentInfo":
            item["content"] = item["content"].replace("\n", " ")
            item["description"] = item["description"].replace("\n", " ")
        if spider.name == "userInfo":
            item["official_verify"] = self.official_verify_map[item["type"]] + " " + item["official_verify"]
            item["vip"] = self.vip_type_map[int(item["vip"])]
        if spider.name == "newVideoInfo":
            item["description"] = item["description"].replace("\n", " ")

        if spider.name=="articleList":
            item["title"]=self.remove_html_tags(text=item["title"])
        return item


class UserInfoJsonWriterPipeline:

    def process_item(self, item, spider):
        file_path="result/user"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "userInfo":
            if item:
                logging.warning(f"爬取到用户 {item['mid']} 的信息")
                filename = f'{file_path}/user_{item["mid"]}.json'
                item_dict = dict(item)
                with open(filename, 'w', encoding="utf-8") as f:
                    json.dump(item_dict, f, ensure_ascii=False)
            else:
                logging.warning(f'爬取出现错误，未获取到当前用户的信息')
        return item


class CommentJsonWriterPipeline:
    file_path="result/comment"
    def open_spider(self, spider):
        # Check if the spider's name matches the one you want to apply the pipeline to
        if spider.name == "commentInfo":
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
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
                logging.warning(f"爬取获取到oid为 {oid}(bvid={av2bv(int(oid))}) 的评论共 {len(items)} 条")
                if items:
                    filename = f'{self.file_path}/comments_{av2bv(int(oid))}_{(datetime.now().strftime("%Y%m%d_%H%M%S"))}.json'
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(items, f, ensure_ascii=False)
                else:
                    logging.warning(f"爬取出现错误")


class NewVideoJsonWriterPipeline:
    def open_spider(self, spider):
        if spider.name == "newVideoInfo":
            self.video_data = {}
            if not os.path.exists('result/newVideo'):
                os.makedirs('result/newVideo')

            # 映射 tid 到对应的名称
            self.tid_to_name = {
                23: 'movie',
                11: 'teleplay',
                211: 'food',
                160: 'life',
                3: 'music',
                217: 'animal',
                155: 'fashion'
            }

    def close_spider(self, spider):
        if spider.name == "newVideoInfo":
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # 获取当前时间戳

            for tid in self.video_data:
                name = self.tid_to_name.get(tid)
                video_filename = os.path.join('result/newVideo', f'videoDetails_{name}_{timestamp}.json')
                # 将每个分区最新视频保存在对应的json文件中
                with open(video_filename, 'w', encoding='utf-8') as video_file:
                    json.dump(self.video_data[tid], video_file, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        if spider.name == "newVideoInfo":
            tid = item['tid']  # Use 'tid' to distinguish different rids

            if tid not in self.video_data:
                self.video_data[tid] = []

            video_detail = {
                'aid': item['aid'],
                'tid': item['tid'],
                'sub_tid': item['sub_tid'],
                'title': item['title'],
                'description': item['description'],
                'pubdate': item['pubdate'],
                'view': item['view'],
                'danmaku': item['danmaku'],
                'reply': item['reply'],
                'favorite': item['favorite'],
                'coin': item['coin'],
                'share': item['share'],
                'like': item['like'],
                'url': item['url'],
                'pic': item['pic'],
                'owner_mid': item['owner_mid'],
                'owner_name': item['owner_name'],
                'owner_face': item['owner_face']
            }
            self.video_data[tid].append(video_detail)

        return item


class UserListJsonWriterPipeline:
    def open_spider(self, spider):
        if spider.name == "userList":
            self.uname_mid_file = open(f"result/uname_and_mid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w',
                                       encoding='utf-8')

    def close_spider(self, spider):
        if spider.name == "userList":
            self.uname_mid_file.close()

    def process_item(self, item, spider):
        if spider.name == "userList":
            # 写入uname_and_mid.txt
            for user in item['result']:
                self.uname_mid_file.write(f"uname: {user['uname']}, mid: {user['mid']}\n")

        return item


class ArticleListJsonWriterPipeline:
    def open_spider(self, spider):
        if spider.name == "articleList":
            self.items = []

    def close_spider(self, spider):
        if spider.name == "articleList":
            if self.items:
                filename = f'result/article_list_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(filename, 'w', encoding="utf-8") as f:
                    json.dump(self.items, f, ensure_ascii=False)
            else:
                logging.warning(f"爬取出现错误")

    def process_item(self, item, spider):
        if spider.name == "articleList":
            self.items.append(dict(item))

        return item
