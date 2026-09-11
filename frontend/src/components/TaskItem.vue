<script setup>
// ============================================================
// 单条任务组件：负责渲染一条任务，并处理「勾选完成」和「删除」两个交互。
// 组件本身不修改数据，而是通过 emit 把用户的操作通知给父组件去处理。
// ============================================================

// 定义组件对外接收的属性（props）。
// task 是一个对象，父组件会传入一条任务的完整数据，
// 结构大致为：{ id, name, done, created_at, category, due_date }
const props = defineProps({
    task: Object
})

// 定义组件对外触发的事件（emit）：
// 'remove' —— 用户点击删除按钮时触发；
// 'toggle' —— 用户勾选/取消勾选复选框时触发。
const emit = defineEmits(['remove', 'toggle'])

// 删除按钮的点击处理函数。
// 做什么：把「删除」意图通知父组件。
// 参数：无（事件对象用不到）。
// 返回值：无。
function handleRemove() {
    emit('remove', props.task.id)   // 把任务的 id 发给父组件
}

// 复选框状态变化的处理函数。
// 做什么：把「新的完成状态」通知父组件，由父组件决定如何保存。
// 参数：无。
// 返回值：无。
function handleToggle() {
    emit('toggle', props.task.id, !props.task.done)   // 把"新的完成状态"发给父组件
}
</script>

<template>
    <!-- 整条任务；:class 动态绑定：当 task.done 为 true 时，给 li 加上 done 类，用于显示"已完成"样式 -->
    <li :class="{ done: task.done }">
        <!-- 左侧信息区：复选框 + 任务名 + 分类 + 截止时间 -->
        <div class="info">
            <!-- 复选框：显示当前完成状态；用户点击改变状态时触发 handleToggle -->
            <input type="checkbox" :checked="task.done" @change="handleToggle">
            <!-- 任务名称 -->
            <span class="name">{{ task.name }}</span>
            <!-- 分类标签：只有存在 category 时才渲染 -->
            <span class="cat" v-if="task.category">{{ task.category }}</span>
            <!-- 截止时间标签：只有存在 due_date 时才渲染 -->
            <span class="due" v-if="task.due_date">📅 {{ task.due_date }}</span>
        </div>
        <!-- 删除按钮：点击后触发 handleRemove -->
        <button class="del" @click="handleRemove">删除</button>
    </li>
</template>

<style scoped>
/* scoped 表示这些样式只作用于当前组件，不会影响其它组件 */

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

/* 任务名超长时显示省略号：先隐藏溢出，再用省略号代替被截断的部分 */
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

/* 已完成任务：任务名变灰并加删除线 */
li.done .name {
    color: #999;
    text-decoration: line-through;
}

/* 已完成任务：整条稍微变淡，突出视觉上的"已完成" */
li.done {
    opacity: 0.75;
}
</style>
