#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import json
import time

import requests
from lxml import etree

from .fetch_proxy import fetch_proxy
from ..code.BaseCrawler import BaseCrawler
from ..code.Downloader import download_get

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

class GoodsCrawler(BaseCrawler, Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Thread.__init__(self)
        self.url_type = 'nav'

    def join_xp_rule(self, n):
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

    def fetch_amazom_navigation(self, url, n=1, result_dict={}):
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
            xp_rule_url, xp_rule_name, xp_rule_pre_name = self.join_xp_rule(n)
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

            result_dict[parent_dirname] = zip_dict
        # print(result_dict)
        return result_dict



def nav_save(dataQ, debug_log, db_log):
    print('\ntosell_save init\n')
    data_type = 'tosell'
    if dataQ.RedisQ.llen('tosellData') > 0:
        dbObj = GetDbObj().get_db_obj()
        cur = dbObj.cursor()
        dataOutput = DataOutput(dbObj, cur, db_log, debug_log, dataQ)
        data_tosell_db_name = SqlConfig.data_tosell_db_name
        data_tosell_update_sql = SqlConfig.data_tosell_update_sql
        data_tosell_insert_sql = SqlConfig.data_tosell_insert_sql

        druid_tosell_db_name = SqlConfig.druid_tosell_db_name
        #druid_tosell_update_sql = SqlConfig.druid_tosell_update_sql
        druid_tosell_update_sql = None #SqlConfig.druid_tosell_update_sql
        druid_tosell_insert_sql = SqlConfig.druid_tosell_insert_sql
        while True:
            datas = dataQ.get_new_tosellData()
            if not datas:
                if dataQ.RedisQ.llen('tosellData') > 0:
                    datas = dataQ.get_new_tosellData()
                else:
                    break
            # print('\ntosell_save datas: [= %s =] \n' % (datas))
            tm = DataOutput.get_redis_time()
            for item in datas:
                asin = item
                tosell_datas = datas[item][0]
                tosell_list = datas[item][1]
                from pprint import pprint
                pprint(tosell_datas)
                pprint(tosell_list)
                print(tosell_datas['getinfo_tm'], 1)
                tosell_datas['getinfo_tm'] = tm
                print(tosell_datas['getinfo_tm'], 2)
                sql = "select asin, aday from public.amazon_product_tosell where asin=%(asin)s and aday=%(aday)s limit 1;"
                aday = tosell_list[0]['aday'] if len(tosell_list) > 0 else return_PST().strftime('%Y%m%d')
                select_dict = {'asin': asin, 'aday': aday}
                cur.execute(sql, select_dict)
                select_rows = cur.fetchall()
                dbObj.commit()
                if len(select_rows) < 1:
                    print(tosell_datas)
                    if not tosell_datas.get('sname'):
                        sql1 = "select sname, seller_id from public.amazon_product_data where asin='%s' and getinfo_tm > %s" % (asin, tm - 24*3600*1000)
                        cur.execute(sql1)
                        select_rows = cur.fetchall()
                        dbObj.commit()
                        select_rows = select_rows[0] if len(select_rows) == 1 else ('', '')
                        sname, seller_id = select_rows
                        print('seller_id: ', seller_id)
                        print('sname ',sname)
                        tosell_datas['sname'] = sname
                        tosell_datas['seller_id'] = seller_id
                    data0 = dataOutput.save_data_to_db(data_tosell_update_sql, data_tosell_insert_sql,
                                                       asin, tosell_datas, db_name=data_tosell_db_name)
                    for item in tosell_list:
                        item['tm'] = int(tm / 1000)
                        data = dataOutput.save_data_to_db(druid_tosell_update_sql, druid_tosell_insert_sql,
                                                          asin, item, db_name=druid_tosell_db_name)

                    # 记录更新时间
                    dataOutput.crawler_tm(asin, data_type)
        cur.close()
        dbObj.close()
        db_log.war('%s, %s线程任务已完成\n' % (return_PST().strftime("%Y-%m-%d %H:%M:%S"), data_type))
    else:
        db_log.war('%s, %s数据队列为空\n' % (return_PST().strftime("%Y-%m-%d %H:%M:%S"), data_type))


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
