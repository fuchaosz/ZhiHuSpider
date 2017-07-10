#测试数据库
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='zhihu',
    port=3306,
    charset='utf8'
)

def test():
    try:
        cursor = conn.cursor()
        sql = 'select * from user order by id'
        cursor.execute(sql)
        res = cursor.fetchone()
        print(res)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    test()