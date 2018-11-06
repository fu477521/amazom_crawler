#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urljoin, urlparse

IP_SERVER_ADDR = 'http://119.29.97.152:5555/proxy/'
IP_SERVER_API = urljoin(IP_SERVER_ADDR, 'https')


def fetch_proxy(scheme='https'):
    """
    从服务器的代理池获取代理.

    :url:       代理池请求地址
    :anonymity: 高匿或者透明代理
    :return:    {scheme: IP:PORT}
    """
    # _parse = urlparse(url)
    # scheme = _parse[0]
    # params = {
    #     "scheme": scheme,
    #     # "anonymity": anonymity,
    # }
    text = None
    try:
        url = urljoin(IP_SERVER_ADDR, scheme)
        req = requests.get(url)
        text = req.text
        # data = req.json()
    except:
        print("Failed to fetch proxy: %s" % text)

    proxy_url = str(text)
    result = {scheme: proxy_url}
    print("Got proxy: ", result)
    return result


# say, the site is 'baidu'
# url = 'http://httpbin.org/get'
# url = 'https://www.baidu.com'
# get scheme and proxy

if __name__ == "__main__":
    _p = fetch_proxy()
    print(_p)
    proxy = {
        'http': '222.221.11.119:3128',
        'https': 'https://122.237.106.56:80'
    }
    url = 'https://httpbin.org/get'
    # build a request
    r = requests.get(url,
                     proxies=_p,
                     timeout=20,
                     # and other parameters
                     )
    print(r.status_code)
    print(r.text)
