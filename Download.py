import json
import os
import re
import threading
import time

import requests
from bs4 import BeautifulSoup

from Browser import Browser
from Info import Info


class Download:

    def __init__(self, browser, mode='noPic'):
        self.browser = browser

        self.comic_name = None
        self.total = 0
        self.count = 0

        if mode == 'noPic':
            self.getImg = self.getNoPic
        else:
            self.getImg = self.getPic

    def down(self, info, getImg=None):
        if getImg is None:
            getImg = self.getImg

        self.comic_name = list(info.keys())[0][0]
        self.total = list(info.keys())[0][1]

        if not os.path.exists('comic/'):
            os.mkdir('comic')
        if not os.path.exists('comic/' + self.comic_name):
            os.mkdir('comic/' + self.comic_name)

        ts = []
        for chapter_info in list(info.values())[0]:
            # getImg(chapter_info)
            ts.append(threading.Thread(target=getImg, args=(chapter_info,)))

        for t in ts:
            t.start()
            t.join()

    # 使用循环控制浏览器滚动至所有 gif，使之加载为正常的漫画图片
    def loading(self):
        while True:
            try:
                eles = self.browser.find_elements_by_css_selector('img[src="//ac.gtimg.com/media/images/pixel.gif"]')

                if not eles:
                    break

                for ele in eles:
                    self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                    time.sleep(0.2)
            except:
                continue

    # 爬取某一话的所有图片 chapter_info 为 [chapter_num, chapter_name, chapter_url]
    def getPic(self, chapter_info):
        comic_name = self.comic_name
        chapter_num = chapter_info[0]
        chapter_name = chapter_info[1].strip().replace(' ', '-')
        chapter_url = chapter_info[2]

        try:
            self.browser.get(chapter_url)
        except:
            self.count += 1
            print('\n{} 第{}话 {} 爬取失败，正在尝试第{}次重试……\n'.format(comic_name, chapter_num, chapter_name, self.count))

            if self.count < 5:
                self.getImg(chapter_info)
            else:
                print('\n{} 第{}话 {} 爬取失败……\n'.format(comic_name, chapter_num, chapter_name))
                return
        finally:
            self.count = 0

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
            except:
                continue

        path = 'comic/' + comic_name + '/' + chapter_num + '.' + chapter_name
        if not os.path.exists(path):
            os.mkdir(path)

        for i in range(len(urls)):
            print('当前{}. {} ： {}/{}'.format(chapter_num, chapter_name, i + 1, len(urls)))
            response = requests.get(urls[i])
            image = response.content

            path_ = path + '/' + num[i] + '.jpg'

            with open(path_, 'wb') as f:
                f.write(image)

    def getNoPic(self, chapter_info):
        comic_name = self.comic_name
        total = self.total
        chapter_num = chapter_info[0]
        chapter_name = chapter_info[1].strip().replace(' ', '-')
        chapter_url = chapter_info[2]

        try:
            self.browser.get(chapter_url)
        except:
            self.count += 1
            print('\n{} 第{}话 {} 爬取失败，正在尝试第{}次重试……\n'.format(comic_name, chapter_num, chapter_name, self.count))

            if self.count < 5:
                self.getImg(chapter_info)
            else:
                print('\n{} 第{}话 {} 爬取失败……\n'.format(comic_name, chapter_num, chapter_name))
                return
        finally:
            self.count = 0

        self.loading()

        source = self.browser.page_source
        soup = BeautifulSoup(source, 'lxml')

        lis = soup.select('#comicContain > li')

        dic1 = {}
        for li in lis:
            try:
                num = re.search('>(\\d+)/(\\d+)<', str(li))[1]
                url = re.search('src="(.*?)"', str(li))[1]
                dic1[num] = url
            except:
                continue

        dic2 = {str((comic_name, total)): {chapter_num + '.' + chapter_name: dic1}}

        if not os.path.exists('comic/' + comic_name + '/' + comic_name + '.json'):
            with open('comic/' + comic_name + '/' + comic_name + '.json', 'w') as f:
                json.dump(dic2, f)
        else:
            with open('comic/' + comic_name + '/' + comic_name + '.json', 'r+') as f:
                try:
                    dic2 = json.load(f)
                    if chapter_num + '.' + chapter_name in dic2[str((comic_name, total))].keys():
                        if len(dic1) > len(dic2[str((comic_name, total))][chapter_num + '.' + chapter_name]):
                            dic2[str((comic_name, total))][chapter_num + '.' + chapter_name] = dic1
                    else:
                        dic2[str((comic_name, total))][chapter_num + '.' + chapter_name] = dic1
                except:
                    pass
                finally:
                    f.seek(0)
                    f.truncate()
                json.dump(dic2, f)


if __name__ == '__main__':
    b = Browser('chrome', 'Nowindow').browser
    D = Download(b, mode='Pic')
    I = Info()
    D.down(I.comic_info('https://ac.qq.com/ComicView/index/id/505432/cid/1'))
