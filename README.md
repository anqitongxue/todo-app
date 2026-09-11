# TODO.app

一个前后端分离的 **TODO（待办事项）应用**，支持多用户注册登录、任务分类、完成状态、筛选与搜索。

## 功能

- 用户注册 / 登录 / 退出（密码用 bcrypt 加密存储，每个用户只看得到自己的任务）
- 任务的增、删、改、查（删除采用软删除，可恢复）
- 完成状态勾选（完成后划线置灰）
- 任务分类（自定义分类名）
- 截止时间
- 按状态筛选（全部 / 进行中 / 已完成）
- 关键词搜索

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3 + Vite |
| 后端 | Flask（Python） |
| 数据库 | MySQL |
| 认证 | Flask Session（cookie）+ bcrypt |

## 目录结构

```
todo-app/
├── frontend/                 # Vue 前端
│   └── src/
│       ├── App.vue           # 主组件（登录 + 任务列表）
│       └── components/
│           └── TaskItem.vue  # 单条任务组件
├── backend/                  # Flask 后端
│   ├── app.py                # 所有接口（认证 + 任务 CRUD）
│   ├── requirements.txt      # Python 依赖
│   └── .gitignore
├── schema.sql                # 建库建表脚本
├── plan.md                   # 学习计划
├── progress.md               # 进度记录
└── README.md
```

## 快速开始

### 前置条件

- Python 3
- Node.js
- MySQL

### 1. 初始化数据库

```bash
mysql -P 8080 -u root -p < schema.sql
```

> 注意：本项目环境里 MySQL 用的是 **8080** 端口（不是默认 3306）。如果你的 MySQL 是默认端口，把 `-P 8080` 去掉即可。

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv .venv

# 安装依赖
pip install -r requirements.txt

# 设置数据库密码环境变量后启动（把「你的密码」换成实际密码）
# Windows PowerShell：$env:DB_PASSWORD = "你的密码"
DB_PASSWORD=你的密码 .venv/Scripts/python app.py
```

后端默认运行在 `http://localhost:5000`。

### 3. 启动前端

```bash
cd frontend
npm install      # 首次
npm run dev
```

浏览器打开终端提示的地址（默认 `http://localhost:5173`）。

### 4. 使用

打开前端页面 → 注册一个账号 → 登录 → 添加任务。

## 环境变量

| 变量 | 说明 |
|------|------|
| `DB_PASSWORD` | MySQL 数据库密码。后端从环境变量读取，不写死在代码里 |

## 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/register` | 注册 |
| POST | `/login` | 登录 |
| POST | `/logout` | 退出 |
| GET | `/me` | 当前登录用户 |
| GET | `/tasks?status=active` | 任务列表（可按 `active`/`done` 筛选） |
| POST | `/tasks` | 添加任务 |
| PUT | `/tasks/<id>` | 更新任务（名称 / 完成状态） |
| DELETE | `/tasks/<id>` | 删除任务（软删除） |
