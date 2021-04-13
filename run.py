# coding=utf-8

import sys
import getopt

from Info import Info
from Login import Login
from Free import FreeUrl
from Browser import Browser
from Download import Download


def usage():
    UG = '''
            ***************************************************************************
            *                   welcome to use the junk script                        *
            ***************************************************************************
            
            python3 run.py 
                
                -h --help 查看帮助
                
               * -U --url=任一话URL 
               * 
               * -F --free 爬取所有免费漫画 
                
                -L --login 在爬取前登陆腾讯动漫
                
                -N --NoPic 只爬取图片链接，不下载图片
                
                -B --browser=chrome 使用chrome浏览器（chrome，firefox可供选择，默认chrome）
                
                -M --mode=Noindow 使用selenium无窗口模式（Nowindow, Window可供选择，默认无窗口）
            
            Example：
                python3 run.py -U https://ac.qq.com/ComicView/index/id/505432/cid/1     # 爬取火影忍者
                
                python3 run.py -F -N  # 爬取所有免费漫画的图片的链接 
                
            ***************************************************************************
    '''
    print(UG)
    sys.exit()


def run1():
    url = ''
    login = 0
    noPic = 'noPic'
    browser = 'chrome'
    mode = 'Nowindow'
    login_mode = 'qq'

    a = input('请选择单本漫画，或者所有免费漫画（0/1）')
    if not a:
        url = input('请输入需要爬取的漫画某一话的URL')
        print('将爬取您所需要的漫画')
    else:
        print('将爬取所有免费漫画')

    a = input('请选择是否登陆(yes/no)')
    if a.lower() == 'yes':
        login = 1
        a = input('请选择登陆方式(qq/wechat)').lower()
        login_mode = a

    a = input('请选择是否需要下载图片（yes/no）')
    if a.lower() == 'yes':
        noPic = 'Pic'

    browser = input('请选择可用的浏览器（chrome/firefox）')

    a = input('是否使用无窗口浏览器（yes/no）')
    if a.lower() == 'no':
        mode = 'Window'

    return url, login, login_mode, noPic, browser, mode


def run2():
    url = ''
    login = 0
    noPic = 'Pic'
    browser = 'chrome'
    mode = 'Nowindow'
    login_mode = 'qq'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hU:FL:NB:M:',
                                   ['help', 'url=', 'free', 'login=', 'NoPic', 'browser=', 'mode='])
    except getopt.GetoptError as e:
        print(e)
        usage()

    for a, o in opts:
        if a in ('-h', '--help'):
            usage()
        elif a in ('-U', '--url'):
            url = o
        elif a in ('-F', '--free'):
            url = ''
        elif a in ('-L', '--login'):
            login = 1
            if o in ('qq', 'wechat'):
                login_mode = o
        elif a in ('-N', '--NoPic'):
            noPic = 'noPic'
        elif a in ('-B', '--browser'):
            if o in ('chrome', 'firefox'):
                browser = o
        elif a in ('-M', '--mode'):
            if o in ('Nowindow', 'Window'):
                mode = o

    return url, login, login_mode, noPic, browser, mode


def run():
    if not len(sys.argv[1:]):
        url, login, login_mode, noPic, browser_type, mode = run1()
    else:
        url, login, login_mode, noPic, browser_type, mode = run2()

    browser = Browser(browser_type, mode).browser
    D = Download(browser, noPic)

    I = Info()

    if login:
        Login(browser).login(login_mode, 'local')      # or wechat

    if url != '':
        D.down(I.comic_info(url))
    else:
        urls = FreeUrl().AllUrls()
        for url in urls:
            D.down(I.comic_info(url))


if __name__ == '__main__':
    run()
