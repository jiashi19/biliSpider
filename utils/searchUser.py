import requests
from urllib.parse import urlencode
from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests
import json



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

    print(params)

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



def get_initial_cookies():
    # 发送 GET 请求到 https://bilibili.com 以获取初始 cookies
    response = requests.get('https://bilibili.com')
    # 返回 cookies
    print(response.cookies)
    return response.cookies

def search_bilibili(img_key, sub_key, headers):
    # 定义请求的基础 URL
    base_url = 'https://api.bilibili.com/x/web-interface/search/type'

    # 定义查询参数
    params = {
        'search_type': 'bili_user',
        'keyword': '老番茄',
        'order_sort': '0',
        'user_type': '0',
        'page':'1',
        'pagesize':'36'
    }


    # 签名处理参数
    signed_params = encWbi(params, img_key, sub_key)

    # 构建完整的 URL
    url = f"{base_url}?{urlencode(signed_params)}"
    #print(url)
    # 发送搜索请求
    response = requests.get(url,headers=headers)

    response.raise_for_status()
    json_response = response.json()
    # 提取总页数
    total_pages = json_response['data']['numPages']
    print(total_pages)
    # 循环爬取多页数据
    all_results = []
    for page_num in range(1, total_pages + 1):
        # 更新参数中的页数
        params['page'] = str(page_num)

        # 签名处理参数
        signed_params = encWbi(params, img_key, sub_key)

        # 构建完整的 URL
        url = f"{base_url}?{urlencode(signed_params)}"
        print(url)

        # 发送搜索请求
        response = requests.get(url, headers=headers)


        # 检查响应状态码并返回结果
        if response.status_code == 200:
            json_response = response.json()
            all_results.extend(json_response['data']['result'])
        else:
            return f"请求失败，状态码: {response.status_code}"
    #print(all_results)
    return all_results

    
def extract_uname_and_mid(file_path):
    # 从文件中读取JSON数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 uname 和 mid
    result = []
    for user in data:
        uname = user.get("uname")
        mid = user.get("mid")
        result.append({"uname": uname, "mid": mid})

    return result

def save_uname_and_mid(data, output_file):

    #将 uname 和 mid 保存到指定文件中。
    with open(output_file, 'w', encoding='utf-8') as file:
        for user in data:
            file.write(f"uname: {user['uname']}, mid: {user['mid']}\n")


def main():
    # 获取初始 cookies
    cookies = get_initial_cookies()

    # 获取 img_key 和 sub_key
    img_key, sub_key = getWbiKeys()
    print(img_key,sub_key)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        "cookie":"SESSDATA=2dd02df1%2C1733119747%2C004dd%2A62CjBrUgO_PKD0hjXSoULcnieaZy8awe7jfsU-uVjhSO9WPRfrKPCvhvCoiQRmJ0ziwd4SVlFCRi1VMC14QUtxZkhWN0dGR3BReU5SWWowY3l3ZHNxZWktTDZRTFZiNV8ydnVrbEVQbXZRYWIxUWNNa0kzVHhUNVdlUUF5cHBoTHpqdjY2UnlIUWd3IIEC"
    }
    # 执行搜索请求
    result = search_bilibili(img_key, sub_key,headers)
    # 打印结果
    #print(result)
    #将结果写入文件
    filepath = 'all_result1.txt'  #包含全部数据的文件
    output_file = 'uname_and_mid.txt'  #只包含uname和mid的文件
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, ensure_ascii=False, indent=4))

     # 提取 uname和mid 字段
    unames_and_mid = extract_uname_and_mid(filepath)
    #print(unames_and_mid)

    save_uname_and_mid(unames_and_mid, output_file)

if __name__ == "__main__":
    main()