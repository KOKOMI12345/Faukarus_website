from database import *

logging.basicConfig(level=logging.INFO)

def get_chat_data() -> list:
    try:
        # 查询数据
        cursor.execute('SELECT * FROM chat')
        data = cursor.fetchall()

        # 关闭游标和连接
        cursor.close()
        conn.close()

        return data
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []

if __name__ == '__main__':
    chat_data = get_chat_data()
    for row in chat_data:
        chat_id = row['id']
        send_time = row['send_time']
        user = row['user']
        message = row['message']
        print(f"ID: {chat_id}, Send Time: {send_time}, User: {user}, Message: {message}")