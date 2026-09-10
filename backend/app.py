import os
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # 允许跨域：让前端(5173)能调这个后端(5000)


# 连接数据库的工具函数：密码从"环境变量"读，不写死在代码里（安全）
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


# 查：GET /tasks —— 只查"没删除"的任务（软删除的过滤）
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, done, created_at FROM tasks WHERE is_deleted = 0 ORDER BY id")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "name": row[1],
            "done": bool(row[2]),
            "created_at": str(row[3]),   # datetime 转成字符串才能放进 JSON
        })
    cursor.close()
    conn.close()
    return jsonify(tasks)


# 增：POST /tasks
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "任务名不能为空"}), 400

    conn = get_conn()
    cursor = conn.cursor()
    # 参数化查询：用 %s 占位符，值单独传，防止 SQL 注入
    cursor.execute("INSERT INTO tasks (name, done) VALUES (%s, FALSE)", (name,))
    conn.commit()
    new_id = cursor.lastrowid   # 拿到刚插入那行的自增 id
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "name": name, "done": False}), 201


# 删：DELETE /tasks/<id> —— 软删除（打标记，不真删）
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_deleted = 1 WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "删除成功"})


# 改：PUT /tasks/<id>
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET name = %s, done = %s WHERE id = %s",
        (data.get('name'), data.get('done'), id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "更新成功"})


if __name__ == '__main__':
    app.run(debug=True)
