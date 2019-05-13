# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-05-05 15:42
desc:
"""
import requests
import time
import pandas as pd
import csv

class CinemaBox(object):
    '''影院票房排行
    date: YYYY-MM-DD Default today
    limit: 1 ～ 700 Default 20
    '''
    base_url = "https://piaofang.maoyan.com/cinema/filter?typeId=0&date={0[0]}&offset=0&limit={0[1]}"
    result = {}
    __all__ = ["get"]

    def __init__(self, date=None, limit=None, **kwargs):
        if not date:
            date = kwargs.get('date', None)
        if not limit:
            limit = kwargs.get('limit', None)

        ISOTIMEFORMAT = '%Y-%m-%d'
        self.base_date = time.strftime(ISOTIMEFORMAT, time.localtime())
        if not date:
            date = self.base_date
        self.date = str(date)

        if not limit:
            limit = 20
        self.limit = limit

    def get(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.base_url.format((self.date, self.limit)), headers=headers)
        if response.status_code == 200:
            try:
                self.data = response.json()['data']
                self.parse_data()
            except Exception as e:
                print("Error:", str(e))
            finally:
                return self.result
        else:
            print("cinimabox响应码：", self.response.status_code)


    def parse_data(self):
        self.result['updateinfo'] = self.data['updateInfo']
        result_list = [{
            "影院名": self.data['all']['cinemaName'],
            "票房": self.data['all']['boxInfo'],
            "人次": self.data['all']['viewInfo'],
            "场均人次": self.data['all']['avgShowView'],
            "人均票价": self.data['all']['avgViewBox']
        }]
        result_list.extend([cinema for cinema in self.parse_list(self.data['list'])])
        self.result['list'] = result_list
        return self.result

    def parse_list(self, data):
        for k, item in enumerate(data):
            cinema = {
                "影院排行": k + 1,
                "影院ID": item['cinemaId'],
                "影院名": item['cinemaName'],
                "票房": item['boxInfo'],
                "人次": item['viewInfo'],
                "场均人次": item['avgShowView'],
                "人均票价": item['avgViewBox']
            }
            yield cinema

if __name__ == '__main__':
    A = CinemaBox(limit=700)
    print(A.get())
