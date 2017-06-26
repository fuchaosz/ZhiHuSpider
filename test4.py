import requests

url = r'https://www.zhihu.com/people/excited-vczh/following'

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

def test():
    d1 = {}
    d1['code'] = 1
    d2 = {}
    d2['code'] = 2
    d2.update(d1)
    print(d2)

if __name__ == '__main__':
    test()