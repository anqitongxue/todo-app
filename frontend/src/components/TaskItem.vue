<script setup>
const props = defineProps({
    task: String,
    index: Number
})

const emit = defineEmits(['remove'])

function handleRemove() {
    emit('remove', props.index)
}
</script>

<template>
    <li>
        <span>{{ task }}</span>
        <button class="del" @click="handleRemove">删除</button>
    </li>
</template>

<style scoped>
/* 这个组件的样式：只管"一条任务"长什么样 */
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
