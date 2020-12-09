import re
import requests
from bs4 import BeautifulSoup

'''
    获取某本漫画所有章节的信息，以二维列表的形式返回
    返回形式： [[章节序号， 章节名， 该章节的链接],[...],...]
'''


def ChaptersInfo(url):
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'lxml')
    lis = soup.select('#catalogueList > li')

    all_chapter_info = []

    for li in lis:
        chapter_num = re.search('\\d+', li.find_all('span')[0].get_text())[0]
        chapter_name = li.find_all('span')[1].get_text()
        chapter_url = 'http://ac.qq.com' + re.search('href="(.*?)"', str(li))[1]

        chapter_info = [chapter_num, chapter_name, chapter_url]

        all_chapter_info.append(chapter_info)

    return all_chapter_info
