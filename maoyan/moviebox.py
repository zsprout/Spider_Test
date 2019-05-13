# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-05-05 15:29
desc:
"""

import requests
import time

class MovieBox(object):
    '''电影票房排行
    date: YYYYMMDD Default today
    '''
    base_url = "https://box.maoyan.com/promovie/api/box/second.json?beginDate={}"
    result = {}
    __all__ = ["get"]

    def __init__(self, date=None, **kwargs):
        if not date:
            date = kwargs.get('date', None)

        ISOTIMEFORMAT = '%Y%m%d'
        self.base_date = time.strftime(ISOTIMEFORMAT, time.localtime())
        if not date:
            date = self.base_date
        self.date = str(date)

    def get(self):
        self.response = requests.get(self.base_url.format(self.date))
        if self.response.status_code == 200:
            try:
                self.second = self.response.json()['data']
                self.parse_data()
            except Exception as e:
                print("Error:", str(e))
            finally:
                return self.result
        else:
            print("moviebox响应码：", self.response.status_code)

    def parse_data(self):
        self.result['查询日期'] = self.second['queryDate']
        self.result['更新时间'] = self.second['updateInfo']
        self.result['累计票房'] = self.second['totalBox'] + self.second['totalBoxUnit']
        if self.second['queryDate'] == self.second['serverTime'][:10]:
            self.result['累计票房'] = "今日实时 " + self.result['累计票房']
        else:
            self.result['累计票房'] = "大盘 " + self.result['累计票房']
        self.result['list'] = [item for item in self.parse_list(self.second['list'])]
        return self.result

    def parse_list(self, data):
        for k,item in enumerate(data):
            result = {
                "排名": k + 1,
                "影片": item['movieName'],
                "综合票房": item['boxInfo'],
                "票房占比": item['boxRate'],
                "排片场次": item['showInfo'],
                "排片占比": item['showRate'],
                "场均人次": item['avgShowView'],
                "上座率": item['avgSeatView'],
                "上映信息": item['releaseInfo'],
                "累计票房": item['splitSumBoxInfo']
            }
            yield result

if __name__ == '__main__':
    A = MovieBox()
    print(A.get())
