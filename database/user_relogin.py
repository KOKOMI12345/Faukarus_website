from database import *

logging.basicConfig(level=logging.INFO)

def run(username,password):
#查询数据
   cursor.execute("select * from userinfo where user=%s and pwd=%s", [username, password])
   result = cursor.fetchone()

#关闭
   cursor.close()
   conn.close()
   if result:   
      print("登录成功")
      return True
   else:
      print("登录失败")
      return False
#end
if __name__ == '__main__':
   run(username='admin',password='123456')