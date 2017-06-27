import requests
import sys

url = r'https://www.zhihu.com/people/excited-vczh/following'

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

def test():
    log_file = open('test.log','w')
    sys.stdout = log_file
    print('hello')
    print('test')
    log_file.close()


if __name__ == '__main__':
    test()