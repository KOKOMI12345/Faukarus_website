import pymysql


# 创建全局数据库连接
connection = None

def connect_database():
    global connection
    # 创建数据库连接
    connection = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='Fukarus', autocommit=True)

