import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiBase = env.VITE_API_BASE_URL || 'http://localhost:8012'

  return {
    plugins: [vue()],
    resolve: {
      alias: { '@': resolve(__dirname, 'src') },
    },
    server: {
      host: '0.0.0.0',
      port: 5174,
      proxy: {
        '/api': { target: apiBase, changeOrigin: true },
        '/media': { target: apiBase, changeOrigin: true },
      },
    },
  }
})
