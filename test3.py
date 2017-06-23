# 测试Selenium的代理,用代理爬知乎
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from zhihu import proxy_tool

base_url = r'https://www.zhihu.com/people/{0}/following'
path = r'E:\software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
TEST_URL = r'https://httpbin.org/get?show_env=1' #查看浏览器请求头
TEST_URL_2 = r'https://www.zhihu.com/people/excited-vczh/following'
start_user_id = 'excited-vczh'
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

def getUserInfo(userId, ip):
    dict = {}
    # 构造用户信息页面的url
    url = base_url.format(userId)
    print('url = ',url)
    dict['user_id'] = userId
    dict['code'] = 200
    try:
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,
                'httpProxy': ip
            }
        )
        desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
        proxy.add_to_capabilities(desired_capabilities)
        driver = webdriver.PhantomJS(executable_path=path, desired_capabilities=desired_capabilities)
        driver.set_page_load_timeout(10)
        driver.get(url)
        driver.get_screenshot_as_file('01.png')
        error = driver.page_source.find('你似乎来到了没有知识存在的荒原...')
        # 404界面
        if error:
            dict['code'] = 404
            print('用户不存在，user_id = ',userId)
            return dict
        elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
        elem.send_keys(Keys.ENTER)
        dict = parsePage(driver.page_source)
    except Exception as e:
        print('发生异常')
        dict['code'] = 405
        print(e)
    finally:
        driver.close()
    return dict

def parsePage(content):
    dict = {}
    p = pq(content)
    # 先抓固定的，所有页面都一定有的信息，即使抓不到也只会是空，不会报错
    image = p('img.UserAvatar-inner').eq(0).attr('src')  # 用户头像
    name = p('span.ProfileHeader-name').text()  # 姓名
    sex = '男' if p('a.is-active').text().split()[0] == '他' else '女'  # 用户性别
    sign = p('span.ProfileHeader-headline').text()  # 个性签名
    dict['image'] = image
    dict['name'] = name
    dict['sex'] = sex
    dict['sign'] = sign
    # 如果连个性签名都没有，那一定是个没有什么价值的用户,其他信息也一定不全，不抓了
    if sign is None:
        dict['code'] = 405
        print('用户没有个性签名')
        return dict
    # 下面抓不是固定的，可能有的人没有填写
    detailItems = p('div.ProfileHeader-detailItem')
    # 下面遍历每一条信息
    for item in detailItems.items():
        itemName = item('span.ProfileHeader-detailLabel').text()
        if itemName == '居住地':
            location = item.find('div.ProfileHeader-detailValue span').text()
            dict['location'] = location
        elif itemName == '所在行业':
            major = item('div.ProfileHeader-detailValue').text()
            dict['major'] = major
        elif itemName == '职业经历':
            job = item('div.ProfileHeader-field').text()
            dict['job'] = job;
        elif itemName == '教育经历':
            education = item('div.ProfileHeader-field').text()
            dict['education'] = education
        elif itemName == '个人简介':
            info = item('div.ProfileHeader-detailValue').text()
            dict['info'] = info
    return dict

def getUserInfo2(userId,ip):
    url = base_url.format(userId)
    proxies = {"http": "http://{0}".format(ip), "https": "http://{0}".format(ip)}
    r = requests.get(url,headers = headers,proxies=proxies)
    print(r.text)

def test():
    try:
        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,
                'httpProxy': '139.162.142.80:80'
            }
        )
        desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
        proxy.add_to_capabilities(desired_capabilities)
        driver = webdriver.PhantomJS(executable_path=path, desired_capabilities=desired_capabilities)
        driver.set_page_load_timeout(25)
        driver.implicitly_wait(3)
        driver.get(TEST_URL_2)
        elem = driver.find_element_by_class_name('ProfileHeader-expandButton')
        elem.send_keys(Keys.ENTER)
        driver.get_screenshot_as_file('01.png')
        dict = parsePage(driver.page_source)
        print(dict)
    except Exception as e:
        print(e)
    print('-----------end----------------')

def test2():
    dict = {'aaa':111,'bbb':'ada'}
    print(dict)

if __name__ == '__main__':
    # dict = getUserInfo(start_user_id,'113.121.42.182:808')
    # print(dict)
    # getUserInfo2(start_user_id,'45.76.47.179:1189')
    test()
    # test2()