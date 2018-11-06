#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import json
import time

import requests
from lxml import etree

from .fetch_proxy import fetch_proxy
# from .Spider.Downloader import download_get
from ..Downloader import download_get

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
proxies = {
  "http": "http://16WRMGEL:070128@n10.t.16yun.cn:6442",
  "https": "http://16WRMGEL:070128@n10.t.16yun.cn:6442",
}
proxy = fetch_proxy()
params = dict(
    # headers=None,
    proxies=proxies,
    # cookies=None,
    verify=None,
    timeout=180,
)


def join_xp_rule(n):
    """
    xpath规则拼接解析
    :param n: 层级数
    :return xp_rule_url: 提取当前层级菜单的URL
    :return xp_rule_name: 提取当前层级菜单的标题
    :return xp_rule_pre_name: 提取上级菜单的标题
    """
    join_ul = '/ul'*n
    pre_join_ul = '/ul'*(n-1)
    xp_rule_url = '//ul[@id="zg_browseRoot"]' + join_ul + '/li/a/@href'
    xp_rule_name = '//ul[@id="zg_browseRoot"]' + join_ul + '/li/a/text()'
    xp_rule_pre_name = '//ul[@id="zg_browseRoot"]' + pre_join_ul + '/li/span/text()'
    return xp_rule_url, xp_rule_name, xp_rule_pre_name

def fetch_amazom_navigation(url, n=1, result_dict={}):
    """
    递归抓取多级菜单，返回一个嵌套菜单的字典
    :param url: 需要爬取的URL
    :param n: 层级数，默认1
    :param result_dict: 返回的字典，默认为{}
    :return: 嵌套菜单的字典
    """
    params['url'] = url
    resp_text, resp, need_param = download_get(**params)
    if resp.status_code == 200:
        html = etree.HTML(resp_text)
        xp_rule_url, xp_rule_name, xp_rule_pre_name = join_xp_rule(n)
        #解析字段
        title_list = html.xpath(xp_rule_name)
        print(title_list)
        url_list = html.xpath(xp_rule_url)
        # print(url_list)
        try:
            parent_dirname = html.xpath(xp_rule_pre_name)[0].strip()
            print('parent:'+parent_dirname)
        except IndexError as e:
            parent_dirname = 0
        #存入字典
        zip_dict = dict(zip(title_list, range(0,len(title_list)) ))
        # zip_dict = dict(zip(title_list, url_list))

        time.sleep(2)
        if title_list:
            n = n+1
            if n < 5:
                for u in url_list:
                    print(u)
                    print('=====%d=====' % n)
                    # url = url_list[0]
                    fetch_amazom_navigation(u, n, zip_dict)

        result_dict[parent_dirname] = zip_dict
    # print(result_dict)
    return result_dict

def main():
    url = "https://www.amazon.com/Best-Sellers/zgbs/"
    result = fetch_amazom_navigation(url)
    print(result)
    try:
        result_json = json.dumps(result, ensure_ascii=False)
    except ValueError as e:
        with open('dirname04.txt', 'w', encoding='utf-8') as f:
            f.write(str(result))
    with open('dirname04.json', 'w', encoding='utf-8') as f:
        f.write(result_json)

if __name__ == '__main__':
    main()

    # from multiprocessing import Pool
    # p = Pool(2)
    # for i in range(3):
    # p.apply_async(fetch_amazom_navigation(), args=(url,))
    # p.close()
    # p.join()


    # from threading import Thread
    # import time
    #
    # print(u'多线程抓取')
    # ts = [Thread(target=get, args=(url,)) for url in urls]
    # t1 = time.time()
    # for t in ts:
    #     t.start()
    # for t in ts:
    #     t.join()
    # print(time.time() - t1)
