import re
import os
import time
import getpass
import requests
import threading

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import Browser
import AllChapter

'''
    Download类，用于下载爬取到的图片
'''


class Download:
    browser = ''
    wait = ''
    name = ''
    total = 0

    # 初始化，调用 Browser 类创建浏览器，默认 Nowindow，使用无窗口浏览器，传入 Window 使用窗口
    def __init__(self, url=None):
        self.browser = Browser.Browser().browser
        self.wait = WebDriverWait(self.browser, 30)

        if url is not None:
            self.comic_info(url)

    def login(self):
        if input('是否登陆（y/n）') != 'y':
            return

        url = 'http://ac.qq.com'
        self.browser.get(url)

        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="sidebarComTabMe"]')))
        self.browser.find_element_by_xpath('//*[@id="sidebarComTabMe"]').click()

        self.browser.switch_to.frame('iframe_qq')
        self.browser.switch_to.frame('ptlogin_iframe')

        if input('选择登陆方式（0：快捷登陆（已登录QQ），1：账号密码登陆（需关闭网页登陆保护）默认为 0） ') != '1':
            # 点击登陆
            self.browser.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]').click()
        else:
            # 账号密码登陆
            self.browser.find_element_by_xpath('//*[@id="switcher_plogin"]').click()

            username = input('请输入账号: ')
            # password = input('请输入密码: ')
            password = getpass.getpass('请输入密码: ') # pycharm 不可用

            self.browser.find_element_by_xpath('//*[@id="u"]').send_keys(username)
            self.browser.find_element_by_xpath('//*[@id="p"]').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="p"]').send_keys(Keys.ENTER)

    # 使用循环控制浏览器滚动至所有 gif，使之加载为正常的漫画图片
    def loading(self):
        while True:
            try:
                elements = self.browser.find_elements_by_css_selector('img[src="//ac.gtimg.com/media/images/pixel.gif"]')

                if not elements:
                    break

                for ele in elements:
                    self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                    time.sleep(0.2)
            except:
                continue

    # 返回漫画名和总话数
    def comic_info(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        total = soup.select('#catalogueContain > span')
        total = re.search('\\d+', str(total))[0]

        name = soup.select('#chapter')
        name = re.search('>(\\S+)<', str(name))[1]

        if not os.path.exists(name):
            os.mkdir(name)

        self.name = name
        self.total = int(total)

    # 爬取某一话的所有图片 chapter_info 为 [chapter_num, chapter_name, chapter_url]
    def getImg(self, chapter_info):
        comic_name = self.name
        chapter_num = chapter_info[0]
        chapter_name = chapter_info[1].strip().replace(' ', '-')
        chapter_url = chapter_info[2]
        
        try:
            self.browser.get(chapter_url)
        except:
            print(comic_name+' '+chapter_num+'.'+chapter_name+'爬取失败')
            if input('是否重新尝试（y/n） ') == 'y':
                self.getImg(chapter_info)
            else:
                return
            
        self.loading()

        source = self.browser.page_source
        soup = BeautifulSoup(source, 'lxml')

        lis = soup.select('#comicContain > li')

        urls = []
        num = []
        for li in lis:
            try:
                num.append(re.search('>(\\d+)/(\\d+)<', str(li))[1])
                urls.append(re.search('src="(.*?)"', str(li))[1])
            except Exception as e:
                print(e)
                continue

        path = comic_name + '/' + chapter_num + '.' + chapter_name
        if not os.path.exists(path):
            os.mkdir(path)

        for i in range(len(urls)):
            print('\r当前{}. {} ： {}/{}'.format(chapter_num, chapter_name, i + 1, len(urls)), end='')
            response = requests.get(urls[i])
            image = response.content

            path_ = path + '/' + num[i] + '.jpg'

            with open(path_, 'wb') as f:
                f.write(image)


# 如果要下载某本已知漫画，直接运行此文件，否则使用 run.py
if __name__ == '__main__':
    url = input('请输入要下载的漫画的某一话的链接')
    D = Download(url)

    D.login()

    all_info = AllChapter.ChaptersInfo(url)

    ts = []

    for chapter_info in all_info:
        ts.append(threading.Thread(target=D.getImg, args=(chapter_info, )))

    for t in ts:
        t.start()
        t.join()

    D.browser.quit()
