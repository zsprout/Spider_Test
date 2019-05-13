# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-04-26 13:08
desc:
"""
import requests
import time
import random
from save_to_mysql import Save_To_Mysql
from pprint import pprint

url = url = 'https://www.douyu.com/gapi/rkc/directory/0_0/{}'

r = requests.Session()
def get_page(num):
    try:
        if num % 30 == 0:
            time.sleep(random.choice((1, 2, 3)))
        response = r.get(url.format(num))
        if response.status_code == 200:
            page_count = response.json()['data']['pgcnt']
            results_list = response.json()['data']['rl']
            yield results_list
            if num < page_count:
                print("已抓取第%d页，一共%d页..."%(num, page_count))
                return loop_main(num + 1)
        return response.status_code
    except requests.ConnectionError as e:
        print(e, flush=True)

def parse_list(results_list):
    for item in results_list:
        yield {
            'rid': item['rid'],
            'uname': item['nn'],
            'title': item['rn'],
            'po_count': item['ol'],
        }
def loop_main(num=1):
    for result_list in get_page(num):
        for data in parse_list(result_list):
            M.insert(data)

config = {
    'db': 'zhibo',
    'table': 'douyu_zhibo'
}
if __name__ == '__main__':
    M = Save_To_Mysql(**config)
    try:
        loop_main()
    except Exception as e:
        print(e)
    finally:
        M.close()