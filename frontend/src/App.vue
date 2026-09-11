<script setup>
import { ref, onMounted, computed } from 'vue'
import TaskItem from './components/TaskItem.vue'

const API = 'http://localhost:5000'

// 登录相关状态
const username = ref('')
const password = ref('')
const loggedIn = ref(false)
const currentUser = ref('')

// 任务相关状态
const newTask = ref('')
const newCategory = ref('')
const newDueDate = ref('')
const tasks = ref([])
const filter = ref('all')   // 筛选状态：'all'（全部）| 'active'（进行中）| 'done'（已完成）
const search = ref('')      // 搜索关键词

// 计算属性：只做"关键词搜索"（状态筛选已交给后端，这里不再筛状态）
const filteredTasks = computed(() => {
    const kw = search.value.trim().toLowerCase()
    if (!kw) return tasks.value
    return tasks.value.filter(t => t.name.toLowerCase().includes(kw))
})

// 页面加载时：检查是否已登录
async function checkLogin() {
    const res = await fetch(`${API}/me`, { credentials: 'include' })
    if (res.ok) {
        const data = await res.json()
        currentUser.value = data.username
        loggedIn.value = true
        loadTasks()
    }
}

// 登录
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

// 注册（成功后直接登录）
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

// 退出
async function logout() {
    await fetch(`${API}/logout`, { method: 'POST', credentials: 'include' })
    loggedIn.value = false
    currentUser.value = ''
    tasks.value = []
}

// 拉取任务列表（把状态 filter 作为查询参数传给后端，让后端筛）
async function loadTasks() {
    let url = `${API}/tasks`
    if (filter.value !== 'all') {
        url += `?status=${filter.value}`
    }
    const res = await fetch(url, { credentials: 'include' })
    tasks.value = await res.json()
}

// 切换筛选：改 filter 状态，并重新从后端拉取
function setFilter(f) {
    filter.value = f
    loadTasks()
}

// 添加任务
async function addTask() {
    const name = newTask.value
    if (name === '') return
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

// 删除任务
async function removeTask(id) {
    await fetch(`${API}/tasks/${id}`, { method: 'DELETE', credentials: 'include' })
    loadTasks()
}

// 切换完成状态
async function toggleTask(id, done) {
    const task = tasks.value.find(t => t.id === id)
    if (!task) return
    await fetch(`${API}/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name: task.name, done }),   // name 要原样带上，否则会被清空
    })
    loadTasks()
}

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

            <div class="filters">
                <button :class="{ active: filter === 'all' }" @click="setFilter('all')">全部</button>
                <button :class="{ active: filter === 'active' }" @click="setFilter('active')">进行中</button>
                <button :class="{ active: filter === 'done' }" @click="setFilter('done')">已完成</button>
            </div>

            <input class="input search" v-model="search" placeholder="搜索任务...">

            <p class="empty" v-if="filteredTasks.length === 0">
                {{ (filter === 'all' && !search) ? '还没有任务，先添加一条吧～' : '没有匹配的任务' }}
            </p>

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
