# -*- coding:utf-8 -*-
"""
@author:zsprout
@file:alibaba.py
@time:2019-03-2220:45
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from .config import URL, KEYWORDS


def reloading(n):
    if n > 4:
        return
    try:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        WebDriverWait(browser, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '#offer60')))
        return
    except TimeoutException:
        return reloading(n+1)

def search():
    try:
        reloading(0)
        tatol = browser.find_element_by_xpath('//*[@id="fui_widget_5"]/div/span[1]/em')
        get_products()
        return tatol.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        page_input = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#fui_widget_5 > div > span.fui-number > input')))[0]
        # submit = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#fui_widget_5 > div > span.fui-forward > button')))[0]
        page_input.clear()
        page_input.send_keys(page_number)
        page_input.send_keys(Keys.ENTER)
        reloading(0)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#fui_widget_5 > span > a.fui-current'), str(page_number)))
        get_products()
    except TimeoutError:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_all_elements_located)
    dom = pq(browser.page_source, parser='html')
    items = dom('.imgofferresult-mainBlock').items()
    for item in items:
        product = {
            'image': item('.sm-offer-photo.sw-dpl-offer-photo').find('img').attr('src'),
            'price': item('div:nth-child(3)').text().split(' ')[0],
            'title': item('.s-widget-offershopwindowtitle.sm-offer-title.sw-dpl-offer-title.sm-widget-offershopwindowtitle-onerow')('a').text().replace('\n', ''),
            'company': item('.s-widget-offershopwindowcompanyinfo.sm-offer-company.sw-dpl-offer-company').text().split(' ')[0],
            'year': item('.s-widget-offershopwindowcompanyinfo.sm-offer-company.sw-dpl-offer-company').text().split(' ')[1],
            'chaseicon': item('.sm-widget-offershopwindowshoprepurchaserate')('span:nth-child(3)').text(),
            'msg': item('.sm-widget-offershopwindowshoprepurchaserate').find('i').text(),
            'tag': item('.s-widget-offershopwindowcompanytagww.sm-offer-sub').text().replace('\n', '')[4:]
        }
        print(product, flush=True)


def main():
    try:
        alisearch_keyword = browser.find_element_by_id('alisearch-keywords')
        alisearch_keyword.send_keys(KEYWORDS)
        alisearch_keyword.send_keys(Keys.ENTER)  # browser.find_element_by_id('alisearch-submit').click()
        wait.until(EC.presence_of_all_elements_located)
        browser.find_element(By.CLASS_NAME, 's-overlay-close-l').click()
        tatol = search()
        tatol = int(tatol)
        for i in range(2, tatol + 1):
            next_page(i)
    except Exception as e:
        print(e.args)
    finally:
        browser.close()



if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    browser.get(URL)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="check-dialog"]/div[2]/div[3]')))
    browser.find_element_by_xpath('//*[@id="check-dialog"]/div[2]/div[3]').click()
    main()

