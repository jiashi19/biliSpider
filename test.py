import requests as re

if __name__ == '__main__':
    # url="https://api.bilibili.com/x/article/viewinfo?id=25450609"
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    #     "cookie":"SESSDATA=2dd02df1%2C1733119747%2C004dd%2A62CjBrUgO_PKD0hjXSoULcnieaZy8awe7jfsU-uVjhSO9WPRfrKPCvhvCoiQRmJ0ziwd4SVlFCRi1VMC14QUtxZkhWN0dGR3BReU5SWWowY3l3ZHNxZWktTDZRTFZiNV8ydnVrbEVQbXZRYWIxUWNNa0kzVHhUNVdlUUF5cHBoTHpqdjY2UnlIUWd3IIEC"
    # }
    # url1="https://api.bilibili.com/x/web-interface/search/type?keyword=%E8%80%81%E7%95%AA%E8%8C%84&order_sort=0&search_type=bili_user&user_type=0&wts=1717573427&w_rid=02591d7d96261ab99b5f72c4463ef43d"
    # response=re.get(url=url1,headers=headers)
    # print(response.content)
    data = re.get('http://127.0.0.1:5010/get/').json()
    print(data["https"])
