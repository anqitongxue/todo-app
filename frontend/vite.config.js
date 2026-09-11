import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 开发时把后端接口转发到 Flask（前端就能用相对路径 /tasks 等）
      '/tasks': 'http://localhost:5000',
      '/login': 'http://localhost:5000',
      '/register': 'http://localhost:5000',
      '/me': 'http://localhost:5000',
      '/logout': 'http://localhost:5000',
    },
  },
})
