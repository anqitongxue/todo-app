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
    padding: 12px 14px;
    margin-bottom: 8px;
    background-color: #fafafa;
    border: 1px solid #f0f0f0;
    border-radius: 10px;
    font-size: 16px;
    transition: box-shadow 0.2s, transform 0.1s;
}

li:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transform: translateY(-1px);
}

.del {
    padding: 4px 10px;
    font-size: 13px;
    background-color: #fdecea;
    color: #e74c3c;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
}

.del:hover {
    background-color: #e74c3c;
    color: white;
}

.info {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
}

.name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cat {
    font-size: 12px;
    color: #4caf50;
    background-color: #e8f5e9;
    padding: 2px 8px;
    border-radius: 10px;
    flex-shrink: 0;
}

.due {
    font-size: 12px;
    color: #f57c00;
    background-color: #fff3e0;
    padding: 2px 8px;
    border-radius: 10px;
    flex-shrink: 0;
}

input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    flex-shrink: 0;
    accent-color: #4caf50;
}

li.done .name {
    color: #999;
    text-decoration: line-through;
}

li.done {
    opacity: 0.75;
}
</style>
