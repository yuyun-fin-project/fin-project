import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    host: true,
    hmr: {
      overlay: false
    },
    proxy: {
      '/api/finlifeapi': {
        target: 'https://finlife.fss.or.kr',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/finlifeapi/, '/finlifeapi'),
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            proxyReq.setHeader('Origin', 'https://finlife.fss.or.kr');
            proxyReq.setHeader('Referer', 'https://finlife.fss.or.kr/');
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            proxyRes.headers['Access-Control-Allow-Origin'] = '*';
            proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS';
            proxyRes.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
          });
        }
      },
      '/finlifeapi': {
        target: 'http://finlife.fss.or.kr',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/finlifeapi/, '')
      }
    }
  },
  build: {
    sourcemap: true,
    chunkSizeWarningLimit: 1000
  }
}) 