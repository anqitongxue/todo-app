import os
import bcrypt
import pymysql
from flask import Flask, jsonify, request, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'dev-secret-key-please-change'   # 给 session cookie 签名的密钥
CORS(app, supports_credentials=True)   # 允许跨域 + 允许携带 cookie（session 需要）


# 连接数据库
def get_conn():
    return pymysql.connect(
        host='localhost',
        port=8080,
        user='root',
        password=os.environ.get('DB_PASSWORD', ''),
        database='todo_app',
        charset='utf8mb4',
    )


@app.route('/')
def hello():
    return '你好，欢迎访问 TODO 后端！'


# 查：GET /tasks —— 只返回"当前登录用户"的未删除任务
@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, done, created_at FROM tasks WHERE is_deleted = 0 AND user_id = %s ORDER BY id",
        (user_id,),
    )
    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "name": row[1],
            "done": bool(row[2]),
            "created_at": str(row[3]),
        })
    cursor.close()
    conn.close()
    return jsonify(tasks)


# 增：POST /tasks
@app.route('/tasks', methods=['POST'])
def add_task():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "任务名不能为空"}), 400

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (name, done, user_id) VALUES (%s, FALSE, %s)",
        (name, user_id),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "name": name, "done": False}), 201


# 删：DELETE /tasks/<id> —— 只能删自己的（WHERE 里加了 user_id）
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_deleted = 1 WHERE id = %s AND user_id = %s", (id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "删除成功"})


# 改：PUT /tasks/<id> —— 只能改自己的
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    data = request.get_json()
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET name = %s, done = %s WHERE id = %s AND user_id = %s",
        (data.get('name'), data.get('done'), id, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "更新成功"})


# 注册：POST /register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "用户名已存在"}), 409

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, hashed.decode('utf-8')),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "注册成功"}), 201


# 登录：POST /login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({"error": "用户名或密码错误"}), 401

    user_id, password_hash = row
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return jsonify({"error": "用户名或密码错误"}), 401

    session['user_id'] = user_id
    return jsonify({"message": "登录成功"})


# 查"我是谁"：GET /me —— 前端用它判断是否已登录
@app.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "未登录"}), 401

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({"error": "未登录"}), 401
    return jsonify({"id": user_id, "username": row[0]})


# 退出：POST /logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)   # 清掉 session，等于"忘记你是谁"
    return jsonify({"message": "已退出登录"})


if __name__ == '__main__':
    app.run(debug=True)
