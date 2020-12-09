# coding=utf-8
from selenium import webdriver

'''
    创建 Browser 类是选择 显示浏览器窗口 或 不显示
    browser2 = Browser('Window').browser
    browser1 = Browser('Nowindow').browser
'''


class Browser:
    browser = ''

    def __init__(self, mode='Nowindow'):
        if mode == 'Nowindow':
            opt = webdriver.ChromeOptions()
            opt.headless = True
            self.browser = webdriver.Chrome(options=opt)
        elif mode == 'Window':
            self.browser = webdriver.Chrome()
