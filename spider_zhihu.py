# 知乎爬虫
import requests
import os
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import multiprocessing
import pymysql

start_user = r'https://www.zhihu.com/people/excited-vczh/following'  # 第一个用户,获取信息的入口
path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
start_user_id = 'excited-vczh'
base_url = r'https://www.zhihu.com/people/{0}/following'
is_exit = False #控制退出的开关
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='zhihu',
    port=3306,
    charset='utf8'
)

# 采用selenium模拟浏览器来访问,从而获取更多用户详细信息
def getUserInfo(userId):
    dict = {}
    #构造用户信息页面的url
    url = base_url.format(userId)
    dict['user_id'] = userId
    dict['url'] = url
    driver = webdriver.PhantomJS(executable_path=path)
    driver.get(url)
    elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
    elem.send_keys(Keys.ENTER)
    p = pq(driver.page_source)
    #先抓固定的，所有页面都一定有的信息，即使抓不到也只会是空，不会报错
    image = p('img.UserAvatar-inner').eq(0).attr('src') #用户头像
    name = p('span.ProfileHeader-name').text() #姓名
    sex = '男' if p('a.is-active').text().split()[0] == '他' else '女'  # 用户性别
    sign = p('span.ProfileHeader-headline').text()  # 个性签名
    dict['image'] = image
    dict['name'] = name
    dict['sex'] = sex
    dict['sign'] = sign
    #如果连个性签名都没有，那一定是个没有什么价值的用户,其他信息也一定不全，不抓了
    if sign is None:
        return None
    #下面抓不是固定的，可能有的人没有填写
    detailItems = p('div.ProfileHeader-detailItem')
    #下面遍历每一条信息
    for item in detailItems.items():
        itemName = item('span.ProfileHeader-detailLabel').text()
        if itemName == '居住地':
            location = item.find('div.ProfileHeader-detailValue span').text()
            dict['location'] = location
        elif itemName == '所在行业':
            major = item('div.ProfileHeader-detailValue').text()
            dict['major'] = major
        elif itemName == '职业经历':
            job = item('div.ProfileHeader-field').text()
            dict['job'] = job;
        elif itemName == '教育经历':
            education = item('div.ProfileHeader-field').text()
            dict['education'] = education
        elif itemName == '个人简介':
            info = item('div.ProfileHeader-detailValue').text()
            dict['info'] = info
    return dict

#获取所有关注者的id
def getAllFollowers(userId):
    list = []
    url = base_url.format(userId)
    driver = webdriver.PhantomJS(executable_path=path)
    driver.get(url)
    p = pq(driver.page_source)
    # #先拿到页码数
    page = p('div.Pagination button:not(.PaginationButton-next):last').text()
    #遍历每一个关注页
    # for i in range(1,int(page)+1):
    for i in range(1, 2):
        url = "{0}?page={1}".format(url,i)
        driver.get(url)
        p = pq(driver.page_source)
        links = p('div.List-item div.ContentItem-head div.Popover a.UserLink-link')
        for link in links.items():
            userHerf = link.attr('href')
            if userHerf is None or userHerf == '':
                continue
            list.append(userHerf[8:])
    return  list

def getUserInfoMultiProcess(queue_user_id):
    while not is_exit:
        print('获取用户信息进程pid=',os.getpid())
        #从队列中取出一个用户信息来
        user_id = queue_user_id.get()
        #获取这个用户的信息
        try:
            print('开始获取用户信息,user_id='+user_id)
            dict = getUserInfo(user_id)
            print('获取用户信息完毕,user_id='+user_id)
        except Exception as e:
            #发生异常了还是继续，不管
            print('抓取用户信息时发生异常 userId = ',user_id)
            print(e)
            continue
        # 获取用户没有价值，则继续
        if dict is None:
            print('抓到的用户没有价值，user_id = ',user_id)
            continue
        # 将用户信息保存到数据库
        print(dict)

def getUserFollwerMultiProcess(queue_user_id,queue_follwer_id):
    while not is_exit:
        print('获取关注者进程pid=',os.getpid())
        #取出一个用户，获取他的关注者
        user_id = queue_follwer_id.get()
        try:
            print('开始获取关注者,user_id='+user_id)
            list = getAllFollowers(user_id)
            print('获取关注者完毕,user_id='+user_id)
        except Exception  as e:
            print('获取用户的关注者发生异常，user_id = ',user_id)
            print(e)
            continue
        #list为空，则继续
        if not list:
            continue
        #list不为空，则将该用户加入列表
        for item in list:
            queue_user_id.put(item)
            queue_follwer_id.put(item)
        print('以下关注{0}的用户入队：'.format(user_id))
        print(list)

#保存用户信息到数据库
def saveUserInfo(dict):
    if not dict:
        return
    with conn.cursor() as cursor:
        sql = "insert into user(user_id,name,image,sex,sign,location,major,job,education,info) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        sql = sql % (dict.get('user_id'),dict.get('name'),dict.get('image',""),dict.get('sex'),dict.get('sign',''),dict.get('location',''),dict.get('major',''),dict.get('job',''),dict.get('education',''),dict.get('info',''))
        cursor.execute(sql)
        cursor.commit()
        print('保存用户信息到数据库成功，user_id=%s' % dict['user_id'])

#保存用户关注信息到数据库
def saveFollowerInfo(user_id,follower_list):
    if not user_id or not follower_list:
        return
    with conn.cursor() as cursor:
        sql = "insert into follow(user_id,follower_id) values('%','vch2')"


def mainProcess():
    #创建进程池
    pool_user = multiprocessing.Pool(10)
    pool_follower = multiprocessing.Pool(5)
    #创建进程间通信的队列
    queue_user_id = multiprocessing.Manager().Queue(100)
    queue_follwer_id = multiprocessing.Manager().Queue(100)
    #初始化队列
    queue_follwer_id.put(start_user_id)
    queue_user_id.put(start_user_id)
    for i in range(10):
        pool_user.apply_async(getUserInfoMultiProcess,args=(queue_user_id,))
    for i in range(5):
        pool_follower.apply_async(getUserFollwerMultiProcess, args=(queue_user_id, queue_follwer_id))
    pool_user.close()
    pool_follower.close()
    pool_user.join()
    pool_follower.join()

if __name__ == '__main__':
    # getUserInfo('teeny-tiny')
    # getUserInfo(start_user_id)
    # getAllFollowers(start_user_id)
    mainProcess()