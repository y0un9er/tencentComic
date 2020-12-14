import AllChapter
import AllFree
import Download
import threading

'''
    选择下载所有免费漫画或部分
'''


def main():
    check = input('\n下载全部免费漫画 或 下载部分 （1 or 2） ')

    if check == '1':
        F = AllFree.FreeUrl()
        all_comic_url = F.AllUrls()

    else:
        check2 = input('\n请选择下载某页，或某范围（1 or 2） ')
        if check2 == '1':
            url = input('\n请输入该页的链接： ')
            F = AllFree.FreeUrl(url=url)
            all_comic_url = F.OnePageUrls()
        else:
            start = int(input('\n请输入开始页码（1-116？） '))
            end = int(input('\n请输入结束页码（1-116？） '))
            F = AllFree.FreeUrl(start=start, end=end)
            all_comic_url = F.AllUrls()

    D = Download.Download()
    D.login()

    for comic_url in all_comic_url:
        D.comic_info(comic_url)

        all_info = AllChapter.ChaptersInfo(comic_url)

        ts = []

        for chapter_info in all_info:
            # D.getImg(chapter_info)
            ts.append(threading.Thread(target=D.getImg, args=(chapter_info,)))

        for t in ts:
            t.start()
            t.join()


if __name__ == '__main__':
    main()
