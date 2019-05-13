# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-05-06 16:08
desc:
"""
import requests
import time
from pyquery import PyQuery as pq
import re

class BaseRanks(object):
    base_tab = 0
    result = {}
    __all__ = ["get"]

    def base_get(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return response.status_code

class RanksYear(BaseRanks):
    '''影片总票房排行榜
    year: 查询年份 Default 0
    '''
    d = {
        '片名': '变形金刚4：绝迹重生',
        '票房': '197651',
        '平均票价': '41.633812',
        '场均人次': '50',
    }
    rankings_year = 'https://piaofang.maoyan.com/rankings/year?year={}'
    base_year = 0

    def __init__(self, year=None, **kwargs):
        if not year:
            year = kwargs.get('year', 0)
        try:
            year = int(year)
        except Exception as e:
            print("Error:输入内容不规范，已处理")
            year = self.base_year
        finally:
            self.response = self.base_get(self.rankings_year.format(self.base_year))
            ul = pq(self.response, parser='html')('#tab-year ul')
            self.year_tup = tuple([int(li.text().strip('年')) for li in ul.find('li').items() if li.attr('class') != 'active'])
            self.base_tab = tuple([i for i in range(len(self.year_tup))])
            if year not in self.year_tup:
                year = self.base_year
            self.query_year = year

    def get(self):
        if self.query_year != self.base_year:
            self.response = self.base_get(self.rankings_year.format(self.query_year))
        self.parse_response()
        return self.result

    def parse_response(self):
        self.dom = pq(self.response, parser='html')
        self.result['title'] = self.dom('#total-box').text()
        self.ul_list = self.parse_list(self.dom('.row').items())
        self.result['row'] = next(self.ul_list)
        self.result['list'] = [item for item in self.ul_list]

    def parse_list(self, ul_list):
        title_li = next(ul_list).find('li')
        row = {
            'row1': title_li('.col0').text(),
            'row2': title_li('.col1').text(),
            'row3': title_li('.col2').text(),
            'row4': title_li('.col3').text(),
            'row5': title_li('.col4').text()
        }
        yield row
        for ul in ul_list:
            list_li = ul.find('li')
            item = {
                '排名': list_li('.col0').text(),
                '片名': list_li('.first-line').text(),
                '上映时间': list_li('.second-line').text(),
                '票房(万元)': list_li('.col2').text(),
                '平均票价': list_li('.col3').text(),
                '场均人次': list_li('.col4').text(),
                '链接': re.findall("href:'(.*?)'", ul.attr('data-com'))[0]
            }
            yield item


class RanksDay(BaseRanks):
    '''影片日票房排行榜
    tab: 0 or 1; 影片单日票房 或 影片首日票房 Default 0
    '''
    rankings_day = 'https://piaofang.maoyan.com/rankings/day?tab={}'
    base_tab = (0, 1)

    def __init__(self, tab=None):
        try:
            if tab and (int(tab) in self.base_tab):
                tab = int(tab)
            else:
                tab = self.base_tab[0]
        except Exception as e:
            print("Error:输入内容不规范，已处理")
            tab = self.base_tab[0]
        finally:
            self.tab = tab

    def get(self):
        self.response = self.base_get(self.rankings_day.format(self.tab))
        self.dom = pq(self.response, parser='html')
        self.result['title'] = self.dom('#total-box').text()
        self.tr_list = self.parse_day(self.dom('#day-list-wrap').find('tr').items())
        self.result['row'] = next(self.tr_list)
        self.result['list'] = [item for item in self.tr_list]
        return self.result

    def parse_day(self, tr_list):
        self.row = {}
        for r, c in enumerate(next(tr_list).find('th').items()):
            self.row[r] = c.text().replace('\n', '')
        yield self.row
        for tr in tr_list:
            item = {
                "链接": re.findall("href:'(.*?)'", tr.attr('data-com'))[0]
            }
            td_list = [item for item in tr.find('td').items()]
            for k, v in enumerate(td_list):
                item[self.row[k]] = v.text().replace('\n', '')
            yield item

class RankMarket(BaseRanks):
    '''大盘票房排行榜
    tab: 0，1， 2 单日票房 单周票房 单月票房 Default 0
    '''
    rankings_market = 'https://piaofang.maoyan.com/rankings/market?tab={}'
    base_tab = (0, 1, 2)

    def __init__(self, tab=None):
        try:
            if tab and (int(tab) in self.base_tab):
                tab = int(tab)
            else:
                tab = self.base_tab[0]
        except Exception as e:
            print("Error:输入内容不规范，已处理")
            tab = self.base_tab[0]
        finally:
            self.tab = tab

    def get(self):
        self.response = self.base_get(self.rankings_market.format(self.tab))
        self.dom = pq(self.response, parser='html')
        self.result['title'] = self.dom('#total-box').text()
        self.tr_list = self.parse_market(self.dom('#market-list-wrap').find('tr').items())
        self.result['row'] = next(self.tr_list)
        self.result['list'] = [item for item in self.tr_list]
        return self.result

    def parse_market(self, tr_list):
        self.row = {}
        for r, c in enumerate(next(tr_list).find('th').items()):
            self.row[r] = c.text().replace('\n', '')
        yield self.row
        for tr in tr_list:
            item = {
            }
            td_list = [item for item in tr.find('td').items()]
            for k, v in enumerate(td_list):
                item[self.row[k]] = v.text().replace('\n', '')
            yield item




if __name__ == '__main__':
    year_box = RanksYear()
    day_box = RanksDay()
    market_box = RankMarket()
    print(year_box.get())
    print(day_box.get())
    print(market_box.get())