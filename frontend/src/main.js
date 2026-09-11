// 本文件是 Vue 应用的入口（启动文件）。
// 作用：创建 Vue 应用实例，并把它挂载（渲染）到页面上的指定 DOM 节点。

// 从 vue 包中导入 createApp 函数。
// createApp 用来创建一个 Vue 应用实例，是 Vue 3 的标准启动方式。
import { createApp } from 'vue'

// 导入全局样式文件。这里不带 from，表示直接执行它（把 CSS 注入页面）。
import './style.css'

// 导入根组件 App.vue。
// App 是整个应用最外层的组件，所有页面内容都由它开始。
import App from './App.vue'

// 创建应用实例，并挂载到页面上 id 为 "app" 的 DOM 元素上。
// createApp(App)：以 App 组件作为根组件创建应用；
// .mount('#app')：把这个应用渲染到 index.html 中 <div id="app"></div> 的位置。
createApp(App).mount('#app')
