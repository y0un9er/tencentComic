# coding=utf-8

import re

import requests
from bs4 import BeautifulSoup


class Info:
    @staticmethod
    def comic_info(url):    # 返回 {(漫画名，总章节数):[[章节序列，章节名，URL]，……]

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        total = soup.select('#catalogueContain > span')
        total = re.search('\\d+', str(total))[0]

        name = soup.select('#chapter')
        name = re.search('>(\\S+)<', str(name))[1]

        lis = soup.select('#catalogueList > li')

        all_chapter_info = []

        for li in lis:
            chapter_num = re.search('\\d+', li.find_all('span')[0].get_text())[0]
            chapter_name = li.find_all('span')[1].get_text()
            chapter_url = 'http://ac.qq.com' + re.search('href="(.*?)"', str(li))[1]

            chapter_info = [chapter_num, chapter_name, chapter_url]

            all_chapter_info.append(chapter_info)

        return {(name, total): all_chapter_info}
        # {('火影忍者', '711'): [['1', '第1话 旋涡鸣人', 'http://ac.qq.com/ComicView/index/id/505432/cid/1'], ......]}


if __name__ == '__main__':
    a = Info()
    b = a.comic_info('https://ac.qq.com/ComicView/index/id/505432/cid/1')
    print(b)