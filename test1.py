#学习python
# lst = []
# lst.append(1)
# lst.append(2)
# print(lst)

# # 1 list用法
# classmates = ['Michael','Bob','Tracy']
# print(classmates)
# print(len(classmates))
# print(classmates[0])
# print(classmates[-1])
# classmates.append("Admin")
# print(classmates)
# classmates.insert(1,'Jack')
# print(classmates)
# classmates.pop()
# print(classmates)

# # 2 list用法2
# L = ['Apple',123,True]
# print(L)
# S = ['python','java',['asp','php'],'schema']
# print(len(S))

# # 3 tuple用法
# t = (1,2)
# print(t)
# t = ()
# print(t)
# t = ('a','b',['A','B'])
# t[2][0] = 'X'
# t[2][1] = 'Y'
# print(t)

# # 4 循环语句
# names = ['Michael','Bob','Tracy']
# for name in names:
#     print(name)
# sum = 0
# for x in [1,2,3,4,5,6,7,8,9,10]:
#     sum += x
# print(sum)
# print(list(range(5)))

# # 5 字典
# d = {'Michael':95,'Bob':75,'Tracy':85}
# print(d['Michael'])
# print(d['Bob'])
# # print(d['Tom'])
# print('Tom' in d) #判断Tom是否在字典的key中
# print(d.get('Tom',-1))

# # 6 集合
# s = set([1,2,3])
# print(s)

# # 7 函数可变参数
# def calc(*numbers):
#     sum = 0;
#     for n in numbers:
#         sum = sum + n * n;
#     return sum;
# print(calc(1,2,3))
# print(calc(1,3,5,6,7))
# nums = [1,2,3]
# print(calc(*nums)) #在传tuple参数的时候前面加一个*号

# # 8 关键字参数
# def person(name,age,**kw):
#     print('name:',name,' age:',age,' other:',kw)
# person('Michael',30)
# person('Bob',35,city='Beijing')
# person('Adam',45,gender='M',job='Engineer')

# # 9 关键字参数
# def person(name,age,**kw):
#     print("0000")
#     if 'city' in kw:
#         print("1111");
#         pass;
#     if 'job' in kw:
#         print("222")
#         pass;
#     print('name:',name,' age:',age,' other:',kw)
# person('Jack',24,city = 'beijing', addr = 'Chaoyang',zipcode = 1234)

# # 10 命名关键字,用*号分割位置参数
# def person(name,age,*,city,job):
#     print(name,age,city,job)
# person('Jack',12,city='Beijing',job='work')
#
# # 11 迭代
# d = {'a':1,'b':2,'c':3}
# for key in d:
#     print(key)
# from collections import Iterable
# a = isinstance('abc',Iterable)
# print(a)
# a = isinstance(123,Iterable)
# print(a)
# for i,value in enumerate(['A','B','C']):
#     print(i,value)
# for x,y in [(1,1),(2,4),(3,9)]:
#     print(x,y)

# # 12 列表生成式子
# a = list(range(1,11))
# print(a)
# a = [x * x for x in range(1,11)]
# print(a)
# a = [x * x for x in range(1,11) if x % 2 == 0]
# print(a)
# a = [m + n for m in 'ABC' for n in 'XYZ']
# print(a)

# # 13 生成器
# L = [x * x for x in range(10)] #L是列表
# g = (x * x for x in range(10)) #g是生成器
# for n in g:
#     print(n)

# # 14 函数式编程
# def add(x,y,f): # 高阶函数
#     return f(x) + f(y)
# a = add(-5,5,abs)
# print(a)
# def f(x):
#     return x * x
# # map是更高级的抽象,对每一个元素操作一次
# r = map(f,[1,2,3,4,5,6])
# l = list(r)
# print(l)
# l = list(map(str,[1,2,3,4,5,6]))
# print(l)
# # reduce是每两个元素依次累加
# from functools import reduce
# def add(x,y):
#     return x + y;
# r = reduce(add,[1,2,3,4,5,6,7,8,9])
# print(r)
# # filter过滤操作符
# def is_odd(n):
#     return n % 2 == 1
# l = list(filter(is_odd,[1,2,3,4,5,6,7,8,9]))
# print(l)

# # 15 匿名函数，lambda表达式
# l = list(map(lambda x: x * x,[1,2,3,4,5,6]))
# print(l)

# # 16 装饰器
# def now():
#     print('2015-3-25')
# f = now
# f()
# print(f.__name__)
# def log(func):
#     def wrapper(*args,**kw): # *args, **kw表示可以接受任何参数
#         print('call %s():' % func.__name__)
#         return func(*args,**kw)
#     return wrapper
# #添加装饰器
# @log
# def now2():
#     print('2015-3-25')
# now2()

# # 17 模块
# import sys
# def test():
#     args = sys.argv
#     if len(args) == 1:
#         print('Hello world!')
#     elif len(args) == 2:
#         print('Hello, %s !' % args[1])
#     else:
#         print('Too many arguments!')
#
# if __name__  == '__main__':
#     test()

# # 18 类
# class Student(object):
#     def __init__(self,name,score):
#         self.__name = name
#         self.__score = score
#
#     def print_score(self):
#         print('%s : %s' % (self.__name, self.__score))
# bart = Student('Bart',90);
# print(bart)
# bart.name = 'Bart Simpson'
# print(bart.name)
# bart.print_score()

# # 19 集成
# class Animal(object):
#     def run(self):
#         print('Animal is runing')
# class Dog(Animal):
#     def run(self):
#         print('dog is running')
#     def eat(self):
#         print('Eating meat....')
# class Cat(Animal):
#     def run(self):
#         print('Cat is running')
# dog = Dog()
# dog.run()
# cat = Cat()
# cat.run()

# # 20 类型判断
# print(type(123) == type(456))
# print(type(123) == int)
# print(type('abc') == str)
# import types
# def fn():
#     pass
# print(type(fn) == types.FunctionType)
# print(type(abs) == types.BuiltinFunctionType)
# type((x for x in range(10)) == types.GeneratorType)
# print(dir('ABC')) # 获取一个对象的所有属性和方法

# # 21 动态绑定方法
# class Student(object):
#     pass
# s = Student()
# s.name = 'Michael'
# print(s.name)
# #给实例绑定一个方法
# def set_age(self,age):
#     self.age = age
# from types import MethodType
# s.set_age = MethodType(set_age,s)
# s.set_age(25)
# print(s.age)
# #给class绑定方法
# def set_score(self,score):
#     self.score = score
# Student.set_score = set_score
# s.set_score(10) #每个实例都可以调用
# print(s.score)
# #限制实例可以添加的属性
# class Student2(object):
#     __slots__ = ('name','age') #用tuple定义允许绑定的属性名称
# s = Student2()
# s.name = 'Michael2'
# s.age = 25
# s.score = 99
# print(s)

# # 22 property属性
# class Student(object):
#
#     def get_score(self):
#         return self._score
#
#     #检查属性的取值范围
#     def set_score(self,value):
#         if not isinstance(value,int):
#             raise ValueError('score must an integer')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0~100')
#         self._score = value
# s = Student()
# s.set_score(60)
# print(s.get_score())
# # 利用property简化代码
# class Student2():
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self,value):
#         if not isinstance(value,int):
#             raise ValueError('score must be integer')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0~100')
# s2 = Student2()
# s2.score = 60 #实际上调用的s2.set_score()方法

# # 23 定制类：重写__iter__
# class Fib(): # 自定义一个可以迭代的对象
#
#     def __init__(self):
#         self.a,self.b = 0,1  #初始化两个计数器
#
#     #返回迭代对象
#     def __iter__(self):
#         return self   #实例本身就是迭代器
#
#     #不断迭代的方法
#     def __next__(self):
#         self.a,self.b = self.b, self.a + self.b #计算下一个值
#         if self.a > 1000: #退出循环的条件
#             raise StopIteration() #停止迭代
#         return self.a   #返回下一个值
#
#     #使类支持下标访问和切片
#     def __getitem__(self, item):
#         if isinstance(item,int): #如果item是索引
#             a,b = 1,1
#             for x in range(item):
#                 a,b =  b,a+b
#             return a
#         if isinstance(item,slice): #如果item是切片
#             start = item.start
#             stop = item.stop
#             if start is None:
#                 start = 0
#             a,b = 1,1
#             L = []
#             for x in range(stop):
#                 if x >= start:
#                     L.append(a)
#                 a,b = b, (a+b)
#             return L
#
# #for n in Fib():
# #    print(n)
# # print(Fib()[2])
# # f = Fib()
# # print(f[1:10])

# # 24 定制类：__getattr__
# class Chain(object):
#
#     def __init__(self,path = ''):
#          self._path = path
#
#     def __getattr__(self,path):
#         return Chain("%s/%s" % (self._path,path))
#
#     def __call__(self,user=''):
#         return Chain("%s/%s" % (self._path,user))
#
#     def __str__(self):
#         return self._path
#
#     __rept = __str__
#
# path = Chain().status.user.main.timeline.list
# print(path)
# path = Chain().status.user('Michael').name
# print(path)

# # 25 定制类：__call__
# class Student(object):
#     def __init__(self,name):
#         self.name = name
#
#     def __call__(self):
#         print('My name is %s' % self.name)
#
# s = Student('Michael')
# s()
# #使用callable判断是否可以被调用
# print(callable(Student('Michael')))
# print(callable(max))
# print(callable(None))
# print(callable('str'))

# # 26 枚举
# from enum import Enum, unique
# # Month = Enum('Month',('Jan','Feb','Mar','Apr','May'))
# # for name,member in Month.__members__.items():
# #     print(name,'=>',member,',',member.value)
# #自定义枚举
# @unique
# class Weekday(Enum):
#     Sun = 0
#     Mon = 1
#     Tue = 2
#
# day1 = Weekday.Mon
# print(day1)
# print(day1.value)

# # 27 错误处理
# try:
#     print('try...')
#     r = 10/1
#     print('result:',r)
# except ValueError as e:
#     print('ValueError:',e)
# except ZeroDivisionError as e:
#     print('Except:',e)
# else:   #如果没有错误则 执行else语句
#     print('no error')
# finally:
#     print('finally...')
# print('END')

# # 28 抛出错误
# class FooError(ValueError):
#     pass
#
# def foo(s):
#     n = int(s)
#     if n == 0:
#         raise FooError('invalid value: %s' % s)
#     return 10/n
#
# foo('0')

# # 29 文件操作
# # try:
# #     f = open(r'D:\test\a.txt','r')
# #     print(f.read())
# # finally:
# #     if f:
# #         f.close()
# # #简化版本
# # with open(r'D:\test\a.txt','r') as f:
# #     print(f.read())
# with open(r'D:\a.log','r',encoding='utf-8',errors='ignore') as f:
#     print(f.read())

# # 30 StrinIO 和 BytesIO
# from io import StringIO
# f = StringIO()
# f.write('Hello')
# f.write(' ')
# f.write('World')
# print(f.getvalue())
# f = StringIO('Hello\nHi!\nGoodBye!')
# while True:
#     s = f.readline()
#     if s == '':
#         break
#     print(s.strip())
# from io import BytesIO
# f = BytesIO()
# f.write('中文'.encode('utf-8'))
# print(f.getvalue())

# # 31 操作文件和目录
# import os
# print(os.name)
# # print(os.environ)
# # print(os.environ.get('PATH'))
# path = r'D:\test\a.txt'
# str = os.path.split(path)
# print(str)
# print(os.path.splitext(path)) #直接得到扩展名
# #列出当前目录下的所有目录
# list = [x for x in os.listdir('.') if os.path.isdir(x)]
# print(list)
# #列出当前目录下的所有py文件
# list = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
# print(list)

# # 33 序列化
# import pickle
# d = dict(name='Bob',age=20,score=88)
# # s = pickle.dumps(d) #将字典序列化为字节
# # print(s)
# #将字典序列化后保存到文件中
# # f = open('dump.txt','wb')
# # pickle.dump(d,f)
# # f.close()
# #从文件中读取序列化的字典
# # f = open('dump.txt','rb')
# # d2 = pickle.load(f)
# # f.close()
# # print(d2)
# import json
# # d3 = json.dumps(d)
# # print(d3)
# #序列化对象
# class Student(object):
#     def __init__(self,name,age,score):
#         self.name = name
#         self.age = age
#         self.score = score
#
# def student2dict(std):
#     return {
#         'name':std.name,
#         'age':std.age,
#         'score':std.score
#     }
#
# s = Student('Bob',20,88)
# #print(json.dumps(s))  #直接序列化对象会报错
# #print(json.dumps(s,default=student2dict)) #传入第二个参数作为序列化规则
# print(json.dumps(s,default=lambda obj:obj.__dict__))

# # 34 多进程
# import os
# # print('Process (%s) start...' % os.getpid())
# # pid = os.fork()
# # if pid == 0:
# #     print('I am child process (%s) and my parent is %s.' % (os.getpid(),os.getppid()))
# # else:
# #     print('I (%s) just created a child process (%s).' % (os.getpid(),pid))
# #跨平台版本多进程
# # from multiprocessing import Process
# #
# # #子进程要执行的代码
# # def run_proc(name):
# #     print('Run child process %s (%s)...' % (name,os.getpid()))
# #
# # if __name__ == '__main__':
# #     print('Parent process %s.' % os.getpid())
# #     p = Process(target=run_proc,args=('test',))
# #     print('child process will start')
# #     p.start()
# #     p.join()
# #     print('Child process end')
# # 要启动大量子进程，则使用pool
# from multiprocessing import Pool
# import os,time,random
#
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name,os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name,(end-start)))
#
# if __name__ == '__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(long_time_task,args=(i,))
#     print('Waiting for all subprocess done...')
#     p.close()
#     p.join()
#     print('All subprocesses done')

# # 35 进程间通信
# from multiprocessing import Process,Queue
# import os,time,random
#
# #写数据进程执行的代码
# def write(q):
#     print('Process to write: %s' % os.getpid())
#     for value in ['A','B','C','D']:
#         print('Put %s to queue...' % value)
#         q.put(value)
#         time.sleep(random.random())
#
# #读数据进程执行代码
# def read(q):
#     print('Process to read: %s' % os.getpid())
#     while True:
#         value = q.get(True)
#         print('Get %s from queue.' % value)
#
# if __name__ == '__main__':
#     #父进程创建Queue，并传给各个子进程
#     q = Queue()
#     pw = Process(target=write,args=(q,))
#     pr = Process(target=read,args=(q,))
#     #启动子进程pw，写入
#     pw.start()
#     #启动子进程pr,读取
#     pr.start()
#     #等待pw结束
#     pw.join()
#     #kill读进程
#     pr.terminate()

# # 36 多线程
# # import time,threading
# # #新线程执行的代码
# # def loop():
# #     print('thread %s is running...'% threading.current_thread().name)
# #     n = 0
# #     while n < 5:
# #         n = n + 1
# #         print('thread %s >>> %s' % (threading.current_thread().name,n))
# #         time.sleep(1)
# #     print('thread %s ended' % threading.current_thread().name)
# #
# # print('thread %s is running...' % threading.current_thread().name)
# # t = threading.Thread(target=loop,name='LoopThread')
# # t.start()
# # t.join()
# # print('thread %s ended' % threading.current_thread().name)
# #多线程同步
# import time,threading
#
# balance = 0
# lock = threading.Lock()
# def change_it(n):
#     global balance
#     balance = balance + n
#     balance = balance - n
#
# def run_therad(n):
#     for i in range(100000):
#         #先获取锁
#         lock.acquire()
#         try:
#             change_it(n)
#         finally:
#             #释放锁
#             lock.release()
#
# t1 = threading.Thread(target=run_therad,args=(5,))
# t2 = threading.Thread(target=run_therad,args=(8,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)

# # 37 正则表达式
# import re
# s = 'a b  c'.split(' ')
# print(s)
# s = re.split(r'\s+', 'a b  c')
# print(s)
# s = re.split(r'[\s\,]+','a b,c')
# print(s)
# m = re.match(r'^(\d{3})-(\d{3,8})$','010-12345')
# print(m.group(0))
# print(m.group(1))
# print(m.group(2))
# m = re.match(r'^(\d+)(0*)$','102300').groups() #贪婪匹配
# print(m)
# m = re.match(r'^(\d+?)(0*)$','102300').groups() #非贪婪匹配
# print(m)

# # 38 内置模块---collections
# # from collections import namedtuple
# # Point = namedtuple('Point',['x','y']) #相当于结构体
# # p = Point(1,2)
# # print(p.x,p.y)
# # #双向链表代替list提高插入、删除速度
# # from collections import deque
# # q = deque(['a','b','c'])
# # q.append('x')
# # q.appendleft('y')
# # print(q)
# #有序字典
# # from collections import OrderedDict
# # d = dict([('a',1),('b',2),('c',3)])
# # print(d)
# # od = OrderedDict([('a',1),('b',2),('c',3)])
# # od['z'] = 1
# # od['y'] = 2
# # od['x'] = 3
# # l = list(od.keys())
# # print(l)
# ## counter计数器
# # from collections import Counter
# # c = Counter()
# # for ch in 'programimg':
# #     c[ch] = c[ch] + 1
# # print(c)
# #itertools无限迭代器
# import itertools
# # natuals = itertools.count(2)  #自然数无限循环
# # for n in natuals:
# #     print(n)
# # cs = itertools.cycle('ABC') #字符串无限重复
# # for c in cs:
# #     print(c)
# # ns = itertools.repeat('A',3)  #重复3次
# # for n in ns:
# #     print(n)
# #通过takewhile设置无限迭代退出的条件
# # natuals = itertools.count(1)
# # ns = itertools.takewhile(lambda  x:x<10,natuals)
# # print(list(ns))
# # chain()将一组迭代对象串联起来，形成一个更大的迭代器
# for c in itertools.chain('ABC','XYZ'):
#     print(c)

# # 39 xml操作
# from xml.parsers.expat import ParserCreate
#
# class DefaultSaxHandler(object):
#     def start_element(self,name,attrs):
#         print('sax:start_element: %s,attrs:%s' % (name,str(attrs)))
#
#     def end_element(self,name):
#         print('sax:end_element: %s' % name)
#
#     def char_data(self,text):
#         print('sax:char_data: %s' % text)
#
# xml = r'''<?xml version="1.0"?>
# <ol>
#     <li><a href="/python">Python</a></li>
#     <li><a href="/ruby">Ruby</a></li>
# </ol>
# '''
#
# handler = DefaultSaxHandler()
# parse = ParserCreate()
# parse.StartElementHandler = handler.start_element
# parse.EndElementHandler = handler.end_element
# parse.CharacterDataHandler = handler.char_data
# parse.Parse(xml)

# # 40 Html Parser
# from html.parser import HTMLParser
# from html.entities import name2codepoint
#
# class MyHTMLParser(HTMLParser):
#
#     def handle_starttag(self, tag, attrs):
#         print('<%s>' % tag)
#
#     def handle_endtag(self, tag):
#         print('<%s>' % tag)
#
#     def handle_startendtag(self, tag, attrs):
#         print('<%s>' % tag)
#
#     def handle_data(self, data):
#         print(data)
#
#     def handle_comment(self, data):
#         print('<!--',data,'-->')
#
#     def handle_entityref(self, name):
#         print('&%s;' % name)
#
#     def handle_charref(self, name):
#         print('&#%s;' % name)
#
# parse = MyHTMLParser()
# parse.feed('''<html>
# <head></head>
# <body>
# <!-- test html parser -->
#     <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
# </body></html>
# ''')

# 41 urllib操作url
from urllib import request,parse

#get请求
# with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
#     data = f.read()
#     print('Status:', f.status,f.reason)
#     for k,v in f.getheaders():
#         print('%s: %s' % (k,v))
#     print('Data:',data.decode('utf-8'))

# # 41 图形界面
# from tkinter import *
#
# class Application(Frame):
#
#     def __init__(self,master=None):
#         Frame.__init__(self,master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.helloLabel = Label(self,text='Hello,world!')
#         self.helloLabel.pack()
#         self.quitButton = Button(self,text='Quit',command=self.quit)
#         self.quitButton.pack()
#
#     def hello(self):
#         name = self.nameInput.get() or 'world'
#         messagebox.showInfo('Message','Hello, %s' % name)
#
# app = Application()
# app.master.title('Hello World')
# app.mainloop()

# 42 数据库操作
import pymysql
import pymysql.cursors

#获取一个数据库连接
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='test',
    port=3306,
    charset='utf8'
)

#获取游标
with conn.cursor() as cursor:
    # sql = "insert into user values('hello1',12,0)"
    sql = 'select * from user'
    count = cursor.execute(sql)
    print('数量：',count)
    for row in cursor.fetchall():
        print('name:{0}  age:{1}  sex:{2}'.format(row[0],row[1],row[2]))
    conn.commit()

