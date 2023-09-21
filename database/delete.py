from database import *

logging.basicConfig(level=logging.INFO)

def run(username):
    # 连接数据库
    cursor = conn.cursor()

    try:
        # 查询重复数据
        cursor.execute("SELECT user, MIN(id) as id FROM userinfo GROUP BY user HAVING COUNT(user) > 1")

        duplicate_data = cursor.fetchall()

        for data in duplicate_data:
            user, id = data
            # 删除除第一条外的重复数据
            cursor.execute("DELETE FROM userinfo WHERE user=%s AND id!=%s", (user, id))

        # 提交事务
        conn.commit()
        logging.info("删除重复数据完成")

    except Exception as e:
        logging.error(f"删除重复数据出错: {str(e)}")
        conn.rollback()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logging.info("关闭连接")


def delete_record(username):
    try:
        cursor = conn.cursor()

        # 使用 DELETE 语句删除指定条件的数据
        delete_query = "DELETE FROM userinfo WHERE user = %s"
        cursor.execute(delete_query, (username))
        conn.commit()

        cursor.close()
        conn.close()
        logging.info("删除用户数据成功")
        return True
        
    except Exception as e:
        logging.error(f"删除用户数据出错: {str(e)}")
        return False

if __name__ == '__main__':
    run(username="Faukarus")