#!user/bin/env python3
# coding:utf-8
from zhihu.spider_const import  log

def mlog(str):
    str = str.encode('UTF-8')
    log(str)

if __name__ == '__main__':
    log('测试中文123')