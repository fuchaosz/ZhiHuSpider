#!/usr/bin/python
#coding:utf-8
#常量
import logging

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Referer": "http://www.example.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}

#检测代理地址是否有效的网址
detect_proxy_url = r'http://ip.chinaz.com/getip.aspx'

#日志
log_file_name = 'spiderlog.log'
format_complex = '%(asctime)s [pid:%(process)d] [tid:%(thread)d]: %(message)s'
format_simple = '[tid:%(thread)d]:%(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=format_complex,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=log_file_name,
    filemode='w'
)
console = logging.StreamHandler()
formatter = logging.Formatter(format_complex)
console.setFormatter(formatter)
console.setLevel(logging.INFO)
logging.getLogger('my_log').addHandler(console)
log = logging.getLogger('my_log').info
loge = logging.getLogger('my_log').error

#phantomjs浏览器的位置
phantomjs_path = r'/usr/local/bin/phantomjs'
# phantomjs_path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'

#检测到下面这个文件则退出全部程序
control_exit_file = 'exit.txt'
control_exit_duration = 1               #检测是否退出的时间间隔，单位：分钟

#Phantomjs的配置
desired_cap = {
        'phantomjs.page.settings.loadImages' : False,
        'phantomjs.page.settings.resourceTimeout' : 10000,
        'phantomjs.page.settings.userAgent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}
