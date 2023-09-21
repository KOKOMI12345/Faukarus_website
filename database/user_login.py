from database import *

logging.basicConfig(level=logging.INFO)
def run(username,password,age):
 try:

#插入数据
   cursor.execute("insert into userinfo(user,pwd,age)values(%s,%s,%s);",[username,password,age])
   conn.commit()
   logging.info("数据已插入")

#关闭
   cursor.close()
   conn.close()
   logging.info("关闭连接")
   return True
 except Exception as e:
    return False
#end

if __name__ == '__main__':
   run(username="Faukarus",password="12345678",age=18)