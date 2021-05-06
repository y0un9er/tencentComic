# 原博文地址
https://blog.csdn.net/CSDNiamcoming/article/details/110926242	

# chrome driver 下载地址
注意本机使用的 chrome 的版本
http://chromedriver.storage.googleapis.com/index.html

# firefox driver 已提供
使用 apt-get install firefox 安装火狐浏览器之后即可使用

# usage:
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
                python3 run.py -N -L qq -B firefox -U https://ac.qq.com/ComicView/index/id/505432/cid/1  
                
                python3 run.py -F -N  # 爬取所有免费漫画的图片的链接 
                
            ***************************************************************************

或直接使用 python3 run.py

# 登陆问题
	经常会登陆出错，所以登陆完之后截了个图，存在本目录下的 login_state.png
	以后加个验证码处理之类的东西就完美了

# 需要的一些库
	pip3 install pillow
	pip3 install selenium
	pip3 install beautifulsoup4

# Linux 建议汉化, 不然截图会有乱码
	apt install language-pack-zh-hans


	输入 vim /etc/environment     

	在末尾追加一行 LANG="zh_CN.uth8"


	source /etc/environment  使更改生效

# 进程问题
	由于各种原因（其实是因为太菜了），并没有控制进程数，主要不知道怎样控制合理，本来就跑得挺慢了
	
	所以导致在 vps 上测试的时候直接崩了，vps 应该是 1核1G 的，并发量太大，直接死锁

	本机 i5-8300H + 两根8G内存条，CPU 利用率在 20% 多，内存 35% 左右，711话的火影忍者爬了 半个小时 左右，爬的链接，没下载图片
	说明一下，火影阅点买的

## 因为环境原因网络原因，很多测试过的代码也会出现各种各样的问题，一般使用以下方法排错
```python
self.browser.get_screenshot_as_file('1.png');	# 网页截图

with open('1.html', 'w') as f:			# 保存网页源码
	f.write(self.browser.page_source)
```
		
