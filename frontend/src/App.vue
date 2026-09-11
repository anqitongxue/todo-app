<script setup>
// ========== App.vue：应用主组件 ==========
// 职责：登录/注册界面、任务增删查、完成状态切换、
//       状态筛选（走后端）、关键词搜索（computed）、分类/截止时间输入
import { ref, onMounted, computed } from 'vue'
import TaskItem from './components/TaskItem.vue'

// 后端接口地址前缀：空字符串 = 相对路径。
// 开发时由 Vite 代理转发到后端，生产时由 Nginx 代理转发。
const API = ''

// ---------- 登录相关状态 ----------
const username = ref('')      // 用户名输入框内容
const password = ref('')      // 密码输入框内容
const loggedIn = ref(false)   // 是否已登录
const currentUser = ref('')   // 当前登录的用户名

// ---------- 任务相关状态 ----------
const newTask = ref('')        // 新增任务名称
const newCategory = ref('')    // 新增任务分类
const newDueDate = ref('')     // 新增任务截止时间（日期字符串）
const tasks = ref([])          // 从后端拉取的任务列表
const filter = ref('all')      // 状态筛选：'all'（全部）| 'active'（进行中）| 'done'（已完成）
const search = ref('')         // 搜索关键词（用于前端按名称过滤）

// 计算属性 filteredTasks：返回展示用的任务列表。
// 只做"关键词搜索"（按任务名称模糊匹配，忽略大小写）；
// 状态筛选已交给后端处理，这里不再重复筛状态。
// 返回值：过滤后的任务数组；关键词为空时原样返回 tasks。
const filteredTasks = computed(() => {
    const kw = search.value.trim().toLowerCase()   // 去掉首尾空格并转小写，便于比较
    if (!kw) return tasks.value                     // 无关键词，直接返回全部任务
    return tasks.value.filter(t => t.name.toLowerCase().includes(kw))
})

// checkLogin：页面加载时检查是否已登录。
// 做什么：向后端 /me 发 GET 请求（携带 cookie，credentials: 'include'）。
// 若已登录（res.ok 为真），读取返回的用户名、标记已登录，并拉取任务列表。
// 参数：无。返回值：无（async 函数）。
async function checkLogin() {
    const res = await fetch(`${API}/me`, { credentials: 'include' })
    if (res.ok) {
        const data = await res.json()
        currentUser.value = data.username
        loggedIn.value = true
        loadTasks()
    }
}

// login：处理登录表单提交。
// 做什么：把用户名、密码 POST 到后端 /login（携带 cookie）。
// 成功：标记已登录、记录当前用户名并拉取任务；失败：弹窗提示。
// 参数：无（从 username/password 响应式状态读取）。返回值：无。
async function login() {
    const res = await fetch(`${API}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username: username.value, password: password.value }),
    })
    if (res.ok) {
        loggedIn.value = true
        currentUser.value = username.value
        loadTasks()
    } else {
        alert('用户名或密码错误')
    }
}

// register：处理注册表单提交。
// 做什么：把用户名、密码 POST 到后端 /register。
// 成功后直接调用 login() 完成登录；失败（如用户名已存在）弹窗提示。
// 参数：无。返回值：无。
async function register() {
    const res = await fetch(`${API}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.value, password: password.value }),
    })
    if (res.ok) {
        login()
    } else {
        alert('注册失败（用户名可能已存在）')
    }
}

// logout：退出登录。
// 做什么：向后端 /logout 发 POST 清除会话 cookie，并清空本地登录状态与任务列表。
// 参数：无。返回值：无。
async function logout() {
    await fetch(`${API}/logout`, { method: 'POST', credentials: 'include' })
    loggedIn.value = false
    currentUser.value = ''
    tasks.value = []
}

// loadTasks：从后端拉取任务列表。
// 做什么：向后端 /tasks 发 GET；若当前筛选不是 'all'，则拼接 ?status= 查询参数，由后端完成状态筛选。
// 返回结果直接写入 tasks 响应式状态。
// 参数：无。返回值：无。
async function loadTasks() {
    let url = `${API}/tasks`
    if (filter.value !== 'all') {
        url += `?status=${filter.value}`   // 把状态筛选交给后端处理
    }
    const res = await fetch(url, { credentials: 'include' })
    tasks.value = await res.json()
}

// setFilter：切换状态筛选。
// 参数 f：'all' | 'active' | 'done'。返回值：无。
// 做什么：更新 filter 状态，然后重新从后端拉取对应状态的任务。
function setFilter(f) {
    filter.value = f
    loadTasks()
}

// addTask：添加一条新任务。
// 做什么：把任务名称、分类、截止时间 POST 到后端 /tasks；
// 成功后清空输入框并重新拉取任务列表。名称为空时直接返回（不提交）。
// 参数：无（从 newTask/newCategory/newDueDate 读取）。返回值：无。
async function addTask() {
    const name = newTask.value
    if (name === '') return   // 名称为空时不提交
    await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name, category: newCategory.value, due_date: newDueDate.value }),
    })
    newTask.value = ''
    newCategory.value = ''
    newDueDate.value = ''
    loadTasks()
}

// removeTask：删除指定任务。
// 参数 id：要删除的任务 ID。返回值：无。
// 做什么：向后端 /tasks/{id} 发 DELETE 请求，成功后重新拉取任务列表。
async function removeTask(id) {
    await fetch(`${API}/tasks/${id}`, { method: 'DELETE', credentials: 'include' })
    loadTasks()
}

// toggleTask：切换任务的完成状态。
// 参数：id 为任务 ID；done 为新的完成状态（true/false，由子组件 TaskItem 传入）。
// 返回值：无。
// 做什么：先在本地找到该任务，再向后端 /tasks/{id} 发 PUT 更新完成状态，成功后重新拉取。
async function toggleTask(id, done) {
    const task = tasks.value.find(t => t.id === id)
    if (!task) return   // 找不到该任务时不做任何操作
    await fetch(`${API}/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name: task.name, done }),   // name 必须原样带上，否则后端会把名称清空
    })
    loadTasks()
}

// 组件挂载完成后立即执行 checkLogin，实现"刷新页面自动恢复登录状态"
onMounted(checkLogin)
</script>

<template>
    <div class="app">
        <h1 class="title">我的任务清单</h1>

        <!-- 未登录：显示登录/注册表单 -->
        <div v-if="!loggedIn" class="login-box">
            <input class="input" v-model="username" placeholder="用户名">
            <input class="input" v-model="password" type="password" placeholder="密码">
            <div class="login-actions">
                <button class="btn" @click="login">登录</button>
                <button class="btn ghost" @click="register">注册</button>
            </div>
        </div>

        <!-- 已登录：显示 TODO 和退出按钮 -->
        <div v-else>
            <p class="welcome">
                👋 {{ currentUser }}
                <button class="logout" @click="logout">退出</button>
            </p>

            <div class="add-area">
                <div class="add-row">
                    <input class="input" v-model="newTask" placeholder="输入一个新任务...">
                    <button class="btn" @click="addTask">添加</button>
                </div>
                <div class="add-meta">
                    <input class="input" v-model="newCategory" placeholder="分类（如：工作）">
                    <input class="input" type="date" v-model="newDueDate">
                </div>
            </div>

            <!-- 状态筛选按钮组：点击调用 setFilter 切换 filter，并重新走后端查询 -->
            <div class="filters">
                <button :class="{ active: filter === 'all' }" @click="setFilter('all')">全部</button>
                <button :class="{ active: filter === 'active' }" @click="setFilter('active')">进行中</button>
                <button :class="{ active: filter === 'done' }" @click="setFilter('done')">已完成</button>
            </div>

            <!-- 搜索框：内容绑定 search，实时由 computed filteredTasks 做前端关键词过滤 -->
            <input class="input search" v-model="search" placeholder="搜索任务...">

            <p class="empty" v-if="filteredTasks.length === 0">
                {{ (filter === 'all' && !search) ? '还没有任务，先添加一条吧～' : '没有匹配的任务' }}
            </p>

            <!-- 任务列表：遍历 filteredTasks 渲染 TaskItem 子组件；
                 @remove / @toggle 是子组件向上抛的自定义事件，分别绑定到删除、切换处理函数 -->
            <ul class="list">
                <TaskItem
                    v-for="task in filteredTasks"
                    :key="task.id"
                    :task="task"
                    @remove="removeTask"
                    @toggle="toggleTask"
                />
            </ul>
        </div>
    </div>
</template>

<style scoped>
.app {
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    padding: 28px;
}

.title {
    color: #2e7d32;
    text-align: center;
    font-size: 24px;
    margin: 0 0 24px;
}

.login-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 300px;
    margin: 0 auto;
}

.login-actions {
    display: flex;
    gap: 10px;
}

.login-actions .btn {
    flex: 1;
}

.add-area {
    margin-bottom: 16px;
}

.add-row {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
}

.add-meta {
    display: flex;
    gap: 8px;
}

.add-meta .input {
    flex: 1;
}

.input {
    flex: 1;
    padding: 10px 12px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
    outline: none;
    border-color: #4caf50;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.btn {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s, transform 0.1s;
}

.btn:hover {
    background-color: #43a047;
}

.btn:active {
    transform: scale(0.97);
}

.ghost {
    background-color: white;
    color: #4caf50;
    border: 1px solid #4caf50;
}

.ghost:hover {
    background-color: #e8f5e9;
}

.welcome {
    color: #666;
    margin: 0 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logout {
    padding: 4px 12px;
    font-size: 14px;
    background-color: #f0f0f0;
    color: #555;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.logout:hover {
    background-color: #e0e0e0;
}

.empty {
    color: #aaa;
    text-align: center;
    margin: 20px 0;
}

.filters {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.filters button {
    padding: 6px 16px;
    font-size: 14px;
    background-color: #f0f0f0;
    color: #555;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
}

.filters button:hover {
    background-color: #e0e0e0;
}

.filters button.active {
    background-color: #4caf50;
    color: white;
}

.search {
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 16px;
}

.list {
    list-style: none;
    padding: 0;
    margin: 0;
}
</style>
