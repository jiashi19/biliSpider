from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests


class BiliWbiSigner:
    mixinKeyEncTab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0.0.0"
                      "Safari/537.36",
    }

    @staticmethod
    def getMixinKey(orig: str):
        return reduce(lambda s, _i: s + orig[_i], BiliWbiSigner.mixinKeyEncTab, '')[:32]

    @staticmethod
    def encWbi(params: dict, _img_key: str, _sub_key: str):
        mixin_key = BiliWbiSigner.getMixinKey(_img_key + _sub_key)
        curr_time = round(time.time())
        params['wts'] = curr_time
        params = dict(sorted(params.items()))
        params = {
            k: ''.join(filter(lambda _chr: _chr not in "!'()*", str(v)))
            for k, v in params.items()
        }
        _query = urllib.parse.urlencode(params)
        wbi_sign = md5((_query + mixin_key).encode()).hexdigest()
        params['w_rid'] = wbi_sign
        return params

    @staticmethod
    def getWbiKeys() -> tuple[str, str]:
        resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=BiliWbiSigner.headers)
        resp.raise_for_status()
        json_content = resp.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        _img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        _sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return _img_key, _sub_key

    @classmethod
    def getSignedQuery(cls, params) -> str:
        img_key, sub_key = cls.getWbiKeys()
        signed_params = cls.encWbi(
            params,
            _img_key=img_key,
            _sub_key=sub_key
        )
        return urllib.parse.urlencode(signed_params)