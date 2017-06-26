#单线程知乎爬虫，因为知乎对单个IP访问有限制，改为单线程
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import time
from zhihu.db_tool import DBUtil
from zhihu.spider_status import  Status
from datetime import  datetime
import threading

path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
base_url = r'https://www.zhihu.com/people/{0}/following'

class ZhiHuSpider():

    def __init__(self):
        self.code_success = 200             #抓取成功
        self.code_failure = 201             #抓取失败
        self.code_user_not_exist = 202      #用户不存在，僵尸粉
        self.code_user_not_useful = 203     #用户没有价值
        self.time_duration = 30             #抓完一次的间隔，默认30秒
        self.time_wait = 10                 #抓之前等待页面加载的时间
        pass

    def getUserInfo(self,userId):
        dict = {}
        # 构造用户信息页面的url
        url = base_url.format(userId)
        dict['user_id'] = userId
        dict['url'] = url
        dict['code'] = self.code_success
        count = 0
        while count < 3:
            try:
                driver = webdriver.PhantomJS(executable_path=path)
                driver.implicitly_wait(self.time_wait)
                driver.get(url)
                # 保存图片
                dt = datetime.now()
                fileName = dt.strftime('%Y-%m-%d_%H-%M-%S') + ".jpg"
                driver.save_screenshot(fileName)
                error = driver.page_source.find('你似乎来到了没有知识存在的荒原...')
                # 404界面
                if error != -1:
                    dict['code'] = self.code_user_not_exist
                else:
                    elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
                    elem.send_keys(Keys.ENTER)
                    dictResult = self.parseUserInfo(driver.page_source)
                    dict.update(dictResult)
                break
            except Exception as e:
                print(e)
                count = count + 1
                print('发生异常，尝试第{0}次抓取, user_id={1}'.format(count + 1, userId))
            finally:
                driver.close()
                print('进入{0}秒休眠'.format(self.time_duration))
                time.sleep(self.time_duration)
                print('{0}秒休眠结束'.format(self.time_duration))
        # 尝试次数超过3次，那么认为抓取失败
        if count >= 3:
            dict['code'] = self.code_failure
        return dict

    #解析用户内容
    def parseUserInfo(self,content):
        dict = {}
        if content is None:
            dict['code'] = self.code_failure
            return dict
        p = pq(content)
        # 先抓固定的，所有页面都一定有的信息，即使抓不到也只会是空，不会报错
        image = p('img.UserAvatar-inner').eq(0).attr('src')  # 用户头像
        name = p('span.ProfileHeader-name').text()  # 姓名
        sex = '男' if p('a.is-active').text().split()[0] == '他' else '女'  # 用户性别
        sign = p('span.ProfileHeader-headline').text()  # 个性签名
        dict['image'] = image
        dict['name'] = name
        dict['sex'] = sex
        dict['sign'] = sign
        # 如果连个性签名都没有，那一定是个没有什么价值的用户,其他信息也一定不全，不抓了
        if sign is None:
            dict['code'] = self.code_user_not_useful
            return dict
        # 下面抓不是固定的，可能有的人没有填写
        detailItems = p('div.ProfileHeader-detailItem')
        # 下面遍历每一条信息
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

    #获取用户关注的人
    def getUserFollowing(self,userId):
        list = []
        url = base_url.format(userId)
        driver = webdriver.PhantomJS(executable_path=path)
        driver.get(url)
        p = pq(driver.page_source)
        # #先拿到页码数
        page = p('div.Pagination button:not(.PaginationButton-next):last').text()
        # 遍历每一个关注页
        # for i in range(1,int(page)+1):
        for i in range(1, 2):
            url = "{0}?page={1}".format(url, i)
            driver.get(url)
            p = pq(driver.page_source)
            links = p('div.List-item div.ContentItem-head div.Popover a.UserLink-link')
            for link in links.items():
                userHerf = link.attr('href')
                if userHerf is None or userHerf == '':
                    continue
                list.append(userHerf[8:])
        return list

def catchUserInfoThread():
    s = ZhiHuSpider()
    d = DBUtil()
    st = Status.Catch()
    while True:
        #取出第一个用户
        userId = d.getFirstUserToCatch()
        if userId is None:
            time.sleep(3)
            continue
        d.setUserIsCatch(userId,st.is_catching)
        dict = s.getUserInfo(userId)
        code = dict['code']
        #用户没有价值
        if code == s.code_user_not_useful:
            d.setUserIsCatch(userId,st.user_not_useful)
        #用户不存在
        elif code == s.code_user_not_exist:
            d.setUserIsCatch(userId,st.user_not_exist)
        #抓取失败
        elif code == s.code_failure:
            d.setUserIsCatch(userId,st.failed)
        #抓取成功
        else:
            d.updateUserInfo(userId,dict)

def test():
    dt = datetime.now()
    str = dt.strftime( '%Y-%m-%d_%H-%M-%S') + '.jpg'
    print(str)

if __name__ == '__main__':
    t = threading.Thread(target=catchUserInfoThread)
    t.start()
    t.join()
    # test()