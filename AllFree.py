import re

import requests
from bs4 import BeautifulSoup

'''
    获取免费漫画的链接
'''


class FreeUrl:
    def __init__(self, url='', start=1, end=116):
        self.url = url
        self.start = start
        self.end = end

    # 获取某一列表页所有漫画的链接
    # url 格式为 https://ac.qq.com/Comic/all/page/1 或 https://ac.qq.com/Comic/all?page=1
    def OnePageUrls(self, url=''):
        if self.url != '':
            url = self.url

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        urls = []

        for i in range(1, 13):
            a = soup.select(f'body > div.ui-wm.ui-mb40.ui-mt40.clearfix > div.ret-main-wr.ui-mb40.ui-left > div > '
                            f'div.ret-search-result > ul > li:nth-child({i}) > div.ret-works-info > a')
            try:
                url = re.search('href="(.*?)"', str(a))[1]
                url = 'https://ac.qq.com' + url.replace('Comic/comicInfo', 'ComicView/index') + '/cid/1'
                urls.append(url)
            except:
                continue
        return urls

    # 所有免费漫画链接
    # https://ac.qq.com/Comic/all/search/hot/vip/1/page/{i} i=1--116
    def AllUrls(self):      
        self.url = ''
        urls = []

        for i in range(self.start, self.end+1):
            page_url = f'https://ac.qq.com/Comic/all/search/hot/vip/1/page/{i}'
            urls += self.OnePageUrls(page_url)

        return urls

