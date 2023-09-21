from database import *

logging.basicConfig(level=logging.INFO)

def run(send_time, user, message):

    # 插入数据
    cursor.execute("INSERT INTO chat (send_time, user, message) VALUES (%s, %s, %s);", [send_time, user, message])
    conn.commit()
    logging.info("消息已插入")

    # 关闭游标和连接
    cursor.close()
    conn.close()
    logging.info("关闭连接")
    return True

if __name__ == '__main__':
   run(send_time=None,user="Fukarus",message="我芙卡洛斯开始测试啦!")