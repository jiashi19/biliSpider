from urllib.parse import urlencode
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

def getMixinKey(orig: str):
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time                                   # 添加 wts 字段
    params = dict(sorted(params.items()))                       # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)                      # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params

def getWbiKeys() -> tuple[str, str]:
    '获取最新的 img_key 和 sub_key'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bilibili.com/'
    }
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key

img_key, sub_key = getWbiKeys()

# 定义目标用户的ID
user_id = '1781681364'

# 定义 API URL 和参数
api_url1 = 'https://api.bilibili.com/x/space/wbi/acc/info'
api_url2 = 'https://api.bilibili.com/x/web-interface/card'
api_url3 = 'https://api.bilibili.com/x/space/wbi/arc/search'
params = {
    'mid': user_id,
}
# 生成 Wbi 签名
wbi_signature = encWbi(params, img_key, sub_key)


# 设置请求头，包括 SESSDATA 和 buvid3
headers1 = {
    'Cookie': 'SESSDATA=fdeed8c6%2C1730295370%2Ca6b13%2A51CjAYMOF09pN8N9wK6SzhQUwF7oIoYcXlJN6-rmDugYqA55aEpTUznqyy-2Ev6MHFIU4SVldYVDNEZmRjVmtpTTQ1b0dLQzl4UFpHTko5R0R6Q3lNby1HRExjel9MWWl0ZTRRTy1tNXcxRHFlRVdaSVhhWlFfWnpsZG5vX1dlTkdYNkE0NDB2bDl3IIEC;buvid3=491B74D7-96C8-1A30-6E5C-DAC6E0F1EA4439320infoc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

headers2 = {
    'Cookie': 'SESSDATA=fdeed8c6%2C1730295370%2Ca6b13%2A51CjAYMOF09pN8N9wK6SzhQUwF7oIoYcXlJN6-rmDugYqA55aEpTUznqyy-2Ev6MHFIU4SVldYVDNEZmRjVmtpTTQ1b0dLQzl4UFpHTko5R0R6Q3lNby1HRExjel9MWWl0ZTRRTy1tNXcxRHFlRVdaSVhhWlFfWnpsZG5vX1dlTkdYNkE0NDB2bDl3IIEC',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
url1 = f"{api_url1}?{urlencode(wbi_signature)}"
url2 = f"{api_url2}?{urlencode(params)}"
url3 = f"{api_url3}?{urlencode(wbi_signature)}"
# 发起请求获取用户信息
response1 = requests.get(url1, headers=headers1)
response2 = requests.get(url2, headers=headers1)
response3 = requests.get(url3, headers=headers1)
user_info1 = response1.json()
user_info2 = response2.json()
user_info3 = response3.json()
# 提取并显示用户信息
if user_info1['code'] == 0:
    data = user_info1['data']
    user_name = data['name']
    user_description = data['sign']
    user_level = data['level']
    print(f"用户名称: {user_name}")
    print(f"用户等级: {user_level}")
    print(f"用户简介: {user_description}")

else:
    print(f"获取用户信息失败: {user_info1['message']}")
# 提取并显示用户信息
if user_info2['code'] == 0:
    data = user_info2['data']
    card = data.get('card', {})
    official_info = card.get('Official', {})
    official_title = official_info.get('title', '无认证信息')
    attention = card.get('attention',{})
    user_count = data['archive_count']
    user_fan = data['follower']
    user_like = data['like_num']


    print(f"认证信息: {official_title}")
    print(f"稿件数: {user_count}")
    print(f"关注数: {attention}")
    print(f"粉丝数: {user_fan}")
    print(f"获赞数: {user_like}")

else:
    print(f"获取用户信息失败: {user_info2['message']}")

# 提取并显示置顶视频
# if user_info3['code'] == 0:
#     data = user_info3['data']
#     vlist = data.get('list', {}).get('vlist', [])
#     for video in vlist:
#         aid = video.get('aid')
#         title = video.get('title')
#         print(f"视频 ID: {aid}, 标题: {title}")
# else:
#     print(f"获取用户视频信息失败: {user_info3['message']}")
#     print(user_info3['code'] )
#     print(url3)