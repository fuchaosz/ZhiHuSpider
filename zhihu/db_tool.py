#数据库操作类
import pymysql

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
        print('获取第一个没有被抓取的用户,user_id=', result)
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
            print('更新用户信息到数据库成功，user_id=%s' % user_id)
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
        print('获取第一个没有爬取关注者的用户, user_id={0}'.format(result))
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
                print('保存用户关注信息，插入follow表发生异常,user_id = ',user_id)
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