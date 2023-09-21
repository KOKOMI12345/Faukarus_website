#定义网站规范的
from __init__ import *

def check(message,username):

 try:
    if message == "":
        return False
    elif username == "":
        return False
    elif len(username) > 15:
        return False
    else:
        return True
 except Exception as e:
    logs.logging.error(e)
    return 1 # 1 代表没登录,验证不通过!
    
def check2(username):
    a = len(username)
    if a > 15:
        return False
    
def check_login(username):
    if not session.get('username'):
        return False