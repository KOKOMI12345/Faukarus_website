from database import *

logging.basicConfig(level=logging.INFO)

def run(username):

    # 查询是否有重复的数据
    cursor.execute("SELECT user, COUNT(*) FROM userinfo GROUP BY user HAVING COUNT(user) > 1")
    results = cursor.fetchall()

    # 输出重复的数据
    for row in results:
        username, count = row
        logging.info(f"用户名 {username} 有 {count} 条重复的数据")

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logging.info("关闭连接")

    if len(results) > 0:
        logging.info("存在重复数据")
        return True
    else:
        logging.info("不存在重复数据")
        return False


if __name__ == '__main__':
    run(username="Faukarus")