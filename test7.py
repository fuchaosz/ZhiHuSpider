#!user/bin/env python3
# -*- coding: utf-8 -*-
#测试数据库
import pymysql
from zhihu.spider_zhihu_single import ZhiHuSpider
from zhihu.db_tool import DBUtil

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='zhihu',
    port=3306,
    charset='utf8mb4'
)

def test():
    try:
        cursor = conn.cursor()
        str = "Hello 'sdsd'"
        # sql = 'insert into user(user_id,info) VALUES("{0}","{1}")'.format('aaaa',str)
        sql = "insert into user(user_id,info) VALUES('{0}','{1}')".format('aaaa_1', str)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def test2():
    s = ZhiHuSpider()
    db = DBUtil()
    user_id = 'guang-ying-31-41'
    dict = s.getUserInfo(user_id)
    db.updateUserInfo(user_id,dict)

def test3():
    try:
        str ='''
       可爱又迷人的反派角色。 掌管黄道十二星座第一宫。 游戏控：RTS，RAC，(MMO)RPG，沙盒，部分动作类，惊悚恐怖冒险类，部分射击类，游戏剧情控。 角色属性：守序邪恶。(๑‾ ꇴ ‾๑) 喜欢游戏的亲们可以一起交流~(´///ω/// `) 最近沉迷《最终幻想14》中。。。。|ω･`) 有一枚红宝石戒指；我觉得它有魔法。 DC粉~(●'◡'●)ﾉ❤ 熊猫粉~ (๛ ˘ ³˘) ❤ 猫咪粉~(●'◡'●)ﾉ❤ 爵士~ヾ(๑╹ヮ╹๑)ﾉ"❤ 努力做一个可爱并且有趣的人。 不爱说话。超级好性格。 愿遇到一个可以一直对我温柔以待的人。 偶尔，会写一些奇奇怪怪的东西。(◉ ω ◉｀)
        '''
        str = str.replace("'", "\\\'")
        str = str.replace('"', '\\\"')
        sql = "insert into test VALUE ('{0}')".format(str)
        cursor = conn.cursor()
        cursor.execute('set names utf8mb4')
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def test4():
    try:
        sql = 'select * from test'
        cursor = conn.cursor()
        cursor.execute('set names utf8mb4')
        cursor.execute(sql)
        list = cursor.fetchall()
        for item in list:
            print(item[0])
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # test()
    test2()
    # test3()
    # test4()