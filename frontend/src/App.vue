<script setup>
import { ref } from 'vue'
import TaskItem from './components/TaskItem.vue'

const newTask = ref('')
const tasks = ref([])

function addTask() {
    const text = newTask.value
    if (text === '') {
        return
    }
    tasks.value.push(text)
    newTask.value = ''
}

function removeTask(index) {
    tasks.value.splice(index, 1)
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
            v-for="(task, index) in tasks"
            :key="index"
            :task="task"
            :index="index"
            @remove="removeTask"
        />
    </ul>
</template>

<style scoped>
/* scoped：这些样式只作用于本组件的模板，不会影响别的组件 */

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
