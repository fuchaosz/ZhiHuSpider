#多线程知乎爬虫
import multiprocessing
from zhihu.spider_zhihu_single import ZhiHuSpider
from zhihu.db_tool import DBUtil
from zhihu.spider_status import Status
import time
import os
import threading
from zhihu.spider_const import log

class ZhiHuThreadSpider():

    def __init__(self):
        self.thread_num = 3        #线程数量
        pass

    #多线程抓取用户信息
    def catchUserInfoThread(self,lock):
        s = ZhiHuSpider()
        db = DBUtil()
        st = Status.Catch()
        while True:
            #加锁
            lock.acquire()
            #获取第一个用户开始爬
            userId = db.getFirstUserToCatch()
            if userId is None:
                lock.release()
                time.sleep(3)
                continue
            #设置为正在爬取
            db.setUserIsCatch(userId,st.is_catching)
            lock.release()
            log('开始爬取用户，pid={1}, user_id={0}'.format(os.getpid(),userId))
            #开始爬取用户信息
            dict = s.getUserInfo(userId)
            code = dict['code']
            # 用户没有价值
            if code == s.code_user_not_useful:
                log('用户没有价值,pid={1}, user_id={0}'.format(os.getpid(),userId))
                db.setUserIsCatch(userId, st.user_not_useful)
            # 用户不存在
            elif code == s.code_user_not_exist:
                log('用户不存在，是僵尸粉,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.setUserIsCatch(userId, st.user_not_exist)
            # 抓取失败
            elif code == s.code_failure:
                log('用户抓取失败,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.setUserIsCatch(userId, st.failed)
            # 抓取成功
            else:
                log('用户抓取成功,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.updateUserInfo(userId, dict)

    #单线程获取用户
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
            total = s.getUserFollowingPageNum(userId)
            log('当前用户总的关注者的页数，user_id={0}, total_page={1}'.format(userId,total))
            #用户没有关注任何人
            if total == 0:
                d.setUserIsFollowing(userId,st.user_following_none)
                continue
            for i in range(currentPage+1,total+1):
                list = s.getUserFollowingPageContent(userId,i)
                #获取关注者成功
                if len(list) > 0:
                    d.saveFollowerInfo(userId,list)
                    #设置状态
                    d.setUserIsFollowing(userId,st.is_catching)
                #设置这一页抓取完毕了
                d.setUserFollowingPage(userId,i)
                log('抓取完一页用户的关注者，user_id={0}, page={1}, list.size={2}'.format(userId,i,len(list)))
                time.sleep(s.time_duration)
            #设置抓取完毕
            d.setUserIsFollowing(userId,st.catched)
            log('当前用户全部抓取完毕，user_id= %s' % userId)

    def testProess(self,lock):
        while True:
            log('count={0},pid={1}'.format(self.count,os.getpid()))
            time.sleep(3)

    def getThreadId(self):
        return threading.current_thread().ident

    def start(self):
        #创建线程
        spiderThreads = []
        followingThread = threading.Thread(target=self.catchUserFollowingThread)
        spiderThreads.append(followingThread)
        lock = threading.Lock()
        for i in range(0,self.thread_num):
            th = threading.Thread(target=self.catchUserInfoThread,args=(lock,))
            spiderThreads.append(th)
        #启动线程
        [th.start() for th in spiderThreads]
        #等待线程结束
        [th.join() for th in spiderThreads]

if __name__ == '__main__':
    d = DBUtil()
    d.init('excited-vczh')
    z = ZhiHuThreadSpider()
    z.start()