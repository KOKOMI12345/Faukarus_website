import pymysql
from pymysql.cursors import DictCursor
import logging
import json
from program import *
# 读取配置文件
with open('database.json') as f:
    config = json.load(f)

# 数据库连接配置
conn = pymysql.connect(
       host=config['host'],
       port=config['port'],
       user=config['user'],
       passwd=config['password'],
       db=config['database'],
       charset=config['charset']
)

    

# 获取数据库游标
def get_cursor():
    cursor = conn.cursor(cursor=DictCursor)
    return cursor

cursor = get_cursor()

db = pymysql.connect(
    host=config['host'],
    port=config['port'],
    user=config['user'],
    passwd=config['password'],
    db=config['database'],
    charset=config['charset']
)