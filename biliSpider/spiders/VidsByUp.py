import scrapy
from utils.getSignedParam import BiliWbiSigner
import redis

class VidsByUp(scrapy.Spider):
    name = "vids_by_up"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始的第一页
        self.video_id_set = None
        self.pages = 1
        # self.mid = input('输入up主的mid: ') 更改为通过命令行参数-a 传递
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36",
            "Referer": f"https://space.bilibili.com/{self.mid}/video",
        }
        # self.cookies = {
        #     "SESSDATA": "974414e9%2C1733718003%2C1ad41%2A61CjDaI2fHqs7mI2jm86jKDOwo0mt3gACtcuLVdUalMZkkMyWh3i5sCJrWbgy-jHXq8qISVkNEN1JFTnFfbHdsZUwtV0lrcVlPRXpoQ0lIZXRKUTh2bTdpWkJkUXRsM3Vqdy1ZdnB3eUxybHJHa21sVl9peEVpNnJpSGxsTkZ1NHQ4WjNrbXdOX0JnIIEC",
        # }
#        self.video_ids = []
        self.signer = BiliWbiSigner()
        # 连接redis
        self.r=redis.Redis(host="localhost",port=6379,db=1)


    def start_requests(self):
        self.video_id_set=self.settings.get("VIDEO_ID_SET")
        # url = "https://api.bilibili.com/x/space/wbi/arc/search?mid={}&pn={}".format(self.mid, 1)
        url = "https://api.bilibili.com/x/space/wbi/arc/search?{}".format(
            self.signer.getSignedQuery({'mid': self.mid, 'pn': 1})
        )
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_page_num,
            # cookies=self.cookies
        )

    def parse_page_num(self, response):
        json_response = response.json()
        #        total_count = sum(item['count'] for item in json_response['data']['list']['tlist'].values())
        total_count = json_response["data"]["page"]["count"]
        # 获取并存储第一页的视频id
        v_list = json_response['data']['list']['vlist']
        for item in v_list:
            self.r.sadd(self.video_id_set, item['bvid'])
        # self.video_ids.extend([item['bvid'] for item in v_list])

        # 总页码数
        self.pages = int(total_count / 30) + 1 if total_count % 30 != 0 else int(total_count / 30)

        if self.pages > 1:
            for i in range(2, self.pages + 1):
                yield scrapy.Request(
                    url="https://api.bilibili.com/x/space/wbi/arc/search?{}".format(
                        self.signer.getSignedQuery({'mid': self.mid, 'pn': i})
                    ),
                    headers=self.headers,
                    callback=self.parse_video_ids
                )

    def parse_video_ids(self, response):
        json_response = response.json()
        v_list = json_response['data']['list']['vlist']
        for item in v_list:
            self.r.sadd(self.video_id_set, item['bvid'])
        # self.video_ids.extend([item['bvid'] for item in v_list])

        # if len(self.video_ids) > (self.pages - 1) * 30:
        #     self.logger.warning(f"All Video IDs: {self.video_ids}")
