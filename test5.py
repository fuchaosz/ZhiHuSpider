#学习多线程
import time
import threading
import multiprocessing
import os
import sys
import logging
from zhihu.spider_const import log
from zhihu.spider_const import loge
import re
class TestThread():

    def __init__(self):
         self.count = 0
         self.lock = threading.Lock()

    def show(self):
        while True:
            self.lock.acquire()
            print(threading.currentThread().ident)
            # print('pid =',os.getpid())
            print(self.count)
            time.sleep(2)
            self.lock.release()
            time.sleep(5)

    def start(self):
        t = []
        for i in range(0,3):
            th = threading.Thread(target=self.show)
            t.append(th)
        for i in t:
            i.start()
        for i in t:
            i.join()

    def startProcess(self):
        p = []
        for i in range(0,3):
            p.append(multiprocessing.Process(target=self.show))
        for i in p:
            i.start()
        time.sleep(5)
        self.count = 5
        print('in main, self.count = ',self.count)
        for i in p:
            i.join()

def test(user,** arg):
    print(user)
    print(arg.get('test','aaa'))

if __name__ == '__main__':
    # t = TestThread()
    # t.start()
    # t.startProcess()
    # [print(x) for x in range(1,10)]
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s %(filename)s[line:%(lineno)d] [pid:%(process)d] [tid:%(thread)d] %(levelname)s: %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S'
    #                     )
    # logging.info('hello')
    # logging.info('test')
    # dict = {}
    # dict['code1'] = 'code1'
    # dict['code2'] = 'code2'
    # dict['code3'] = 'code3'
    # l = []
    # l.append('code1')
    # l.append('code2')
    # l.append('code3')
    # sql = "{0},{1},{2}".format(l)
    # print(sql)
    # str = '获得 25494 次感谢，46181 次收藏'
    # pattern = re.compile(r'获得\s?(\d+)\s?次感谢')
    # pattern2 = re.compile(r'(\d+)\s?次收藏')
    # result = re.search(pattern,str)
    # result2 = re.search(pattern2,str)
    # x = result.groups()[0] if result else 0
    # y = result2.groups()[0] if result2 else 0
    # print(x)
    # print(y)
    dict = {'AAA':'aaa'}
    dict2 = {'AAA':'bb'}
    print(dict)
    dict.update(dict2)
    print(dict)


