#!/usr/bin/python
#coding:utf-8
from pyquery import PyQuery as pq
import random
import requests
import spider_const

class ProxyTool():

    def __init__(self):
        self.headers = spider_const.headers
        self.detect_proxy_url = spider_const.detect_proxy_url
        self.session = requests.session()
        self.session.keep_alive = False

    #检测抓到的IP是否有效
    def detectProxyIP(self,ip,port):
        result = False
        proxies = {
            'http':'http://{0}:{1}'.format(ip,port),
            'https':'http://{0}:{1}'.format(ip,port)
        }
        try:
            r = self.session.get(self.detect_proxy_url,proxies=proxies,headers=self.headers)
            if r.status_code == 200:
                result = True
                print(r.text)
        except Exception as e:
            result = False
            print(e)
        return  result

    #从西刺提供的API文件中读取ip
    def getProxyIpByFile(self):
        url = r'http://api.xicidaili.com/free2016.txt'
        list = []
        r = requests.get(url,headers=spider_const.headers)
        str = r.text.split('\r\n')
        for item in str:
            ip = item.split(':')[0]
            port = item.split(':')[1]
            list.append((ip,port))
        return list

if __name__ == '__main__':
    p = ProxyTool()
    list = p.getProxyIpByFile()
    for ip,port in list:
        p.detectProxyIP(ip,port)