from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
                  "Safari/537.36",
}


def getMixinKey(orig: str):
    # 对 imgKey 和 subKey 进行字符顺序打乱编码
    return reduce(lambda s, _i: s + orig[_i], mixinKeyEncTab, '')[:32]


def encWbi(params: dict, _img_key: str, _sub_key: str):
    # 为请求参数进行 wbi 签名
    mixin_key = getMixinKey(_img_key + _sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: ''.join(filter(lambda _chr: _chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    _query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((_query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    # 获取最新的 img_key 和 sub_key
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    _img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    _sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return _img_key, _sub_key


img_key, sub_key = getWbiKeys()

# 获取cookie
cookies = {
    "buvid4": "",
}
preResponse = requests.get("https://api.bilibili.com/x/frontend/finger/spi", headers=headers)
preData = preResponse.json()
cookies['buvid4'] = preData['data']['b_4']

keyword = input("文章关键字：")
pageNum = int(input("文章页数（默认一页20篇文章）："))
articles = []

for i in range(pageNum):
    signed_params = encWbi(
        params={
            "search_type": "article",
            "page": i + 1,
            "keyword": keyword,
        },
        _img_key=img_key,
        _sub_key=sub_key
    )
    query = urllib.parse.urlencode(signed_params)
    url = "https://api.bilibili.com/x/web-interface/wbi/search/type?{}".format(query)
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        data = response.json()['data']['result']
        articles.extend(data)

for article in articles:
    print(article)
