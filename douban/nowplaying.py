# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-05-11 12:08
desc:
"""
import bs4
from coming import DoubanMovie

url = 'https://movie.douban.com/cinema/nowplaying/{city}'


def main():
    u = DoubanMovie(url)
    soup = DoubanMovie.makesoup(u.get_response())
    for li in soup.find(attrs={'id': 'nowplaying'}).ul.children:
        if isinstance(li, bs4.element.Tag):
            u = DoubanMovie(li.find('a', attrs={'class':'ticket-btn'}).attrs['href'])
            u.run()
            print(u.result)


if __name__ == '__main__':
    main()