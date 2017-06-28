#多进程知乎爬虫
import multiprocessing
from zhihu.spider_zhihu_single import ZhiHuSpider
from zhihu.db_tool import DBUtil
from zhihu.spider_status import Status
import time
import os

class ZhiHuMultiSpider():

    def __init__(self):
        self.process_num = 2        #进程数量
        pass

    def catchUserInfoProcess(self,lock):
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
            print('开始爬取用户，pid={1}, user_id={0}'.format(os.getpid(),userId))
            #开始爬取用户信息
            dict = s.getUserInfo(userId)
            code = dict['code']
            # 用户没有价值
            if code == s.code_user_not_useful:
                print('用户没有价值,pid={1}, user_id={0}'.format(os.getpid(),userId))
                db.setUserIsCatch(userId, st.user_not_useful)
            # 用户不存在
            elif code == s.code_user_not_exist:
                print('用户不存在，是僵尸粉,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.setUserIsCatch(userId, st.user_not_exist)
            # 抓取失败
            elif code == s.code_failure:
                print('用户抓取失败,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.setUserIsCatch(userId, st.failed)
            # 抓取成功
            else:
                print('用户抓取成功,pid={1}, user_id={0}'.format(os.getpid(), userId))
                db.updateUserInfo(userId, dict)

    def catchUserFollowingProcess(self,lock):
        z = ZhiHuSpider()
        d = DBUtil()
        st = Status.Following()
        while True:
            lock.acquire()
            # 取出第一个用户
            userId, currentPage = d.getFirstUserToFollowing2()
            print('开始抓取用户关注者,user_id={0}, current_page={1}'.format(userId, currentPage))
            if userId is None:
                lock.release()
                time.sleep(3)
                continue
            d.setUserIsFollowing(userId, st.multi_catching)
            lock.release()
            # 获取关注者页数
            total = z.getUserFollowingPageNum(userId)
            print('当前用户总的关注者的页数，user_id={0}, total_page={1}'.format(userId, total))
            # 用户没有关注任何人
            if total == 0:
                d.setUserIsFollowing(userId, st.user_following_none)
                continue
            for i in range(currentPage + 1, total + 1):
                list = z.getUserFollowingPageContent(userId, i)
                # 获取关注者成功
                if len(list) > 0:
                    d.saveFollowerInfo(userId, list)
                # 设置这一页抓取完毕了
                d.setUserFollowingPage(userId, i)
                print('抓取完一页用户的关注者，user_id={0}, page={1}, list.size={2}'.format(userId, i, len(list)))
                time.sleep(z.time_duration)
            # 设置抓取完毕
            d.setUserIsFollowing(userId, st.catched)
            print('当前用户全部抓取完毕，user_id=', userId)

    def testProess(self,lock):
        while True:
            print('count={0},pid={1}'.format(self.count,os.getpid()))
            time.sleep(3)

    def start(self):
        pool = multiprocessing.Pool(self.process_num)
        m = multiprocessing.Manager()
        l = m.Lock()
        for i in range(self.process_num):
            pool.apply_async(self.catchUserInfoProcess,(l,))
        pool.close()
        pool.join()

if __name__ == '__main__':
    z = ZhiHuMultiSpider()
    z.start()