# 进度与学习记录

> 本文件持续记录我们**每次做了什么**、**学到了什么知识**。
> 目的是：随时能回顾"我们已经走到哪了、学会了哪些东西"。
>
> **更新规则**：每完成一小步（一个功能、一个章节的一节），我会追加一条记录，并更新"项目当前状态"。

---

## 一、项目当前状态

| 项目 | 状态 |
|------|------|
| 当前阶段 | 阶段二：前后端联调 |
| 当前章节 | 第 9 章：功能增强（✅ 已完成，含界面美化） |
| 下一步 | 第 10 章：Git 进阶与远程协作 |
| 已完成 | 环境搭建 + Git + 第 3~9 章（含多用户、分类、筛选、搜索、截止时间） |

---

## 二、记录（按时间倒序）

### 2026-09-11 · 第 9 章完成：界面美化 🎉

**做了什么：**
- 页面换成柔和渐变背景 + 白色圆角卡片。
- 按钮/输入框/筛选按钮加 hover、focus 反馈和过渡动画。
- 任务项加悬停阴影、超长文字省略号、勾选框绿色主题色、删除按钮改为淡红悬停变红。

**学到了什么：**
- box-shadow 阴影、transition 过渡、linear-gradient 渐变。
- 伪类 :hover / :focus / :active 表示元素的不同状态。
- accent-color 给表单控件换主题色；text-overflow: ellipsis 显示省略号。

**里程碑**：第 9 章全部完成 ✅。TODO 应用功能完整（多用户 + 分类 + 完成状态 + 筛选 + 搜索 + 截止时间），界面也打磨到位。按你的要求，排序/优先级/加载中提示等可选增强就不做了。

### 2026-09-11 · 第 9 章第六步：任务截止时间

**做了什么：**
- 数据库 `tasks` 表加 `due_date` 列（DATE，可空）。
- 后端 GET /tasks 返回 due_date（无则 null）；POST 接收 due_date（空字符串转 None → NULL）。
- 前端加 `<input type="date">` 日期选择框，TaskItem 用橙色小标签显示截止时间。

**学到了什么：**
- 加字段的三层套路再走一遍（数据库 → 后端 → 前端），和"分类"完全一致。
- DATE 类型存日期；`<input type="date">` 选日期。
- NULL vs 空字符串：数据库用 NULL 表示"没有值"，输入框没填给 ''，插入前要 `or None` 转换。

**里程碑**：第 9 章第六步完成 ✅。

### 2026-09-11 · 第 9 章第五步：后端筛选（查询参数）

**做了什么：**
- 后端 `GET /tasks` 支持 `?status=active|done` 查询参数，用 `request.args.get()` 读取，动态拼 SQL 的 WHERE 条件。
- 前端状态筛选从 `computed` 移到后端：`loadTasks` 拼 `?status=` URL，加 `setFilter` 点击时重新拉取。
- `computed` 只保留关键词搜索；空状态改成一条三元表达式区分"没任务 vs 没匹配"。

**学到了什么：**
- 查询字符串（Query String）：URL 里 `?` 后面的 key=value，是"带参数请求"的通用方式。
- `request.args.get('status')` 读查询参数（对比 `request.get_json()` 读请求体）。
- 动态拼 SQL 的安全姿势：用 if 分支选写死的固定条件，而不是直接把用户输入拼进 SQL（防注入）。
- 前端筛 vs 后端筛的分工：状态交给数据库（SQL WHERE），关键词留在前端（computed）。
- 移动筛选层级后，"列表为空"的含义变了，空状态要重新判断。

**里程碑**：第 9 章第五步完成 ✅。状态筛选从"前端"迁移到"后端"，掌握了前后端筛选的分工。

### 2026-09-11 · 第 9 章第四步：搜索（按关键词过滤）

**做了什么：**
- `App.vue` 加 `search` 状态，`filteredTasks` 计算属性扩展成"先按状态筛、再按关键词搜"的链式过滤。
- 加搜索输入框，用 `v-model` 绑定关键词。
- 空状态文案改成"没有匹配的任务"。

**学到了什么：**
- 搜索和筛选是同一套思路：都用 `computed`，只是匹配规则不同。
- 三个字符串方法：`includes()` 判断是否包含、`trim()` 去首尾空格、`toLowerCase()` 转小写实现英文大小写不敏感。
- 链式过滤：computed 里一步步 `filter`，先状态后关键词，逻辑清晰、好扩展。

**里程碑**：第 9 章第四步完成 ✅。

### 2026-09-11 · 第 9 章第三步：按状态筛选（前端筛选）

**做了什么：**
- `App.vue` 加 `filter` 状态 + `computed` 计算属性 `filteredTasks`，按"全部/进行中/已完成"过滤。
- 加三个筛选按钮，用 `:class` 高亮当前选中项；列表改遍历 `filteredTasks`。
- 空状态分两种情况：真没任务 vs 当前筛选下没任务。

**学到了什么：**
- 筛选两条路：前端筛（数据在内存里用 JS 过滤）vs 后端筛（`?status=done` 查询参数 + SQL WHERE），数据量小选前端筛。
- `computed` 计算属性：由别的数据算出来、自动重算，适合"过滤后的列表"。
- `filter()` 数组方法：返回满足条件的新数组，原数组不变。
- `npm run build` 编译一次能快速自查语法错误（不用每次手动开页面）。

**里程碑**：第 9 章第三步完成 ✅。

### 2026-09-11 · 第 9 章第二步：完成状态（勾选完成）

**做了什么：**
- `TaskItem` 加勾选框（`:checked` + `@change`），勾选时 emit `toggle` 事件上报。
- 完成任务加删除线 + 变灰（`:class` 动态绑定 + `text-decoration: line-through`）。
- `App.vue` 加 `toggleTask`，调 `PUT /tasks/<id>` 更新 done。

**学到了什么：**
- 加功能不一定要改三层——done 字段后端早就支持，这次只改前端。
- checkbox 不能用 `v-model` 直接绑 prop（子组件不能改 prop），要用 `:checked`（只读）+ `@change`（上报）——单向数据流的体现。
- `:class="{ done: task.done }"` 动态绑定 class：条件为真才加这个类。
- 踩坑：现有 PUT 会同时更新 name 和 done，所以切换时要把 name 原样带上，否则会被清空。

**里程碑**：第 9 章第二步完成 ✅。

### 2026-09-11 · 第 9 章开始：给任务加"分类"字段

**做了什么：**
- 数据库 `tasks` 表用 `ALTER TABLE` 加 `category` 列（VARCHAR(50)，默认空字符串）。
- 后端 `GET /tasks` 返回 `category`；`POST /tasks` 接收 `category`（不传则默认空）。
- 前端加"分类"输入框，`TaskItem` 用绿色小标签显示分类。

**学到了什么：**
- 加新功能的通用思路：**数据库 → 后端 → 前端** 三层依次改。
- `ALTER TABLE` 改表结构；`VARCHAR(50)` 是变长字符串；`DEFAULT ''` 给旧数据兜底。
- `data.get('category', '')` 的默认值写法 = **向后兼容**（旧请求不传也不报错）。
- 踩坑：Windows Git Bash 用 curl 发中文会按 GBK 编码，Flask 只认 UTF-8，导致 400；浏览器 fetch 会自动用 UTF-8，所以页面正常。

**里程碑**：第 9 章第一步完成 ✅。

### 2026-09-10 · 第 8 章完成：用户认证 🎉

**做了什么：**
- 建 `users` 表，用 bcrypt 哈希存密码。
- 写注册 / 登录 / 退出接口，用 Flask Session 记住登录态。
- `tasks` 表加 `user_id`，任务按用户隔离；未登录拦截 401。
- 前端加登录/注册界面，fetch 带 `credentials` 携带 cookie。

**学到了什么：**
- 密码不能存明文，用 bcrypt 哈希（hashpw 存、checkpw 验证）。
- Session vs JWT：Session 服务器记状态、JWT 无状态。
- 数据隔离：任务加 user_id 外键，查询/操作都带 user_id。
- 跨域带 cookie：后端 `supports_credentials`、前端 `credentials:'include'`。
- 安全细节：登录失败不区分"用户名不存在"和"密码错误"。

**里程碑**：第 8 章完成 ✅。多用户、数据隔离、带认证的 TODO 应用达成。

### 2026-09-10 · 第 8 章开始：认证概念 + 用户表

**做了什么：**
- 理解认证流程（注册 → 登录 → 数据隔离）和密码哈希（不存明文）。
- 建 `users` 表（username 唯一、password_hash 存哈希）。
- 把 MySQL bin 加进 PATH，以后直接敲 `mysql` 就能连。

**学到了什么：**
- 认证：确认"你是谁"；密码不能存明文，要存哈希。
- 哈希是单向函数：明文 → 哈希可算，哈希 → 明文不可反推。
- bcrypt 是专门的密码哈希算法。
- users 表：`username UNIQUE` 防重名，`password_hash` 存哈希值。

### 2026-09-10 · 第 7 章完成：前后端打通 🎉

**做了什么：**
- 后端接 MySQL：pymysql 读写 + 软删除 + 参数化查询 + 环境变量存密码。
- 加 `flask-cors` 解决跨域。
- 前端用 `fetch` 调后端接口，增、删、查全部走真实数据库。
- 数据存进 MySQL，刷新页面不丢。

**学到了什么：**
- `fetch` 发 HTTP 请求、`async/await` 处理异步、`onMounted` 生命周期钩子。
- `JSON.stringify`（对象→JSON）与 `res.json()`（JSON→对象）互转。
- 同源策略与跨域（CORS）。
- 前端状态 vs 后端数据：数据现在来自后端 + 数据库。

**里程碑**：第 7 章完成 ✅，真·全栈闭环达成，阶段一圆满收官。

### 2026-09-10 · 第 6 章完成：pymysql 读写 + ORM 概念 🎉

**做了什么：**
- 装 pymysql，写 `db_demo.py`：连接 MySQL（端口 8080）、插入一条任务、查出来。
- 装 DBeaver 可视化工具，连接数据库查看数据。
- 学了 ORM 概念（对比原生 SQL 和 SQLAlchemy），决定本项目暂用 pymysql 原生 SQL。

**学到了什么：**
- `pymysql.connect()` 连接、`cursor.execute()` 执行 SQL、`conn.commit()` 提交、`fetchall()` 取结果。
- 事务：增删改之后要 commit 才真正写入。
- ORM：操作对象、框架生成 SQL，类似 Vue 之于 DOM。
- 安全：密码不能写死在代码里、不能提交进 Git。
- `requirements.txt` 记录依赖。

**里程碑**：第 6 章完成 ✅。交付物"用代码往 MySQL 写入并读出任务"达成。

### 2026-09-10 · 第 6 章开始：建库建表 + 解决端口问题

**做了什么：**
- 排查 MySQL 连接问题：发现本机 MySQL 端口是 **8080**（非默认 3306），用 `-P 8080` 连接成功。
- 创建数据库 `todo_app` 和 `tasks` 表（id 自增主键、name、done）。

**学到了什么：**
- 关系型数据库核心概念：表 / 行 / 列 / 主键 / 外键。
- `CREATE DATABASE` 建库、`CREATE TABLE` 建表。
- 列类型：INT、VARCHAR、BOOLEAN；`AUTO_INCREMENT` 自增主键。
- `ERROR 2003` = 连不上 MySQL（端口不对或服务没起）。
- MySQL 的 BOOLEAN 实际存成 tinyint(1)。

### 2026-09-10 · 第 5 章：DELETE/PUT + 路径参数

**做了什么：**
- 加 `DELETE /tasks/<id>` 和 `PUT /tasks/<id>` 接口，完成后端增删改查全套 CRUD。
- 认识了路径参数 `<int:id>`。

**学到了什么：**
- 路径参数：`<int:id>` 从 URL 里取整数参数，用来定位具体资源（如 `/tasks/3`）。
- 遍历列表找 id 匹配、`list.remove()` 删除、找不到返回 404。
- `data.get('key', 默认值)` 的安全取值写法。

### 2026-09-10 · 第 5 章：POST 新增接口 + 状态码 + curl

**做了什么：**
- 加 `POST /tasks` 接口，用 `request.get_json()` 读请求体，新增任务。
- 认识了 HTTP 状态码（200/201/400/404/500）。

**学到了什么：**
- 同一个 URL `/tasks`，用不同 HTTP 方法实现不同操作（GET 查 / POST 增）。
- `methods=['POST']` 指定路由接受的方法（默认只有 GET）。
- `request.get_json()` 读前端发来的 JSON；`data.get('name')` 安全取值。
- 状态码：`return jsonify(...), 201` 返回"数据 + 状态码"。

### 2026-09-10 · 第 5 章：返回 JSON + HTTP 方法 + RESTful

**做了什么：**
- 把 `app.py` 升级成返回 JSON：`GET /tasks` 用 `jsonify` 返回任务列表。
- 认识了 HTTP 方法（GET/POST/PUT/DELETE）和 RESTful 风格。

**学到了什么：**
- 后端要返回"结构化数据"（JSON），而不是给人看的纯文本。
- RESTful：URL 用名词表资源（`/tasks`）、HTTP 方法表操作（GET 查 / POST 增 / PUT 改 / DELETE 删）。
- `jsonify()` 把 Python 的列表/字典转成 JSON 返回。
- Python 的 dict（字典）≈ JS 的对象，list（列表）≈ JS 的数组。

### 2026-09-10 · 第 5 章开始：venv + 第一个 Flask 接口

**做了什么：**
- 创建 `backend` 目录，用 `python -m venv .venv` 建虚拟环境。
- 用 pip 在虚拟环境里安装 Flask 3.1.3。
- 写 `backend/app.py`，定义第一个路由 `/`，返回一段文字。

**学到了什么：**
- 后端：跑在服务器上、处理请求、返回数据的部分，用 Flask 写。
- venv：给项目独立的 Python 环境，避免依赖冲突；pip 是 Python 的包管理器。
- Flask 基本结构：`Flask(__name__)` 创建应用、`@app.route('/')` 定义路由、`app.run()` 启动。

### 2026-09-10 · 第 4 章完成：美化 + 清理 🎉

**做了什么：**
- 给 Vue 版 TODO 加上样式：全局 body 样式放 `src/style.css`，组件样式用 `<style scoped>` 分别写在 `App.vue` 和 `TaskItem.vue`。
- 删除没用的 `HelloWorld.vue` 和 `src/assets/` 里的示例图片。

**学到了什么：**
- `<style scoped>`：样式只作用于当前组件、不泄露；全局样式（body）放 `style.css`。
- 组件各自维护自己的样式，职责更清晰。

**里程碑**：第 4 章全部完成 ✅。Vue 版 TODO（增删 + 条件渲染 + 组件化 + 样式）功能与第 3 章一致。

### 2026-09-10 · 第 4 章：组件拆分（props 与 emit）

**做了什么：**
- 新建 `TaskItem.vue` 组件，把"一条任务"从 `App.vue` 里拆出来。
- `App.vue` 用 `<TaskItem>` + `v-for` 渲染列表。

**学到了什么：**
- 组件化：把界面拆成职责单一的独立组件。
- props（父 → 子）：父组件用 `:task="task"` 传数据，子组件用 `defineProps` 接收。
- emit（子 → 父）：子组件用 `defineEmits` 声明、`emit('remove', index)` 发事件，父组件用 `@remove` 监听。
- 单向数据流：数据只在父组件手里，子组件要改数据必须"上报"，由父改。

### 2026-09-10 · 第 4 章：删除 + v-if（条件渲染）

**做了什么：**
- 给每条任务加"删除"按钮，`removeTask(index)` 用 `splice` 从响应式数组删任务。
- 加 `v-if`，列表为空时显示提示语"还没有任务，先添加一条吧～"。

**学到了什么：**
- 响应式删除：`splice` 一下数组，对应的 `<li>` 自动消失，不需要第 3 章那样手动 `remove()`。
- 事件处理传参：`@click="removeTask(index)"`（带括号、传参数）对比 `@click="addTask"`（不带括号）。
- `v-if` 条件渲染：条件为真才渲染元素，为假则从页面移除。

### 2026-09-10 · 第 4 章：用 Vue 重写 TODO（添加 + 列表）

**做了什么：**
- 把 `App.vue` 重写成 TODO 页面，实现"添加 + 显示列表"。
- 认识了 `ref` 响应式数据，以及 `v-model`、`v-for`、`@click`、`{{ }}` 这几个核心指令。

**学到了什么：**
- `ref` 声明响应式数据：script 里 `.value` 访问，模板里直接写变量名。
- `v-model` 双向绑定：一行替代第 3 章的"手动读值 + 手动清空"。
- `v-for` 列表渲染：数据变，界面自动渲染，不再手动 createElement/appendChild。
- `@click` 事件绑定（等价于 `v-on:click`，等价于第 3 章的 addEventListener）。
- 数据驱动视图：只 `push` 数据，不操作 DOM。

### 2026-09-10 · 第 4 章开始：用 Vite 创建 Vue 项目

**做了什么：**
- 用 `npm create vite@latest frontend -- --template vue` 生成 Vue 项目骨架。
- 用 `npm install` 安装依赖（vue、vite 等）。
- 认识了项目的 4 个关键文件：`index.html`、`package.json`、`src/main.js`、`src/App.vue`。

**学到了什么：**
- Vue 的核心思想：数据驱动视图（声明式 + 响应式），对比第 3 章手动操作 DOM 的痛点。
- 组件化：界面拆成可复用的 `.vue` 单文件组件（template + script + style）。
- Vite：构建工具，负责脚手架、开发服务器、打包。
- 启动流程：index.html → main.js → `createApp(App).mount('#app')` → 渲染模板。
- `package.json`：记录依赖（dependencies）和脚本（scripts，`npm run dev` = `vite`）。

### 2026-09-10 · 第 3 章完成：盒模型与 Flex 布局 🎉

**做了什么：**
- 速览盒模型（content / padding / border / margin）和 Flex 布局两个 CSS 知识点。
- 用 Flex 美化页面：输入框 + 按钮横排一行，列表项做成"文字靠左、删除按钮靠右"的白色卡片。

**学到了什么：**
- 盒模型：每个元素都是一个盒子，从里到外 content → padding → border → margin。
- Flex：容器 `display: flex` 让子元素横向排列；`justify-content: space-between` 两端对齐；`align-items: center` 垂直居中；`gap` 控制间距；`flex: 1` 让元素占满剩余空间。
- `list-style: none` 去掉列表默认圆点，`padding: 0` 去掉 `<ul>` 默认缩进。

**里程碑**：第 3 章全部完成 ✅。阶段零（准备与打地基）也随之完成。

### 2026-09-10 · 第 3 章：按回车也能添加（事件对象）

**做了什么：**
- 给输入框加 `keydown` 监听，按 Enter 键也能添加任务。
- 把"从输入框取文字并添加"的逻辑抽成 `addFromInput` 函数，按钮点击和回车共用。

**学到了什么：**
- 键盘事件 `keydown`：按下按键时触发。
- 事件对象 `event`：监听函数收到的参数，`event.key` 是按下的是哪个键（回车键的值是 `"Enter"`）。
- 代码复用（DRY）：两种触发方式共用同一个函数，不重复写逻辑。
- 传函数 vs 调用函数：`addEventListener("click", addFromInput)` 传的是函数本身（不加括号）；加了括号 `()` 就会立刻调用。

### 2026-09-10 · 第 3 章：实现"删除"，章节功能完成 🎉

**做了什么：**
- 改写 [ch03/script.js](ch03/script.js)，给每条任务加"删除"按钮，点击后同时从页面和内存数组里删掉。
- 把"添加一项"的逻辑抽成 `addTask` 函数，代码更清晰、可复用。
- 给 [ch03/style.css](ch03/style.css) 加 `.del` 样式，删除按钮变成红色小按钮。

**学到了什么：**
- 嵌套事件：每个删除按钮有自己的监听器，点击时只删自己那一项（涉及"闭包"：内层函数记住了外层函数的变量）。
- `元素.remove()` 从页面删元素；`数组.splice(位置, 个数)` 从数组删元素。
- `indexOf` 在数组里找元素位置（找不到返回 -1）；`!==` 是"不等于"。
- 代码复用：把重复逻辑抽成函数 `addTask`。

**里程碑**：第 3 章核心交付物（能添加、能删除的静态 TODO 页面）已完成 ✅。

### 2026-09-10 · 第 3 章：DOM 操作与事件（实现"添加"）

**做了什么：**
- 改写 [ch03/script.js](ch03/script.js)，实现点击"添加"按钮 → 读输入框文字 → 生成新 `<li>` 挂到页面上。
- 把 [ch03/index.html](ch03/index.html) 里写死的三个 `<li>` 清空，列表改由 JS 动态生成。

**学到了什么（DOM 与事件层面）：**
- `document.querySelector(".类名")` 用 CSS 选择器在 JS 里选中页面元素。
- 读输入框的值用 `.value`；造元素用 `document.createElement`；挂载用 `appendChild`。
- 事件：`addEventListener("click", 函数)` 监听按钮点击，触发"回调函数"。
- 用数组 `tasks` 在内存里记录任务（刷新就丢，第 6 章再存数据库）。
- 防呆：`if (text === "") return;` 阻止加入空任务；`===` 是"比较"，`=` 才是"赋值"。

### 2026-09-10 · 第 3 章：JavaScript 基础语法

**做了什么：**
- 新建 [ch03/script.js](ch03/script.js)，用 `<script>` 标签引入到 [ch03/index.html](ch03/index.html)。
- 认识了 JS 的四个基础概念：变量、数组、对象、函数，并用 `console.log` 打印到控制台。

**学到了什么（JS 层面）：**
- JS 通过 `<script>` 标签引入，通常放在 `<body>` 末尾（保证 HTML 元素先加载完）。
- 变量用 `let`（可改）或 `const`（不可改）声明。
- 数组 `[]` 装一列数据，对象 `{}` 装"带名字"的数据。
- 函数用 `function` 定义，是可重复调用的代码块。
- 用浏览器开发者工具（F12）的控制台，配合 `console.log` 观察代码输出、调试代码。

### 2026-09-10 · 第 3 章：CSS 基础（给骨架穿衣服）

**做了什么：**
- 新建 [ch03/style.css](ch03/style.css)，给 TODO 页面加上颜色、字体、边框、圆角、间距等样式。
- 在 [ch03/index.html](ch03/index.html) 里用 `<link>` 引入 CSS，并给元素加了 `class`。
- 认识了三种引入 CSS 的方式，以及元素选择器、类选择器。

**学到了什么（CSS 层面）：**
- CSS 基本语法：`选择器 { 属性: 值; }`，一条规则 = "装饰谁" + "装饰成什么"。
- 引入 CSS 的三种方式：内联（`style` 属性）、内部（`<style>` 标签）、外部文件（`<link>`，最推荐）。
- 选择器：元素选择器（写标签名）、类选择器（`.类名`）、id 选择器（`#id`）。
- 常用属性：`color`（文字色）、`background-color`（背景色）、`font-size`（字号）、`border`/`border-radius`（边框/圆角）、`padding`（内边距）。
- 属性值简写：`margin: 上下 左右`，两个值依次代表垂直、水平方向。

### 2026-09-10 · 第 3 章开始：HTML 基础与静态骨架

**做了什么：**
- 进入第 3 章，理解网页"三件套"的分工：HTML（骨架）、CSS（外观）、JavaScript（行为）。
- 新建 [ch03/index.html](ch03/index.html)，用纯 HTML 搭出 TODO 页面的静态骨架：标题 + 输入框 + 按钮 + 待办列表。
- 认识了 HTML 的基本结构：`<!DOCTYPE>`、`<html>`、`<head>`、`<body>`，以及几个常用标签。

**学到了什么（HTML 层面）：**
- 网页 = 结构（HTML）+ 样式（CSS）+ 行为（JS），三者各司其职。
- HTML 用**标签**写内容，标签通常成对出现（`<h1>`…`</h1>`）。
- 标签可以**嵌套**（`<ul>` 里套 `<li>`），形成父子关系。
- **属性**给标签补充信息，如 `<input type="text">` 里的 `type` 决定输入框类型。

### 2026-08-24 · 第 2 章完成：Git 基础与 GitHub 推送

**做了什么：**
- `git init` 把项目文件夹初始化成 Git 仓库
- `git config` 设置身份（名字 + 邮箱）
- 做了**第一次 commit**（4 个 md 文件，提交号 e820b47）
- 在 GitHub 建了远程仓库 `anqitongxue/todo-app`，用 `git remote add` + `git push` 推了上去
- 配置 Git 走本地代理 `127.0.0.1:7890`（国内访问 GitHub 需要）
- 共完成 **3 次提交**并全部推送到 GitHub（初始化 → 更新进度 → 补充术语）

**学到了什么（Git 层面）：**
- Git 的"三步存档"模型：工作区 → 暂存区（`add`）→ 版本库（`commit`）
- 核心命令：`init` / `status` / `add` / `commit` / `log` / `remote` / `push`
- 什么是远程仓库、`origin` 这个代号的含义
- commit message 要写得简短、能说明"这次改了什么"
- Windows 常见坑：换行符（LF/CRLF）警告用 `core.autocrlf=false` 关掉；PowerShell 中文乱码改用 Git Bash 根治

### 2026-08-24 · 第 1 章完成：开发环境与工具

**做了什么：**
- 确认并验证了 5 样开发工具，全部就绪。

| 工具 | 版本 | 状态 |
|------|------|------|
| VS Code | - | ✅ |
| Git | 2.44.0 | ✅ |
| Python | 3.14.7 | ✅ |
| Node.js | 24.19.0（npm 11.17.0） | ✅ |
| MySQL | 9.7 | ✅（能登录） |

**学到了什么（环境与命令行层面）：**
- 什么是 **PATH 环境变量**：终端去哪里找命令的"清单"，装工具时勾选"Add to PATH"才能让命令被识别。
- Windows 的"假 Python"坑：没装真 Python 时，`python` 指向微软商店的占位程序，什么也不干。
- **执行策略（Execution Policy）**：PowerShell 默认禁止运行脚本，`npm` 因此被拦，用 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 放开本机脚本。
- **服务（Service）**：MySQL 是"常驻后台、开机自动运行"的服务，不是一次性命令，用 `Get-Service` 查看。
- **root 账号**：MySQL 的超级管理员账号，密码要记牢。

> 备注：曾发现机器上有多个旧 MySQL（8.0、桌面 zip 版 9.7 等），已全部清理，现在只剩一个干净的 MySQL 9.7。

### 2026-08-24

**做了什么：**
- 创建 [plan.md](plan.md)：把 2 个月的项目拆成 12 章、4 个阶段，每章定义了"交付物"。
- 创建 [requirements.md](requirements.md)：记录用户提出的要求，以及我们之间的协作约定。
- 创建 [progress.md](progress.md)：本文件，用于记录进度与学习。
- 创建 [glossary.md](glossary.md)：术语表，记录遇到的专业名词。

**学到了什么（项目规划层面）：**
- 一个完整全栈项目应该**先规划再动手**：拆阶段 → 拆章节 → 每章定一个"交付物"（判断是否完成的标志）。
- 长期合作中，用**文档固定"要求"和"约定"**很重要，避免方向跑偏、节奏不一致。
- 学习型项目应该**前后端分开跑通，再联调打通**，而不是一上来就三层一起写。

---

## 三、已学知识速查表（累积，用于复习）

> 随着项目推进，把每个章节的核心知识点填进来，方便日后复习和面试准备。

| 章节 | 核心知识点 | 简述 |
|------|-----------|------|
| 第 0 章（规划） | 项目规划方法 | 阶段 / 章节 / 交付物的拆解思路 |
| 第 1 章（环境） | PATH / 服务 / 执行策略 | 装好并验证 5 样工具 |
| 第 2 章（Git 上） | 三步存档模型 / 核心命令 / 远程推送 | 3 次提交并推送 GitHub |

---

> 说明：目前我们完成了"规划与搭建文档"，第 1 章（环境）、第 2 章（Git）已完成，下一步进入第 3 章（HTML/CSS/JS）。等开始写代码后，这里会逐步记录前端、后端、数据库等知识点。
