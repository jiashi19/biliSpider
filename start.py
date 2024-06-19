import os
import time

import redis
from utils.videoscrapy import download_video_by_bvid


def popFromRedis(redis_conn, redis_key):
    # 使用SPOP命令弹出并删除集合中的一个随机id
    popped_bvid = redis_conn.spop(redis_key)
    # 如果集合为空，返回None
    return popped_bvid.decode('utf-8') if popped_bvid else None


if __name__ == '__main__':

    r = redis.Redis(host="localhost", port=6379, db=1)
    r.delete("video_id_set")
    mid = input("请输入up主的mid:")
    os.system(f"scrapy crawl userInfo -a mid={mid}")
    os.system(f"scrapy crawl vids_by_up -a mid={mid}")
    video_cnt = r.scard("video_id_set")
    print(f"该up主发布了{video_cnt}条视频")
    for i in range(0, video_cnt):
        # 爬取一个视频（下载）及其评论
        bvid = popFromRedis(r, "video_id_set")
        os.system(f"scrapy crawl commentInfo -a id={bvid}")
        download_video_by_bvid(bvid)
        time.sleep(5)
