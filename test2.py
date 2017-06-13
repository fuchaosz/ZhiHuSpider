# 学习Python爬虫
import urllib
from urllib import request, parse, error, response
import re

# 1 get请求
# url = 'http://www.baidu.com'
# response = request.urlopen(url)
# print(response.read())

# # 2 post请求
# values = {'uesername':'1016903103@qq.com','password':'xxxxx'}
# data = parse.urlencode(values).encode('utf-8')
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# req = request.Request(url,data)
# response = request.urlopen(req)
# print(response.read())

# # 3 异常处理
# req = request.Request('http://www.google.com')
# try:
#     urllib.request.urlopen(req)
# except urllib.error.URLError as e:
#     print(e.reason)

# 4 正则表达式
# #将正则表达式编译成Pattern对象
# pattern = re.compile(r'hello')
# #使用re.match匹配文本，获得匹配结果，无法匹配是将返回None
# result1 = re.match(pattern,'hello')
# result2 = re.match(pattern,'helloo CQC!')
# result3 = re.match(pattern,'helo CQC!')
# result4 = re.match(pattern,'hello CQC!')
#
# print(result1.group() if result1 is not None else '1匹配失败')
# print(result2.group() if result2 is not None else '2匹配失败')
# print(result3.group() if result3 is not None else '3匹配失败')
# print(result4.group() if result4 is not None else '4匹配失败')

# #分组
# m = re.match(r'(\w+) (\w+)(?P<sign>.*)','hello world!')
# print('m.string:',m.string)
# print('m.re:',m.re)
# print('m.pos:',m.pos)
# print('m.endpos:',m.endpos)
# print('m.lastindex:',m.lastindex)
# print('m.lastgroup:',m.lastgroup)
# print('m.group(1,2):',m.group(1,2))
# print('m.groups():',m.groups())
# print('m.groupdict():',m.groupdict())
# print('m.start(2):',m.start(2))
# print('m.end(2):',m.end(2))
# print('m.span(2):',m.span(2))
# print(r"m.expand(r'\g \g\g'):",m.expand(r'\2 \1\3'))
# # 搜索search
# pattern = re.compile(r'world')
# match = re.search(pattern,'hello world!')
# # match = re.match(pattern,'hello world')      #用match则无法匹配
# if match:
#     print(match.group())
# #分割 split
# pattern = re.compile(r'\d+')
# print(re.split(pattern,'one1two2three3four4'))
# #搜索全部能匹配的子串
# pattern = re.compile(r'\d+')
# print(re.findall(pattern,'one1two2three3four4'))
# #搜索，返回一个迭代器
# pattern = re.compile(r'\d+')
# for m in re.finditer(pattern,'one1two2three3four4'):
#     print(m.group())
# #替换
# pattern = re.compile(r'(\w+) (\w+)')
# s = 'i say, hello world!'
# print(re.sub(pattern,r'\2 \1',s))
# def func(m):
#     return m.group(1).title() + " --" + m.group(2).title()
# print(re.sub(pattern,func,s))

# # 5 爬糗事百科的爬虫
# page = 3
# url = 'https://www.qiushibaike.com/hot/page/' + str(page) + '/'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# heads = {'User-Agent':user_agent}
# try:
#     req = request.Request(url,headers=heads)
#     res = request.urlopen(req)
#     content = res.read().decode('utf-8')
#     # print(content)
#     # rex = '<div.*?clearfix>.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>'
#     rex = '<div.*?"author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>'
#     pattern = re.compile(rex,re.S)
#     patternSub = re.compile('<br/>')
#     items = re.findall(pattern,content)
#     # items = re.finditer(pattern,content)
#     for item in items:
#         item = re.sub(patternSub,'',item)
#         print(item)
#         print(item[1])
#         print("\n")
#     print('end')
# except error.URLError as e:
#     if hasattr(e,'code'):
#         print(e.code)
#     if hasattr(e,'reason'):
#         print(e.reason)

# # 6 完整的糗事百科爬虫
# import threading
# import time
# class QSBK:
#
#     def __init__(self):
#         self.pageindex = 1
#         self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#         self.headers = {'User-Agent':self.user_agent}
#         #存放段子的变量，每一个元素是每一页的段子
#         self.stories = []
#         #存放程序是否继续运行的变量
#         self.enable = False
#
#     #传入某一页的索引获得页面代码
#     def getPage(self,pageIndex):
#         try:
#             url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
#             req = request.Request(url,headers=self.headers)
#             res = request.urlopen(req)
#             pageCode = res.read().decode('utf-8')
#             return pageCode
#         except error.URLError as e:
#             if hasattr(e,'reason'):
#                 print('连接糗事百科失败，reson:' + e.reason)
#                 return None
#
#     def getPageItem(self,pageIndex):
#         pageCode = self.getPage(pageIndex)
#         if not pageCode:
#             print('页面加载失败')
#             return None
#         rex = '<div.*?"author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>'
#         pattern = re.compile(rex,re.S)
#         items = re.findall(pattern,pageCode)
#         pageStories = []
#         for item in items:
#             pageStories.append([item[0],item[1]])
#         return pageStories
#
#     def loadPage(self):
#         if self.enable == True:
#             if len(self.stories) < 2:
#                 #获取新一页
#                 pageStories = self.getPageItem(self.pageindex)
#                 #将该页段子存放到全局list中
#                 if pageStories:
#                     self.stories.append(pageStories)
#                     self.pageindex += 1
#
#     #调用该方法，每次敲回车打印输出一个段子
#     def getOneStory(self,pageStories,page):
#         for story in pageStories:
#             userInput = input()
#             self.loadPage()
#             if userInput == 'Q':
#                 self.enable = False
#                 return
#             print(u'第%d页\t发布人:%s\t%s' % (page,story[0],story[1]))
#
#     #开始方法
#     def start(self):
#         print(u'正在读取糗事百科的段子，按回车查看新段子，Q退出')
#         self.enable = True
#         self.loadPage()
#         nowPage = 0
#         while self.enable:
#             if len(self.stories) > 0:
#                 pageStories = self.stories[0]
#                 nowPage += 1
#                 del self.stories[0]
#                 self.getOneStory(pageStories,nowPage)
#
# spider = QSBK()
# spider.start()

# 7 requests库的用法
# import requests
# r = requests.get('http://cuiqingcai.com')
# print(type(r))
# print(r.status_code)
# print(r.encoding)
# # print(r.cookies)
# #get请求,加上参数
# payload = {'key1':'value1','key2':'value2'}
# head = {'content-type':'application/json'}
# r = requests.get('http://httpbin.org/get',params=payload,headers = head)
# print(r.url)
# #post 请求
# payload = {'key1':'value1','key2':'value2'}
# r = requests.post('http://httpbin.org/post',data=payload)
# print(r.text)
# #json 格式数据
# import json
# url = 'http://httpbin.org/post'
# playload = {'some':'data'}
# r = requests.post(url,data=json.dumps(playload))
# print(r.text)
# # 获得cookies
# url = 'http://httpbin.org/cookies'
# cookies = dict(cookies_are='working')
# r = requests.get(url,cookies=cookies)
# print(r.text)

# #8 beautyful soup用法
# from bs4 import BeautifulSoup
# html = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# <p class="story">...</p>
# """
# soup = BeautifulSoup(html)
# # print(soup.prettify())
# # print(soup.title)
# # print(soup.a)
# # print(soup.p.attrs)
# # print(soup.p['class'])
# # print(soup.p.string)
# # print(soup.head.contents)
# #css选择器
# # print(soup.select('title'))
# # print(soup.select('a'))
# # print(soup.select('b'))
# # print(soup.select('.sister')) #通过类名查找
# # print(soup.select('#link1')) #通过id查找
# # print(soup.select('p #link1')) #组合查找
# # print(soup.select('head > title')) #子标签查找
# # print(soup.select('a[class="sister"]')) #属性查找
# # soup = BeautifulSoup(html,'lxml')
# # print(type(soup.select('title')))
# # print(soup.select('title')[0].get_text())
# # for title in soup.select('title'):
# #     print(title.get_text())

# # 9 selenium 用法
# from selenium import webdriver
#
# chromedriver = r'E:\software\chromedriver_win32\chromedriver.exe'
# # browser = webdriver.Chrome(chromedriver)
# # browser.get('http://www.baidu.com/')
# from selenium.webdriver.common.keys import Keys
#
# # driver = webdriver.Chrome(chromedriver)
# # driver.get('http://www.python.org')
# # assert 'Python' in driver.title
# # elem = driver.find_element_by_name('q')
# # elem.send_keys('pycon')
# # elem.send_keys(Keys.RETURN)
# # print(driver.page_source)
#
# import unittest
#
#
# class PythonOrgSearch(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome(chromedriver)
#
#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get('http://www.python.org')
#         self.assertIn('Python', driver.title)
#         elem = driver.find_element_by_name('q')
#         elem.send_keys('pycon')
#         elem.send_keys(Keys.RETURN)
#         assert 'No results found:' not in driver.page_source
#
#     def tearDown(self):
#         self.driver.close()
#
# if __name__ == "__main__":
#     unittest.main()

# # 10 爬去瓜子二手车
# from bs4 import BeautifulSoup
# import requests
#
# def detailOper(url):
#     web_data = requests.get(url)
#     soup = BeautifulSoup(web_data.text,'lxml')
#     titles = soup.select('div.list > ul > li > div > p.infoBox > a')
#     prices = soup.select('div.list > ul > li > div > p.priType-s > span > i')
#     for title,price in zip(titles,prices):
#         data = {
#             'title':title.get_text(),
#             'detailHerf':title.get('href'),
#             'price':price.get_text().replace(u'万','').replace(' ','')
#         }
#         print(data)
#
# def start():
#     urls = ['http://www.guazi.com/tj/buy/o{}'.format(str(i)) for i in range(1,30,1)]
#     for url in urls:
#         detailOper(url)
#
# if __name__ == '__main__':
#     start()

# # 11 动态爬去斗鱼直播房间信息
# import unittest
# from selenium import webdriver
# from bs4 import BeautifulSoup
#
# path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
# class SeleniumTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.PhantomJS(path)
#
#     def testEle(self):
#         driver = self.driver
#         driver.get('http://www.douyu.com/directory/all')
#         soup = BeautifulSoup(driver.page_source,'lxml')
#         while True:
#             titles = soup.find_all('h3',{'class':'ellipsis'})
#             nums = soup.find_all('span',{'class':'dy-num fr'})
#             for title,num in zip(titles,nums):
#                 print(title.get_text(),num.get_text())
#             if driver.page_source.find('shark-pager-disable-next') != -1:
#                 break
#             elem = driver.find_element_by_class_name('shark-pager-next')
#             elem.click()
#             soup = BeautifulSoup(driver.page_source,'lxml')
#
#     def tearDown(self):
#         print('down')
#
# if __name__ == '__main__':
#     unittest.main()

import requests
from bs4 import BeautifulSoup

def get_url():
    url = 'https://mm.taobao.com/json/request_top_list.htm?page=1'
    req = requests.get(url)
    soup = BeautifulSoup(req.text)
    ladynames = soup.select('a.lady-name')
    for name in ladynames:
        print(name.get('href'))

def show_html():
    # url = 'https://mm.taobao.com/self/model_info.htm?user_id=687471686&is_coment=false'
    url = 'http://mm.taobao.com/self/model_card.htm?user_id=96614110'
    req = requests.get(url)
    print(req.text)

if __name__ == '__main__':
    # get_url()
    # show_html()
