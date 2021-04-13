# coding=utf-8

# import getpass
import os
import time

import requests
import getpass

from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Browser import Browser


class Login:

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 30)

    def login(self, mode='qq', option=''):
        self.browser.get('http://ac.qq.com')
        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="sidebarComTabMe"]')))
        self.browser.find_element_by_xpath('//*[@id="sidebarComTabMe"]').click()

        if mode == 'qq':
            self.login_qq(option)
        else:
            return self.login_wechat(option)

    def logout(self):
        self.browser.delete_all_cookies()
        self.browser.refresh()

    def login_qq(self, option=''):
        self.browser.switch_to.frame('iframe_qq')

        self.wait.until(ec.frame_to_be_available_and_switch_to_it('ptlogin_iframe'))

        if option == 'quick':
            # 点击登陆
            self.browser.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]').click()
        else:
            # 账号密码登陆
            time.sleep(2)
            self.browser.find_element_by_xpath('//*[@id="switcher_plogin"]').click()

            username = input('\n请输入账号: ')
            # password = input('请输入密码: ')
            password = getpass.getpass('请输入密码: ')  # pycharm 不可用

            self.browser.find_element_by_xpath('//*[@id="u"]').send_keys(username)
            self.browser.find_element_by_xpath('//*[@id="p"]').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="p"]').send_keys(Keys.ENTER)

            self.browser.get_screenshot_as_file('login_state.png')

    def login_wechat(self, option=''):
        self.browser.switch_to.frame('iframe_wx')
        image_url = self.browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/img').get_attribute('src')

        if option == 'local':
            with open('qr.png', 'wb') as f:
                f.write(requests.get(image_url).content)

            Image.open('qr.png').show()
            os.remove('qr.png')

            self.browser.switch_to.parent_frame()
            while self.browser.find_element_by_xpath('//*[@id="sidebarComTabMe"]/img').get_attribute('src') == 'https://ac.gtimg.com/media/images/top_face_no_bg.jpg':
                time.sleep(1)

            return
        else:
            return image_url


if __name__ == '__main__':
    b = Browser('chrome', 'Window').browser
    L = Login(b)
    print(L.login('wechat'))
