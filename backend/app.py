# ==================== TODO 后端主文件 ====================
# 职责：
#   1. 连接 MySQL 数据库（配置全部从环境变量读取）
#   2. 用户注册 / 登录 / 退出
#   3. 任务的增删改查（软删除、按用户隔离、?status 查询参数筛选）
# 说明：所有需要"登录"的接口都先从 session 里取 user_id，
#       取不到就返回 401，从而做到"每个用户只能操作自己的数据"。

import os
import bcrypt
import pymysql
from flask import Flask, jsonify, request, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')   # 生产环境用环境变量
CORS(app, supports_credentials=True)   # 允许跨域 + 允许携带 cookie（session 需要）


# 连接数据库（配置全部从环境变量读，本地/生产分开）
# 每次调用都会新建一条连接，用完记得 cursor.close() + conn.close() 释放资源
def get_conn():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', '3306')),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'todo_app'),
        charset='utf8mb4',
    )


# 根路径：最简单的欢迎/健康检查接口，访问 http://localhost:5000/ 能看到这段文字
@app.route('/')
def hello():
    return '你好，欢迎访问 TODO 后端！'


# 查：GET /tasks —— 只返回"当前登录用户"的未删除任务
# 可选查询参数：?status=active 只查未完成、?status=done 只查已完成
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """查询当前登录用户的任务列表，返回 JSON 数组（每个元素是一个任务字典）。"""
    # 从 session 拿当前登录用户 id；没登录（session 里没有 user_id）就拒绝访问
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    # 读查询参数：URL 里 ?status=done 这种，request.args 里能取到
    status = request.args.get('status')

    conn = get_conn()
    cursor = conn.cursor()

    # 动态拼 SQL：固定条件（未删除 + 当前用户）写死，状态条件按参数追加
    # is_deleted = 0 过滤掉"软删除"的任务（删除只是打标记，数据还在库里）
    # user_id = %s 保证只查得到自己的任务（按用户隔离）
    sql = "SELECT id, name, done, created_at, category, due_date FROM tasks WHERE is_deleted = 0 AND user_id = %s"
    params = [user_id]

    # 根据查询参数追加状态过滤条件：active=未完成，done=已完成
    if status == 'active':
        sql += " AND done = 0"
    elif status == 'done':
        sql += " AND done = 1"

    # 按 id 升序排列，保证每次返回顺序稳定
    sql += " ORDER BY id"

    cursor.execute(sql, params)   # 用参数化查询执行，params 会替换掉 %s，防止 SQL 注入
    rows = cursor.fetchall()      # 取出所有符合条件的行
    tasks = []
    for row in rows:
        # 把数据库里的一行转成字典方便前端使用，布尔/时间都做类型转换
        tasks.append({
            "id": row[0],
            "name": row[1],
            "done": bool(row[2]),          # 数据库里的 0/1 转成 True/False
            "created_at": str(row[3]),     # datetime 转成字符串
            "category": row[4],
            "due_date": str(row[5]) if row[5] else None,  # 有截止时间转字符串，没有就是 None
        })
    cursor.close()   # 及时关闭游标和连接，释放数据库资源
    conn.close()
    return jsonify(tasks)   # 把列表转成 JSON 数组返回


# 增：POST /tasks —— 新建一条任务，归属当前登录用户
@app.route('/tasks', methods=['POST'])
def add_task():
    """新增任务。请求体 JSON 里带 name（必填）、category、due_date（都可选）。"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    data = request.get_json()               # 解析请求体里的 JSON
    name = data.get('name')
    category = data.get('category', '')   # 没传分类就默认空字符串
    due_date = data.get('due_date') or None   # 空字符串转成 NULL（表示"没有截止时间"）
    if not name:
        return jsonify({"error": "任务名不能为空"}), 400

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        # done 字段直接写死 FALSE，新任务默认"未完成"
        "INSERT INTO tasks (name, done, user_id, category, due_date) VALUES (%s, FALSE, %s, %s, %s)",
        (name, user_id, category, due_date),
    )
    conn.commit()                    # INSERT 后必须 commit 才会真正写入数据库
    new_id = cursor.lastrowid        # 拿到刚插入这条记录的自增 id
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "name": name, "done": False, "category": category, "due_date": due_date}), 201


# 删：DELETE /tasks/<id> —— 只能删自己的（WHERE 里加了 user_id）
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """软删除任务：不真正删数据，只把 is_deleted 标记成 1。"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    conn = get_conn()
    cursor = conn.cursor()
    # 注意：这里是 UPDATE 而不是 DELETE —— 软删除只打标记，任务还在库里，查询时被过滤掉
    # WHERE 里同时带 id 和 user_id，防止用户删别人的任务
    cursor.execute("UPDATE tasks SET is_deleted = 1 WHERE id = %s AND user_id = %s", (id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "删除成功"})


# 改：PUT /tasks/<id> —— 只能改自己的
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """更新任务：修改名称 name 和完成状态 done。"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    data = request.get_json()
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        # 同样带 user_id 限制，只能改自己的任务
        "UPDATE tasks SET name = %s, done = %s WHERE id = %s AND user_id = %s",
        (data.get('name'), data.get('done'), id, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "更新成功"})


# 注册：POST /register —— 创建新用户
@app.route('/register', methods=['POST'])
def register():
    """注册新账号：用户名不能重复，密码用 bcrypt 加密后存储。"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    conn = get_conn()
    cursor = conn.cursor()

    # 先查用户名是否已被占用
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():   # 查到了就说明用户名已存在
        cursor.close()
        conn.close()
        return jsonify({"error": "用户名已存在"}), 409

    # bcrypt 加密密码：绝不把明文密码存进数据库
    # encode('utf-8') 把字符串转成字节，hashpw 需要字节类型输入
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        # 存的是加密后的哈希值（decode 转回字符串再存入数据库）
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, hashed.decode('utf-8')),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "注册成功"}), 201


# 登录：POST /login —— 校验用户名密码，成功后写入 session
@app.route('/login', methods=['POST'])
def login():
    """登录：查到用户并用 bcrypt 校验密码，成功后把 user_id 存进 session。"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:   # 用户名不存在
        # 故意用"用户名或密码错误"这种模糊提示，不透露具体是哪个错了
        return jsonify({"error": "用户名或密码错误"}), 401

    user_id, password_hash = row
    # 校验密码：把用户输入的密码和库里存的哈希比对，bcrypt 会自动处理盐值
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({"error": "用户名或密码错误"}), 401

    session['user_id'] = user_id   # 登录成功，把用户 id 记到 session，之后接口都靠它认人
    return jsonify({"message": "登录成功"})


# 查"我是谁"：GET /me —— 前端用它判断是否已登录
@app.route('/me', methods=['GET'])
def me():
    """返回当前登录用户的信息（id 和用户名），未登录返回 401。"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:   # 理论上少见：session 里的 id 在用户表里查不到（比如用户已被删）
        return jsonify({"error": "未登录"}), 401
    return jsonify({"id": user_id, "username": row[0]})


# 退出：POST /logout —— 清除 session 里的登录状态
@app.route('/logout', methods=['POST'])
def logout():
    """退出登录：删掉 session 里的 user_id，之后访问需登录接口都会返回 401。"""
    session.pop('user_id', None)   # 清掉 session，等于"忘记你是谁"；None 表示没有这个键也不报错
    return jsonify({"message": "已退出登录"})


# 直接运行 python app.py 时启动开发服务器；debug=True 会开启自动重载和详细报错
if __name__ == '__main__':
    app.run(debug=True)
