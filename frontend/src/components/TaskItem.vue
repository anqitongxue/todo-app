<script setup>
// 现在 task 是一个对象：{ id, name, done, created_at }
const props = defineProps({
    task: Object
})

const emit = defineEmits(['remove'])

function handleRemove() {
    emit('remove', props.task.id)   // 把任务的 id 发给父组件（不再用 index）
}
</script>

<template>
    <li>
        <span>{{ task.name }}</span>
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
</style>
