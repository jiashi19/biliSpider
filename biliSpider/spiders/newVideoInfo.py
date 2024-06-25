import random

import redis
import scrapy
import json
from biliSpider.items import VideoItem

'''
使用示例：scrapy crawl newVideoInfo 
'''
class NewVideoSpider(scrapy.Spider):
    name = 'newVideoInfo'
    r = redis.Redis(host="localhost", port=6379, db=1)


    def start_requests(self):
        #各分区tid：电影：23 电视剧：11 美食：211 生活：160 音乐：3 动物：217 时尚：155  
        # ps：vlog版块实际上归在生活区的日常子区中，不再重复爬取。
        tids = [23,11,211,160,3,217,155]  # 目标分区tid列表
        pn = 1  # 页码
        ps = 10  # 每页项数

        for tid in tids:
            # url = f'https://api.bilibili.com/x/web-interface/dynamic/region?pn={pn}&ps={ps}&rid={tid}' 
            url = f'https://api.bilibili.com/x/web-interface/newlist?pn={pn}&ps={ps}&rid={tid}'
            headers = {
                'User-Agent': random.choice(self.settings.get("FAKE_UA_LIST")),
                'Referer': 'https://www.bilibili.com/'
            }
            yield scrapy.Request(url, headers=headers, callback=self.parse, meta={'tid': tid})
    
    def parse(self, response):
        data = json.loads(response.body)
        if 'data' in data and 'archives' in data['data']:
            for archive in data['data']['archives']:
                item = VideoItem()
                item['aid'] = archive['aid']
                item['tid'] = response.meta['tid']  #视频主分区id
                item['sub_tid'] = archive['tid']    #视频子分区id
                item['title'] = archive['title']
                item['description'] = archive['desc']
                item['pubdate'] = archive['pubdate']
                item['view'] = archive['stat']['view']
                item['danmaku'] = archive['stat']['danmaku']
                item['reply'] = archive['stat']['reply']
                item['favorite'] = archive['stat']['favorite']
                item['coin'] = archive['stat']['coin']
                item['share'] = archive['stat']['share']
                item['like'] = archive['stat']['like']
                item['url'] = archive['short_link_v2']
                item['pic'] = archive['pic']
                item['owner_mid'] = archive['owner']['mid']
                item['owner_name'] = archive['owner']['name']
                item['owner_face'] = archive['owner']['face']
                self.r.sadd(self.settings.get("VIDEO_ID_SET"), archive["bvid"])
                yield item
