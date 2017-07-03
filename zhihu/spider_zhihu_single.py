#单线程知乎爬虫，因为知乎对单个IP访问有限制，改为单线程
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import time
from zhihu.db_tool import DBUtil
from zhihu.spider_status import  Status
from datetime import  datetime
import threading
import  requests
from zhihu import spider_const
from zhihu.spider_const import log
from zhihu.spider_const import loge
import re


base_url = r'https://www.zhihu.com/people/{0}/following'

class ZhiHuSpider():

    def __init__(self):
        self.code_success = 200             #抓取成功
        self.code_failure = 201             #抓取失败
        self.code_user_not_exist = 202      #用户不存在，僵尸粉
        self.code_user_not_useful = 203     #用户没有价值
        self.code_following_none = 204      #用户没有关注任何人
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
                driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
                driver.implicitly_wait(self.time_wait)
                driver.get(url)
                # 保存图片
                # dt = datetime.now()
                # fileName = dt.strftime('%Y-%m-%d_%H-%M-%S') + ".jpg"
                # driver.save_screenshot(fileName)
                error = driver.page_source.find('你似乎来到了没有知识存在的荒原...')
                # 404界面
                if error != -1:
                    dict['code'] = self.code_user_not_exist
                else:
                    elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
                    elem.send_keys(Keys.ENTER)
                    #解析用户信息
                    dictResult = self.parseUserInfo(driver.page_source)
                    #解析用户个人成就
                    dictAchieve = self.parseAchieve(driver.page_source)
                    dict.update(dictResult)
                    dict.update(dictAchieve)
                break
            except Exception as e:
                loge(e)
                count = count + 1
                log('发生异常，尝试第{0}次重试, user_id={1}'.format(count, userId))
            finally:
                driver.close()
                log('进入{0}秒休眠'.format(self.time_duration))
                time.sleep(self.time_duration)
                log('{0}秒休眠结束'.format(self.time_duration))
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
        image = image.replace('xl','r') #转换为原始图片地址
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
                location = location.replace('现居','')
                location = location.strip()
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

    #解析个人成就
    def parseAchieve(self,content):
        dict = {}
        if content is None:
            return dict
        p = pq(content)
        card = p('div.Profile-sideColumnItem')
        for item in card.items():
            pTitle = item('div.IconGraf')
            title = pTitle.text()
            if title == '优秀回答者':
                topic = item('div.Profile-sideColumnItemValue').text()
                dict['is_excellent_answer'] = True
                dict['excellent_topic'] = topic
                log('优秀回答者：topic=' + topic)
            elif title[:4] == '知乎收录':
                record_num = re.sub('\D', "", title)
                record_by = item('div.Profile-sideColumnItemValue').text()
                dict['record_num'] = record_num
                dict['record_by'] = record_by
                log('知乎收录{0}个答案, {1}'.format(record_num, record_by))
            elif title[:2] == '获得':
                # 获得xx次赞同
                applaud_num = re.sub('\D', '', title)
                itemContent = item('div.Profile-sideColumnItemValue').text()
                # 获得感谢的次数
                pattern = re.compile(r'获得\s?(\d+)\s?次感谢')
                result = re.search(pattern, itemContent)
                gratitude_num = result.groups()[0] if result else 0
                # 获得收藏的次数
                pattern2 = re.compile(r'(\d+)\s?次收藏')
                result2 = re.search(pattern2, itemContent)
                collect_num = result2.groups()[0] if result2 else 0
                dict['applaud_num'] = applaud_num
                dict['gratitude_num'] = gratitude_num
                dict['collect_num'] = collect_num
                log('获得{0}次称赞，{1}次感谢，{2}次收藏'.format(applaud_num, gratitude_num, collect_num))
            elif title[:2] == '参与':
                public_edit_num = re.sub('\D', '', title)
                dict['public_edit_num'] = public_edit_num
                log('参与{0}次公共编辑'.format(public_edit_num))
        return dict

    #获取用户关注的人
    def getUserFollowing(self,userId):
        list = []
        code = self.code_success
        try:
            url = base_url.format(userId)
            driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
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
        except Exception as e:
            loge(e)
        finally:
            driver.close()
        return list

    #获取用户关注的人的页数
    def getUserFollowingPageNum(self,userId):
        page = 0
        if userId is None or userId == '':
            return page
        try:
            url = base_url.format(userId)
            driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
            driver.get(url)
            p = pq(driver.page_source)
            # 先判断有没有TA关注的人
            count = p('div.List-item').size()
            if count == 0:
                page = 0
            else:
                #再拿到页码数
                page = p('div.Pagination button:not(.PaginationButton-next):last').text()
                #处理只有一页的情况
                if page == '':
                    page = 1
                else:
                    page = int(page)
        except Exception as e:
            loge(e)
            page = 0
        finally:
            driver.close()
        return page

    #获取指定页的关注者
    def getUserFollowingPageContent(self,userId,page):
        list = []
        if page == 0:
            return list
        url = base_url.format(userId)
        url = '{0}?page={1}'.format(url,page)
        try:
            driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
            # driver.implicitly_wait(self.time_wait)
            driver.get(url)
            p = pq(driver.page_source)
            links = p('div.List-item div.ContentItem-head div.Popover a.UserLink-link')
            for link in links.items():
                userHerf = link.attr('href')
                if userHerf is None or userHerf == '':
                    continue
                list.append(userHerf[8:])
        except Exception as e:
            list.clear()
            loge(e)
        finally:
            driver.close()
        return list

    def catchUserInfoThread(self):
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
            #获取用户信息
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
                d.saveAchieveInfo(userId,dict)

    def catchUserFollowingThread(self):
        s = ZhiHuSpider()
        d = DBUtil()
        st = Status.Following()
        while True:
            #取出第一个用户
            userId,currentPage = d.getFirstUserToFollowing2()
            log('开始抓取用户关注者,user_id={0}, current_page={1}'.format(userId,currentPage))
            if userId is None:
                time.sleep(3)
                continue
            d.setUserIsFollowing(userId,st.is_catching)
            #获取关注者页数
            total = self.getUserFollowingPageNum(userId)
            log('当前用户总的关注者的页数，user_id={0}, total_page={1}'.format(userId,total))
            #用户没有关注任何人
            if total == 0:
                d.setUserIsFollowing(userId,st.user_following_none)
                continue
            for i in range(currentPage+1,total+1):
                list = self.getUserFollowingPageContent(userId,i)
                #获取关注者成功
                if len(list) > 0:
                    d.saveFollowerInfo(userId,list)
                    #设置状态
                    d.setUserIsFollowing(userId,st.is_catching)
                #设置这一页抓取完毕了
                d.setUserFollowingPage(userId,i)
                log('抓取完一页用户的关注者，user_id={0}, page={1}, list.size={2}'.format(userId,i,len(list)))
                time.sleep(self.time_duration)
            #设置抓取完毕
            d.setUserIsFollowing(userId,st.catched)
            log('当前用户全部抓取完毕，user_id=%s' % userId)

    def start(self):
        t1 = threading.Thread(target=self.catchUserInfoThread)
        t2 = threading.Thread(target=self.catchUserFollowingThread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == '__main__':
    d = DBUtil()
    d.init('excited-vczh')
    z = ZhiHuSpider()
    z.start()
