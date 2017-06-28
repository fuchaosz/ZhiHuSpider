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
format_complex = '%(asctime)s %(filename)s[line:%(lineno)d] [pid:%(process)d] [tid:%(thread)d] [method:%(funcName)s()] %(levelname)s: %(message)s'
format_simple = '[tid:%(thread)d]:%(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=format_simple,
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename=log_file_name,
    # filemode='w'
)
log = logging.getLogger('my_log').info
loge = logging.getLogger('my_log').error

#phantomjs浏览器的位置
phantomjs_path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
