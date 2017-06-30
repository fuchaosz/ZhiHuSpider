#学习多线程
import time
import threading
import multiprocessing
import os
import sys
import logging
from zhihu.spider_const import log
from zhihu.spider_const import loge
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
    url = 'https://pic1.zhimg.com/3a6c25ac3864540e80cdef9bc2a73900_xl.jpg'
    str = url.replace('xl','r')
    print(str)




