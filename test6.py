#抓取个人成就
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

def test():
    # url = 'https://www.zhihu.com/people/cloudycity/following'
    # driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
    # driver.get(url)
    # p = pq(driver.page_source)
    # file = open('test.html', mode='rb')
    # conten = file.read().decode('utf-8')
    # p = pq(conten)
    # print(p.outer_html)
    # file = open('test.html',mode='r',encoding='utf-8')
    # p = pq(file.read())
    db = DBUtil()
    userList = []
    try:
        db.openMySql()
        cursor = db.conn.cursor()
        sql = 'select * from user order by id'
        cursor.execute(sql)
        res = cursor.fetchmany(20)
        if res:
            [userList.append(name[1]) for name in res]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.closeMySql()
    for user_id in userList:
        print('------------------------------------')
        print('开始抓取用户:user_id = {0}'.format(user_id))
        url = base_url.format(user_id)
        driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
        driver.get(url)
        dict = parseAchieve(driver.page_source)
        if not dict:
            continue
        print('开始保存用户信息：user_id = {0}'.format(user_id))
        db.saveAchieveInfo(user_id,dict)
        time.sleep(5)

def test2():
    url = base_url.format('cloudycity')
    driver = webdriver.PhantomJS(executable_path=spider_const.phantomjs_path)
    driver.get(url)
    dict = parseAchieve(driver.page_source)
    db = DBUtil()
    db.saveAchieveInfo('cloudycity',dict)

def parseAchieve(content):
    if content is None:
        return None
    p = pq(content)
    card = p('div.Profile-sideColumnItem')
    dict = {}
    for item in card.items():
        pTitle = item('div.IconGraf')
        title = pTitle.text()
        if title == '优秀回答者':
            topic = item('div.Profile-sideColumnItemValue').text()
            dict['is_excellent_answer'] = True
            dict['excellent_topic'] = topic
            print('优秀回答者：topic='+topic)
        elif title[:4] == '知乎收录':
            record_num = re.sub('\D',"",title)
            record_by = item('div.Profile-sideColumnItemValue').text()
            dict['record_num'] = record_num
            dict['record_by'] = record_by
            print('知乎收录{0}个答案, {1}'.format(record_num,record_by))
        elif title[:2] == '获得':
            #获得xx次赞同
            applaud_num = re.sub('\D','',title)
            itemContent = item('div.Profile-sideColumnItemValue').text()
            #获得感谢的次数
            pattern = re.compile(r'获得\s?(\d+)\s?次感谢')
            result = re.search(pattern, itemContent)
            gratitude_num = result.groups()[0] if result else 0
            #获得收藏的次数
            pattern2 = re.compile(r'(\d+)\s?次收藏')
            result2 = re.search(pattern2, itemContent)
            collect_num = result2.groups()[0] if result2 else 0
            dict['applaud_num'] = applaud_num
            dict['gratitude_num'] = gratitude_num
            dict['collect_num'] = collect_num
            print('获得{0}次称赞，{1}次感谢，{2}次收藏'.format(applaud_num,gratitude_num,collect_num))
        elif title[:2] == '参与':
            public_edit_num = re.sub('\D','',title)
            dict['public_edit_num'] = public_edit_num
            print('参与{0}次公共编辑'.format(public_edit_num))
    return dict

if __name__ == '__main__':
    test2()