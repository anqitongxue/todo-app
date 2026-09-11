<script setup>
import { ref, onMounted } from 'vue'
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
const tasks = ref([])

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

// 拉取任务列表
async function loadTasks() {
    const res = await fetch(`${API}/tasks`, { credentials: 'include' })
    tasks.value = await res.json()
}

// 添加任务
async function addTask() {
    const name = newTask.value
    if (name === '') return
    await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name, category: newCategory.value }),
    })
    newTask.value = ''
    newCategory.value = ''
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

        <div class="add-row">
            <input class="input" v-model="newTask" placeholder="输入一个新任务...">
            <input class="input category" v-model="newCategory" placeholder="分类（如：工作）">
            <button class="btn" @click="addTask">添加</button>
        </div>

        <p class="empty" v-if="tasks.length === 0">还没有任务，先添加一条吧～</p>

        <ul class="list">
            <TaskItem
                v-for="task in tasks"
                :key="task.id"
                :task="task"
                @remove="removeTask"
                @toggle="toggleTask"
            />
        </ul>
    </div>
</template>

<style scoped>
.title {
    color: #333;
    text-align: center;
    margin-bottom: 24px;
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

.add-row {
    display: flex;
    gap: 10px;
}

.input {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 6px;
}

.category {
    flex: 0 0 140px;
    max-width: 140px;
}

.btn {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

.ghost {
    background-color: white;
    color: #4caf50;
    border: 1px solid #4caf50;
}

.welcome {
    color: #666;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logout {
    padding: 4px 12px;
    font-size: 14px;
    background-color: #eee;
    color: #555;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.empty {
    color: #999;
    margin: 12px 0;
}

.list {
    list-style: none;
    padding: 0;
}
</style>
