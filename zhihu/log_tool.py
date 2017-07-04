#日志工具
import logging
import spider_const

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] [pid:%(process)d] [tid:%(thread)d] [method:%(funcName)s()] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename=spider_const.log_file_name,
    # filemode='w'
)
logger = logging.getLogger('my_log')

class Log():

    @staticmethod
    def i(msg):
        logger.info(msg)

    @staticmethod
    def d(msg):
        logger.debug(msg)

    @staticmethod
    def e(msg):
        logger.error(msg)

    @staticmethod
    def setLevelInfo():
        logger.setLevel(logging.INFO)

    @staticmethod
    def setLevelDebug():
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def setLevelError():
        logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    Log.d('hello')
    Log.e('error')