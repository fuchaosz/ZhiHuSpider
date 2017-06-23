# 知乎爬虫
import requests
import os
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from pyquery import PyQuery as pq
import multiprocessing
import pymysql
import time
from zhihu import proxy_tool

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
conn_arg = {'host':'localhost','user':'root','password':'root','db':'zhihu','port':3306,'charset':'utf8'}

# 采用selenium模拟浏览器来访问,从而获取更多用户详细信息
def getUserInfo(userId,queue):
    dict = {}
    #构造用户信息页面的url
    url = base_url.format(userId)
    dict['user_id'] = userId
    dict['url'] = url
    dict['code'] = 200
    count = 0
    while count < 3:
        try:
            #取一个代理
            item = queue.get()
            print('取出一个代理IP开始抓取，pid={0} ip={1}'.format(os.getpid(),item))
            proxy = Proxy(
                {
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': '{0}:{1}'.format(item[0],item[1])
                }
            )
            desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
            proxy.add_to_capabilities(desired_capabilities)
            driver = webdriver.PhantomJS(executable_path=path,desired_capabilities=desired_capabilities)
            driver.implicitly_wait(count * 3)
            driver.get(url)
            error = driver.page_source.find('你似乎来到了没有知识存在的荒原...')
            #404界面
            if error:
                dict['code'] = 404
                return dict
            elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
            elem.send_keys(Keys.ENTER)
            p = pq(driver.page_source)
            break
        except Exception as e:
            print(e)
            count = count + 1
            print('发生异常，尝试第{0}次抓取, pid = {1}, user_id = {2}'.format(count + 1, os.getpid(), userId))
        finally:
            driver.close()
    #尝试次数超过3次，那么认为抓取失败
    if count >= 3:
        dict['code'] = 406
        return dict
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
        dict['code'] = 405
        return dict
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

def getUserInfoMultiProcess(lock,queue):
    db = DBUtil()
    while not is_exit:
        lock.acquire()
        #从数据库中取出第一个没有被抓的用户
        user_id = db.getFirstUserToCatch()
        #如果没有获取到可以被抓取的用户，则休眠3秒后继续
        if not user_id:
            print('没有获取到要爬取的用户，休眠3秒,pid=',os.getpid())
            lock.release()
            time.sleep(3)
            continue
        #开始抓取这个用户之前，设置这个用户的状态为正在抓取
        db.setUserIsCatch(user_id,2)
        lock.release()
        print("开始抓取用户信息,pid={0}, use_id={1}".format(os.getpid(),user_id))
        #获取这个用户的信息
        try:
            dict = getUserInfo(user_id,queue)
        except Exception as e:
            print('抓取用户信息时发生异常 userId = ',user_id)
            #设置这个用户表示抓取失败
            db.setUserIsCatch(user_id,4)
            print(e)
            continue
        # 获取用户没有价值，则继续
        code = dict['code']
        if code == 405:
            print('抓到的用户没有价值，pid = {0}, user_id = {1}'.format(os.getpid(),user_id))
            #标记该用户没有价值
            db.setUserIsCatch(user_id,3)
        elif code == 404:
            print('抓到了僵尸粉，pid = {0}, user_id = {1}'.format(os.getpid(),user_id))
            db.setUserIsCatch(user_id,5)
        elif code == 406:
            print('尝试3次后抓取用户仍然失败，pid = {0}, user_id={1}'.format(os.getpid(),user_id))
            db.setUserIsCatch(user_id,4)
        else:
            # 将用户信息保存到数据库
            db.updateUserInfo(user_id,dict)
            print("抓取的用户信息成功保存到数据库，pid = {0}, user_id = {1}".format(os.getpid(),user_id))

def getUserFollwingMultiProcess(lock):
    db = DBUtil()
    while not is_exit:
        lock.acquire()
        #取出一个用户，获取他的关注者
        user_id = db.getFirstUserToFollowing()
        #没有取到用户则休眠3秒后继续
        if not user_id:
            # print('没有获取到关注者，休眠3秒')
            lock.release()
            time.sleep(3)
            continue
        #设置状态为正在爬取
        db.setUserIsFollowing(user_id,2)
        lock.release()
        # print("开始获取关注者: pid={0},user_id={1}".format(os.getpid(),user_id))
        try:
            list = getAllFollowers(user_id)
        except Exception  as e:
            # print('获取用户的关注者发生异常，user_id = ',user_id)
            print(e)
            #设置爬去该用户关注的人失败
            db.setUserIsFollowing(user_id,4)
            continue
        #list不为空，保存到数据库
        if list:
            db.saveFollowerInfo(user_id,list)
            print("获取关注者成功:pid={0},user_id={1}".format(os.getpid(),user_id))
        #设置状态为已经爬取了
        db.setUserIsFollowing(user_id,1)

#抓取代理IP，检测后放入队列
def getProxyIpQueue(queue):
    p = proxy_tool.ProxyTool()
    print('抓取代理IP的进程,pid = ',os.getpid())
    while True:
        list = p.getProxyIpByFile()
        time_1 = time.time()
        for item in list:
            if p.detectProxyIP(item[0],item[1]):
                print('发现一个有效代理并入队：',item)
                queue.put(item)
        time_2 = time.time()
        durtion = (5 * 60) - (time_2 - time_1)
        print('抓取IP代理的进程，抓完一轮ip，pid={0}, duration={1}'.format(os.getpid(),durtion))
        #必须满5分钟后再抓下一次
        if durtion > 0:
            print('抓取IP的进程进入休眠,duration = ',durtion)
            time.sleep(durtion)

def mainProcess():
    num_1 = 5
    num_2 = 1
    m = multiprocessing.Manager()
    q = m.Queue()
    lock_1 = m.Lock()
    lock_2 = m.Lock()
    # 创建进程池
    pool1 = multiprocessing.Pool(num_1)
    pool2 = multiprocessing.Pool(num_2)
    for i in range(num_1):
        pool1.apply_async(getUserInfoMultiProcess,(lock_1,q))
    for i in range(num_2):
        # pool2.apply_async(getUserFollwingMultiProcess,(lock_2,))
        pool2.apply_async(getProxyIpQueue,(q,))
    pool1.close()
    pool1.join()
    pool2.close()
    pool2.join()

def init():
    # 首先插入一个初始化用户
    try:
        sql = "insert into user(user_id) values('%s')" % start_user_id
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#数据库操作类
class DBUtil(object):

    def __init__(self):
        # self.conn = pymysql.connect(host='localhost',user='root',password='root',db='zhihu',port=3306,charset='utf8')
        pass

    def __del__(self):
        if self.conn:
            self.conn.close()

    def openMySql(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', db='zhihu', port=3306,charset='utf8')

    def closeMySql(self):
        if self.conn:
            self.conn.close()

    # 从数据库取出第一个没有被抓取的用户
    def getFirstUserToCatch(self):
        result = None
        try:
            self.openMySql()
            sql = "select * from user where is_catch=0 order by id"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            if res:
                result = res[1]
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.closeMySql()
        # print('获取第一个没有被抓取的用户,user_id=', result)
        return result

    # 设置用户是否被抓取，0表示未被抓取，1表示已抓取，2表示正在抓取,3表示用户没有价值,4表示抓取失败
    def setUserIsCatch(self,user_id, status):
        try:
            self.openMySql()
            sql = "update user set is_catch=%d where user_id='%s'" % (status, user_id)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            # print('用户状态设置成功,user_id=%s  is_catch=%d' % (user_id, status))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.closeMySql()

    # 更新用户详细信息到数据库
    def updateUserInfo(self,user_id, dict):
        if not dict:
            return
        try:
            self.openMySql()
            # update user u set u.name='轮子哥2',u.image='www.baidu.com',u.sex='男',u.sign='个性签名',u.location='西雅图',u.major='软件',u.job='谷歌',u.education='xx大学',u.info='个人信息',u.is_catch=1 where u.user_id='vch2'
            sql = "update user u set u.name='%s',u.image='%s',u.sex='%s',u.sign='%s',u.location='%s',u.major='%s',u.job='%s',u.education='%s',u.info='%s',url_following='%s',u.is_catch=1 where u.user_id='%s'"
            sql = sql % (
            dict.get('name'), dict.get('image', ""), dict.get('sex'), dict.get('sign', ''), dict.get('location', ''),
            dict.get('major', ''), dict.get('job', ''), dict.get('education', ''), dict.get('info', ''),dict.get('url',''),user_id)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            # print('更新用户信息到数据库成功，user_id=%s' % user_id)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.closeMySql()

    # 获取第一个用户的账户
    def getFirstUserToFollowing(self):
        result = None
        try:
            self.openMySql()
            sql = 'select * from user where is_following=0 order by id'
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            result = res[1]
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.closeMySql()
        # print('获取第一个没有爬取关注者的用户，pid = {0}, user_id={1}'.format(os.getpid(),result))
        return result

    # 设置是否抓取用户关注的人的标志，0表示已抓取，1表示未抓取
    def setUserIsFollowing(self,user_id, status):
        try:
            self.openMySql()
            sql = "update user set is_following=%d where user_id='%s'" % (status, user_id)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            # print('用户is_following设置成功,user_id=%s  is_following=%d' % (user_id, status))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.closeMySql()

    # 保存用户关注信息到数据库
    def saveFollowerInfo(self,user_id, follower_list):
        if not user_id or not follower_list:
            return
        self.openMySql()
        cursor = self.conn.cursor()
        for item in follower_list:
            try:
                sql = "insert into follow(user_id,follower_id) values('%s','%s')" % (user_id, item)
                cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print('保存用户关注信息，插入follow表发生异常,pid = ',os.getpid())
                print(e)
        for item in follower_list:
            try:
                sql = "insert into user(user_id) values('%s')" % item
                cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                pass
        cursor.close()
        self.closeMySql()

def test():
    # url = 'https://www.zhihu.com/people/wang-si-cong-shi-shui-20/answers'
    # url = 'https://www.zhihu.com/tang-que'
    # driver = webdriver.PhantomJS(executable_path=path)
    # driver.get(url)
    # p = pq(driver.page_source)
    # error = driver.page_source.find('你似乎来到了没有知识存在的荒原...')
    # # error = p('div.error')
    # if error:
    #     print('404界面')
    # else:
    #     print('正常界面')
    time_1 = time.time()
    time.sleep(5)
    time_2 = time.time()
    print(time_2 - time_1)

if __name__ == '__main__':
    # init()
    #开启多进程
    mainProcess()
    # test()
