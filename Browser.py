# coding=utf-8

from selenium import webdriver

'''
    创建 Browser 类是选择 显示浏览器窗口 或 不显示
    browser1 = Browser('chrome', 'Nowindow').browser
    browser2 = Browser('firefox', 'Window').browser
'''


class Browser:
    browser = ''

    def __init__(self, browser, mode='Nowindow'):
        if browser == 'chrome':
            self.chrome(mode)
        elif browser == 'firefox':
            self.firefox(mode)

    def chrome(self, mode):
        if mode == 'Nowindow':
            opt = webdriver.ChromeOptions()
            opt.headless = True
            self.browser = webdriver.Chrome(options=opt)
        elif mode == 'Window':
            self.browser = webdriver.Chrome()

    def firefox(self, mode):
        if mode == 'Nowindow':
            opt = webdriver.FirefoxOptions()
            opt.headless = True
            self.browser = webdriver.Firefox(executable_path='./geckodriver', options=opt)
        elif mode == 'Window':
            self.browser = webdriver.Firefox(executable_path='./geckodriver')


if __name__ == '__main__':
    b = Browser('chrome').browser
    b.delete_all_cookies()
    b.refresh()
