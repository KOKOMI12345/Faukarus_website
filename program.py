import pymysql
import requests
from pymysql.cursors import DictCursor
# 项目的功能写在program文件中!
from __init__ import *


def get_current_time():
    send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return send_time



app = Flask(__name__)

# 记录日志所需的代码
app.logger.addHandler(logs.getloghandler())
ctx = app.app_context()
ctx.push()

# 头像的代码
UPLOAD_FOLDER = 'static/avatars'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =======我懒得搞太多的代码重构，所以都记载这了啊！=======#

# =========== 下边为主逻辑============#
app.logger.info("flask启动中")
# 设置session密钥
with open('database.json') as f:
    config = json.load(f)
app.config['SECRET_KEY'] = config['session-key']
app.logger.info("session-key已经应用:" + config['session-key'])
app.config['MAX_CONNECTIONS'] = 1000
app.logger.warn("注意,最大连接数已经设置为:" + str(app.config['MAX_CONNECTIONS']) + ",时刻监视连接数值!")

app.logger.info("应用数据库配置连接:" + str(config['host']) + ":" + str(config['port']) + ":" + str(config['user']) + ":"
 + str(config['password']) + ":" + str(config['database']) + ":" + str(config['charset']))

if app.config['SECRET_KEY'] == "":
    app.logger.warning("警告,session_key未设置! 后边的session应用可能会无法使用!")


# 实例化一个限速器
limiter = Limiter(app)

'''获取数据库游标'''


def get_cursor():
    conn = pymysql.connect(
    host=config['host'],
    port=config['port'],
    user=config['user'],
    passwd=config['password'],
    db=config['database'],
    charset=config['charset']
)
    cursor = conn.cursor(cursor=DictCursor)
    return cursor, conn


@app.before_request
def before_request():
    app.logger.info(
        '[方法为:] - {} - [路径来自] - {} - [访问请求来自:] - {}'.format(request.method, request.path, request.remote_addr))
    if not hasattr(g, 'connections'):
        g.connections = 0
    if g.connections >= app.config['MAX_CONNECTIONS']:
        app.logger.warning("警告,最大的连接数已经达到!")
        return "Max connections reached", 503
    g.connections += 1
    return app.logger.info("连接数为:" + str(g.connections))


@app.after_request
def after_request(response):
    g.connections -= 1
    return response


@app.route('/chat', methods=['GET', 'POST'])
@limiter.limit("100/second")
def chat():
    return render_template('chat.html')




@app.route('/chat2', methods=['POST'])
@limiter.limit("100/second")
def chat2():
    send_time = get_current_time()
    username = session.get('username')
    message = request.form['message']
    n = check.check(message=message, username=username)
    if n == False:
        return "......"
    app.logger.info('[用户名] - {} - [发送时间] - {} - [发送内容] - {}'.format(username, send_time, message))
    add_chat.run(send_time=send_time, user=username, message=message)

    chat_data = get_chat.get_chat_data()  # 获取聊天数据
    return render_template('chat.html', chat_data=chat_data)


'''注册页面'''


@app.route('/registation1', methods=['GET', 'POST'])
@limiter.limit("100/second")
def procress_registation1():
    if request.method == 'GET':
        return render_template('registation.html')
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    code = request.form['code']
    correct = user_login.run(username, password, age=18)  # 判断密码用户名，密码是否正确的代码函数
    user_repeat = repeated_data.run(username)  # 判断用户名是否重复,以后如果有人要卡bug绕过登录，用这个模块制裁他!
    the_long = check.check2(username)
    if user_repeat == True:
        delete.run(username)  # 删除重复的用户名,因为上面的user_login模块先记录了数据,如果重复则会删除，防止刷数据
        return jsonify({'code': 101, 'msg': '用户名已存在'})
    else:
        if the_long == False:
            # 我希望这里提示了他之后，把user_login记录的数据再删掉,但是他不是重复的!
            delete.delete_record(username)
            return jsonify({'code': 102, 'msg': '你输入的信息在允许范围外'})
        if correct == True:
            print('验证码及你的输入：' + session['valid_code'], code)
            if session['valid_code'].upper() == code.upper():
                return jsonify({'code': 100, 'msg': '注册成功'})
            else:
                return jsonify({'code': 103, 'msg': '验证码错误'})


''''好友功能'''


@app.route('/addfriend', methods=['POST'])
def addfriend():
    my_name = request.form.get('my_name')
    friend_name = request.form.get('friend_name')
    cursor, conn = get_cursor()
    cursor.execute('select id from userinfo where user = %s', (friend_name,))
    result = cursor.fetchone()
    if result:
        friend_id = result['id']
        cursor.execute('select id from userinfo where user = %s', (my_name,))
        my_result = cursor.fetchone()
        my_id = my_result['id']
        already_friend = cursor.execute('select * from friend where user_id = %s and friend_id = %s',
                                        (my_id, friend_id))
        if not already_friend:
            cursor.execute('insert into friend(user_id,friend_id) values(%s,%s)', (my_id, friend_id))
            conn.commit()
            cursor.execute('select friend_id from friend where user_id = %s ', (my_id,))
            friends = cursor.fetchall()
            friends_list = []
            for i in friends:
                friend_id = i['friend_id']
                cursor.execute('select user from userinfo where id = %s', (friend_id,))
                friend_name = cursor.fetchone()['user']
                friends_list.append({'user': friend_name, 'id': friend_id})

            return jsonify({'code': 100, 'msg': '成功添加好友', 'friends': friends_list})
        else:
            return jsonify({'code': 101, 'msg': '你已添加该好友'})
    else:
        return jsonify({'code': 102, 'msg': '你添加的好友不存在'})


'''验证码'''


@app.route('/get_code')
def my_code():
    response = get_code.get_code()
    return response


'''图片功能'''
@app.route('/get_img')
def get_img():
    username = session.get('username')
    a = check.check_login(username=username)  # 验证登录的，不用多说!
    if a == False:
        return redirect('/')
    cursor, conn = get_cursor()
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    if len(images) > 10:
        images = random.sample(images, 10)

    return render_template('picture.html', images=images)


'''上传图片页面路由'''


@app.route('/upload', methods=['POST', 'get'])
def upload():
    username = session.get('username')
    a = check.check_login(username=username)  # 验证登录的，不用多说!
    if a == False:
        return redirect('/')

    file = request.files['image']

    # 将图片保存到服务器
    filename = file.filename
    file.save('./static/images/' + filename)

    # 将图片信息插入数据库
    cursor = db.cursor()
    cursor.execute("INSERT INTO images (filename) VALUES (%s)", (filename,))
    db.commit()
    cursor.close()

    return jsonify({'code': 100, 'msg': '图片上传成功'})


'''登录页面'''
@app.route('/')
@limiter.limit("100/second")  # 限速100个每一秒
def login():
    return render_template('login.html')


'''登录校验'''
@app.route('/procress_login', methods=['POST'])
@limiter.limit("100/second")
def progress_login():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    from database import user_relogin
    b = user_relogin.run(username=username, password=password)
    if b == True:
        return jsonify({'code': 100, 'msg': '登陆成功'})
    elif b == False:
        return jsonify({'code': 103, 'msg': '用户名或密码错误'})


'''好友列表'''
@app.route('/friend_list', methods=["GET"])
def friend_list():
    # 通过游标对象拿到用户表所有数据
    cursor, conn = get_cursor()
    username = session.get('username')
    cursor.execute('SELECT id FROM userinfo WHERE user = %s', (username,))
    id = cursor.fetchone()['id']
    friends_list = []
    cursor.execute('select friend_id from friend where user_id = %s', (id,))
    friend_result = cursor.fetchall()
    for friend in friend_result:
        friend_id = friend['friend_id']
        cursor.execute('select user from userinfo where id = %s', (friend_id,))
        friend_name = cursor.fetchone()['user']
        friends_list.append({'user': friend_name, 'id': friend_id})

    # 分页，每页20条
    per_page = 20
    pagination = make_pagenation.Pagination(friends_list, per_page)
    page = int(request.args.get('page', 1))
    # 当前页数据
    page_data = pagination.get_page(page)
    # 总页数
    total_pages = pagination.get_total_pages()
    print(page_data, total_pages)
    return jsonify({'page_data': page_data, 'total': total_pages})


'''欢迎页面'''
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    # 通过游标对象拿到用户表所有数据
    cursor, conn = get_cursor()
    username = session.get('username')

        # 查询帖子标题、作者和发帖时间
    query = '''
            SELECT posts.title, userinfo.user, posts.created_at, posts.content,posts.id
            FROM posts
            INNER JOIN userinfo ON posts.user_id = userinfo.id
            ORDER BY posts.created_at DESC 
        '''
    cursor.execute(query)
    results = cursor.fetchall()
    finally_results = []
    for result in results:
        filepath = 'static/avatars/' + result['user'] + '.jpg'
        if os.path.exists(filepath):
            result['avatar'] = True
            finally_results.append(result)
        else:
            result['avatar'] = False
            finally_results.append(result)
    filepath = 'static/avatars/' + username + '.jpg'
    if os.path.exists(filepath):
        return render_template("welcome.html", username=username, avatar=True, results=finally_results)

    return render_template("welcome.html", username=username, results=finally_results)


'''查看消息'''
@app.route('/message', methods=["GET"])
def get_message():
    cursor, conn = get_cursor()
    username = session.get('username')
    cursor.execute('SELECT id FROM userinfo WHERE user = %s', (username,))
    id = cursor.fetchone()['id']
    cursor.execute('SELECT * FROM messagetable WHERE user_id = %s', (id,))
    message = cursor.fetchall()
    return jsonify({'message': message})


'''更换头像'''
@app.route('/avatar', methods=['POST'])
def avatar():
    file = request.files['file']  # 获取上传的文件对象

    cursor, conn = get_cursor()
    username = session.get('username')
    cursor.execute('UPDATE userinfo SET age = 20 WHERE user = %s', (username,))
    conn.commit()
    # 保存文件到服务器
    file.save('static/avatars/' + username + '.jpg')

    # 进行进一步的文件处理和业务逻辑

    return '文件上传成功'


'''发送消息'''
@app.route('/sendmsg', methods=['POST'])
def sendmsg():
    recive_id = request.form['recive_id'].strip()
    send_name = request.form['send_name']
    message = request.form['message']

    app.logger.info(send_name + "向" + recive_id + '发送消息：' + message)
    cursor, conn = get_cursor()
    cursor.execute("INSERT INTO messagetable (user_id, message, sender) VALUES (%s, %s, %s)",
                   (recive_id, message, send_name))
    conn.commit()
    return jsonify({'code': 100, 'msg': '发送成功'})


'''查看帖子'''
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    cursor, conn = get_cursor()
    username = session.get('username')
    comments_sql = '''
    SELECT comments.content, userinfo.user, comments.created_at
    FROM comments
    INNER JOIN userinfo ON comments.user_id = userinfo.id
    WHERE comments.post_id = %s;
    '''
    posts_sql = '''
        SELECT *
        FROM posts
        WHERE id = %s;
    '''
    if request.method == 'GET':
        post_id = request.args.get('index')
        cursor.execute(comments_sql,(post_id,))
        comments_results = cursor.fetchall()
        cursor.execute(posts_sql, (post_id,))
        posts_result = cursor.fetchone()
        cursor.execute('select id from userinfo where user = %s',(username,))
        my_id = cursor.fetchone()['id']
        post_userid = posts_result['user_id']
        cursor.execute('select user from userinfo where id = %s',(post_userid,))
        post_user = cursor.fetchone()['user']
        if os.path.exists('static/avatars/'+post_user+'.jpg'):
            posts_result['avatar'] = True
            posts_result['username'] = post_user
        else:
            posts_result['username'] = post_user
        if my_id == post_userid:
            print(posts_result,comments_results)
            return render_template('posts.html',comments=comments_results,posts=posts_result,delete=True,username=username)
        return render_template('posts.html',comments=comments_results,posts=posts_result,username=username)


    comment_content = request.form.get('comment')
    username = session.get('username')
    post_id = request.form.get('post_id')

    cursor.execute('select id from userinfo where user = %s',(username,))
    user_id = cursor.fetchone()['id']
    cursor.execute('insert into comments (content,user_id,post_id) values(%s,%s,%s)',(comment_content,user_id,post_id))
    conn.commit()

    cursor.execute(comments_sql,(post_id,))
    results = cursor.fetchall()
    return jsonify({'comments':results})

'''发布帖子'''
@app.route('/send_posts',methods=['POST'])
def send_posts():
    post_title = request.form.get('title')
    post_content = request.form.get('content')
    user = session.get('username')
    cursor,conn = get_cursor()
    cursor.execute('select id from userinfo where user = %s',(user,))
    id = cursor.fetchone()['id']
    cursor.execute('insert into posts (title,content,user_id) values(%s,%s,%s)',(post_title,post_content,id))
    conn.commit()
    return jsonify({'code':100,'msg':'发布成功'})


'''删除帖子'''
@app.route('/delete_post',methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id')
    print(post_id+'post_id')
    cursor,conn = get_cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s',(post_id,))
    conn.commit()
    print(66)
    return jsonify({'code':100,'msg':'删除成功'})

'''注销功能'''
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
