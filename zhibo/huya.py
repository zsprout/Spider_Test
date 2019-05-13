# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-04-26 15:07
desc:
"""

import requests
import random
from time import sleep
from save_to_mysql import Save_To_Mysql



class Huya():
    url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page={}'
    _config = {
        'db': 'zhibo',
        'table': 'huya_zhibo'
    }

    def __init__(self):
        self.r = requests.Session()
        self._client = Save_To_Mysql(**self._config)

    def get_page(self, num):
        response = self.r.get(self.url.format(num))
        if response.status_code == 200:
            return response.json()['data']

    def parse_page(self, results):
        for item in results:
            yield {
                'rid': item['profileRoom'],
                'uname': item['nick'],
                'title': item['introduction'],
                'po_count': item['totalCount'],
            }

    def save_to_mysql(self, item):
        try:
            self._client.insert(item)
        except Exception as e:
            print(e)


    def close(self):
        self._client.close()

    def run(self, num=1):
        self.data = self.get_page(num)
        self.datas = self.data['datas']
        self.page = self.data['page']
        self.totalPage = self.data['totalPage']
        for item in self.parse_page(self.datas):
            self.save_to_mysql(item)
        if self.page <= self.totalPage:
            print("已抓取第%d页，一共%d页..."%(self.page, self.totalPage))
            return self.run(num + 1)

hu = Huya()
try:
    hu.run()
finally:
    hu.close()