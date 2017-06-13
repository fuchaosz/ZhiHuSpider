#Python分布式程序---服务端进程
import random,time,queue
from multiprocessing.managers import BaseManager

#发送任务的队列
task_queue = queue.Queue()
#接收结果的队列
result_queue = queue.Queue()

class QueueMaager(BaseManager):
    pass

#把两个queue都注册到网络上
QueueMaager.register('get_task_queue',callable=lambda :task_queue)
QueueMaager.register('get_result_queue',callable=lambda :result_queue)
#绑定端口5000，设置验证码'abc'
manager = QueueMaager(address=('',5000),authkey=b'abc')
#启动Queue
manager.start()
