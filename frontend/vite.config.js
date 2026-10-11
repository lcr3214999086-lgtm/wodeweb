import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  base: '/static/frontend/',
  build: {
    rollupOptions: {
      input: Object.fromEntries(['index.html', 'products/index.html', 'support/index.html', 'contact/index.html', 'about/index.html'].map(path => [path, fileURLToPath(new URL(path, import.meta.url))])),
    },
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000',
      '/admin': 'http://127.0.0.1:8000',
      '/static/admin': 'http://127.0.0.1:8000',
    },
  },
})
