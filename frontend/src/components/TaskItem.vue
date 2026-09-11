<script setup>
// task 是一个对象：{ id, name, done, created_at, category }
const props = defineProps({
    task: Object
})

const emit = defineEmits(['remove', 'toggle'])

function handleRemove() {
    emit('remove', props.task.id)   // 把任务的 id 发给父组件
}

function handleToggle() {
    emit('toggle', props.task.id, !props.task.done)   // 把"新的完成状态"发给父组件
}
</script>

<template>
    <li :class="{ done: task.done }">
        <div class="info">
            <input type="checkbox" :checked="task.done" @change="handleToggle">
            <span class="name">{{ task.name }}</span>
            <span class="cat" v-if="task.category">{{ task.category }}</span>
            <span class="due" v-if="task.due_date">📅 {{ task.due_date }}</span>
        </div>
        <button class="del" @click="handleRemove">删除</button>
    </li>
</template>

<style scoped>
li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 14px;
    margin-bottom: 8px;
    background-color: white;
    border-radius: 6px;
    font-size: 18px;
}

.del {
    padding: 4px 10px;
    font-size: 14px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.info {
    display: flex;
    align-items: center;
    gap: 8px;
}

.cat {
    font-size: 12px;
    color: #4caf50;
    background-color: #e8f5e9;
    padding: 2px 8px;
    border-radius: 10px;
}

.due {
    font-size: 12px;
    color: #f57c00;
    background-color: #fff3e0;
    padding: 2px 8px;
    border-radius: 10px;
}

input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    flex-shrink: 0;
}

li.done .name {
    color: #999;
    text-decoration: line-through;
}

li.done {
    opacity: 0.75;
}
</style>
