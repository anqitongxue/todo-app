// =====================================================================
// Vite 配置文件（构建工具 Vite 的配置文件，文件名固定为 vite.config.js）
// 职责：告诉 Vite 如何构建项目、如何在开发环境下运行，以及如何处理接口请求。
// 核心作用之一：开发环境下把前端发往 /tasks、/login 等路径的请求
// 「代理（proxy）」到后端 Flask 服务，从而解决跨域问题。
// =====================================================================

// 引入 Vue 插件：让 Vite 能够识别并编译 .vue 单文件组件（模板 + 脚本 + 样式）
import vue from '@vitejs/plugin-vue'
// 引入 defineConfig 辅助函数：用于书写配置时获得类型提示和校验（本身不做任何逻辑）
import { defineConfig } from 'vite'

// https://vite.dev/config/
// defineConfig(...) 返回一个「配置对象」交给 Vite 使用，export default 把它导出。
export default defineConfig({
  // plugins：Vite 用到的插件列表，这里启用 Vue 插件
  plugins: [vue()],
  // server：开发服务器（npm run dev 启动的那个）的相关配置
  server: {
    // proxy：代理规则。前端开发服务器收到匹配的请求时，会「转交」给下面的目标地址。
    // 好处：前端代码里只需写相对路径（如 /tasks），不用关心后端真实地址，也绕开了浏览器的跨域限制。
    proxy: {
      // 开发时把后端接口转发到 Flask（前端就能用相对路径 /tasks 等）
      // 规则：凡是路径以 /tasks 开头的请求，都转发到 http://localhost:5000（后端服务）
      '/tasks': 'http://localhost:5000',
      // 登录接口：以 /login 开头的请求转发到后端
      '/login': 'http://localhost:5000',
      // 注册接口：以 /register 开头的请求转发到后端
      '/register': 'http://localhost:5000',
      // 获取当前登录用户信息的接口：以 /me 开头的请求转发到后端
      '/me': 'http://localhost:5000',
      // 退出登录接口：以 /logout 开头的请求转发到后端
      '/logout': 'http://localhost:5000',
    },
  },
})
