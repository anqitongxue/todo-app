<script setup>
import { ref, onMounted } from 'vue'
import TaskItem from './components/TaskItem.vue'

const API = 'http://localhost:5000'   // 后端的地址

const newTask = ref('')
const tasks = ref([])

// 从后端拉取任务列表
async function loadTasks() {
    const res = await fetch(`${API}/tasks`)   // 发 GET 请求
    tasks.value = await res.json()            // 把返回的 JSON 转成 JS 对象
}

// 页面加载完成后，执行一次 loadTasks
onMounted(loadTasks)

// 添加任务：调后端的 POST 接口
async function addTask() {
    const name = newTask.value
    if (name === '') return

    await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),   // JS 对象 → JSON 字符串
    })
    newTask.value = ''
    loadTasks()   // 加完重新拉一次列表
}

// 删除任务：调后端的 DELETE 接口
async function removeTask(id) {
    await fetch(`${API}/tasks/${id}`, { method: 'DELETE' })
    loadTasks()   // 删完重新拉一次列表
}
</script>

<template>
    <h1 class="title">我的任务清单</h1>

    <div class="add-row">
        <input class="input" v-model="newTask" placeholder="输入一个新任务...">
        <button class="btn" @click="addTask">添加</button>
    </div>

    <p class="empty" v-if="tasks.length === 0">还没有任务，先添加一条吧～</p>

    <ul class="list">
        <TaskItem
            v-for="task in tasks"
            :key="task.id"
            :task="task"
            @remove="removeTask"
        />
    </ul>
</template>

<style scoped>
.title {
    color: #333;
    text-align: center;
    margin-bottom: 24px;
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

.btn {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
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
