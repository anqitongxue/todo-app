from flask import Flask, jsonify, request

app = Flask(__name__)

# 内存里的任务列表（重启就没了，第 6 章进数据库）
tasks = [
    {"id": 1, "name": "学 HTML", "done": True},
    {"id": 2, "name": "学 Vue", "done": False},
]


@app.route('/')
def hello():
    return '你好，欢迎访问 TODO 后端！'


# 查：GET /tasks —— 获取所有任务
@app.route('/tasks')
def get_tasks():
    return jsonify(tasks)


# 增：POST /tasks —— 新增一条任务
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "任务名不能为空"}), 400

    new_task = {"id": len(tasks) + 1, "name": name, "done": False}
    tasks.append(new_task)
    return jsonify(new_task), 201


# 删：DELETE /tasks/<id> —— 删除指定 id 的任务
# <int:id> 是"路径参数"：URL 里这一部分是整数，Flask 会把它存进变量 id
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:            # 遍历列表，找 id 匹配的那条
        if task['id'] == id:
            tasks.remove(task)    # 找到了就删掉
            return jsonify({"message": "删除成功"})
    return jsonify({"error": "没找到这个任务"}), 404   # 没找到 → 404


# 改：PUT /tasks/<id> —— 更新指定 id 的任务
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == id:
            # data.get('name', task['name'])：有新值就用新的，没传就保留原来的
            task['name'] = data.get('name', task['name'])
            task['done'] = data.get('done', task['done'])
            return jsonify(task)
    return jsonify({"error": "没找到这个任务"}), 404


if __name__ == '__main__':
    app.run(debug=True)
