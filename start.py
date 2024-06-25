import os
import time

import redis
from utils.videoscrapy import download_video_by_bvid
from biliSpider.settings import VIDEO_ID_SET


def popFromRedis(redis_conn, redis_key):
    # 使用SPOP命令弹出并删除集合中的一个随机id
    popped_bvid = redis_conn.spop(redis_key)
    # 如果集合为空，返回None
    return popped_bvid.decode('utf-8') if popped_bvid else None


if __name__ == '__main__':

    r = redis.Redis(host="localhost", port=6379, db=1)

    mid = input("请输入up主的mid(输入1 直接根据redis中已存在的bvid爬取视频信息):")
    if int(mid)!=1:
        r.delete(VIDEO_ID_SET)  # VIDEO_ID_SET从settings中统一读取，规范性
        os.system(f"scrapy crawl userInfo -a mid={mid}")
        os.system(f"scrapy crawl vids_by_up -a mid={mid}")

    video_cnt = r.scard(VIDEO_ID_SET)
    for i in range(0, video_cnt):
        # 爬取一个视频（下载）及其评论
        bvid = popFromRedis(r, VIDEO_ID_SET)
        os.system(f"scrapy crawl commentInfo -a id={bvid}")
        download_video_by_bvid(bvid)
        #如果不sleep，视频爬取偶尔会出现问题
        time.sleep(20)
