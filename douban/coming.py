# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-05-11 12:08
desc:
"""
import requests
import bs4
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

url = 'https://movie.douban.com/coming'

class DoubanMovie(object):
    result = {}

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def get_response(self):
        try:
            self.r = requests.get(self.url, headers=self.headers)
            self.r.raise_for_status()
            self.r.encoding = 'utf-8'
            self.html = self.r.text
            return self.html
        except:
            print("请求异常")
            return

    @classmethod
    def makesoup(cls, html):
        cls.soup = BeautifulSoup(html, 'lxml')
        return cls.soup

    def makedoc(self):
        self.doc = pq(self.html, parser='html')
        return self.doc

    def parse_info(self):
        data = {}
        for item in self.doc('#info').text().split('\n'):
            msg = item.split(': ')
            if "/" in item:
                data[msg[0]] = ", ".join(msg[1].split(' / '))
            else:
                data[msg[0]] = msg[1]
        if "IMDb链接" in data:
            data["IMDb链接"] = self.doc('#info')('a')[-1].xpath('@href')[0]
        return data

    def parse_rating(self):
        rating_start = self.doc('.ratings-on-weight div').text()
        if rating_start:
            return {
                'start': rating_start.replace('\n', ':').split('  '),
                'sum': self.doc('.rating_self.clearfix').text().split('\n')
            }
        else:
            return "暂无评分"

    def parse_result(self):
        self.makedoc()
        self.result['title'] = self.doc('h1').text()
        self.result['info'] = self.parse_info()
        self.result['rating'] = self.parse_rating()

    def run(self):
        if self.get_response():
            self.parse_result()
        return self.result



def main():
    u = DoubanMovie(url)
    soup = DoubanMovie.makesoup(u.get_response())
    for tr in soup.find(attrs={'id': 'content'}).tbody.children:
        if isinstance(tr, bs4.element.Tag):
            u = DoubanMovie(tr.a.attrs['href'])
            u.run()
            print(u.result)


if __name__ == '__main__':
    main()