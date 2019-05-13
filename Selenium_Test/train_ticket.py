# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-04-16 17:18
desc:
"""
from getpass import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class TrainTciket(object):
    login_url = "https://kyfw.12306.cn/otn/resources/login.html"
    welcome_url = "https://kyfw.12306.cn/otn/view/index.html"
    search_url = "https://kyfw.12306.cn/otn/leftTicket/init"

    def __init__(self):
        self.options = Options()
        self.options.set_headless()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 45)

    def _login(self):
        self.driver.get(self.login_url)
        try:
            sleep(1)
            self.actions.click(self.driver.find_element(By.LINK_TEXT, "账号登录"))
            self.actions.perform()
            sleep(20)
            self.actions.click(self.driver.find_element(By.LINK_TEXT, "立即登录"))
            self.actions.perform()
            self.wait.until(EC.url_to_be(self.welcome_url))
            print("登陆成功！")
        except TimeoutException:
            return self._login()



    def wait_input(self):
        self.from_station_text = input("请输入出发地：")
        self.to_station_text = input("请输入目的地：")
        # 时间格式：YYYY-MM-DD
        self.train_date_text = input("请输出发日期：")
        self.passengers_text = input("乘客姓名（如果有多名乘客，用英文逗号隔开）：")
        self.trains_text = input("车次（如果有多名乘客，用英文逗号隔开）：")


    def _order_ticket(self):
        try:
            self.driver.get(self.search_url)
            # self.wait.until(EC.text_to_be_present_in_element_value((By.ID, 'fromStationText'), self.from_station_text))
            self.from_station_input = self.wait.until(EC.presence_of_element_located((By.ID, 'fromStationText')))
            self.from_station_input.send_keys(self.from_station_text)
            # self.wait.until(EC.text_to_be_present_in_element_value((By.ID, 'toStationText'), self.to_station_text))
            self.to_station_input = self.wait.until(EC.text_to_be_present_in_element_value((By.ID, 'toStationText')))
            self.to_station_input.send_keys(self.to_station_text)
            self.wait.until(EC.text_to_be_present_in_element_value((By.ID, 'train_date'), self.train_date_text))
            self.search_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'query_ticket')))
            self.search_button.click()
        except TimeoutException:
            self.driver.close()


    def close(self):
        self.driver.close()

    def run(self):
        # self.wait_input()
        self._login()
        self._order_ticket()








if __name__ == '__main__':
    spider = TrainTciket()
    try:
        spider.run()
    finally:
        print("关闭")
        spider.close()
