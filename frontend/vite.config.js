import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'
import { loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
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
        '/dapi.kakao.com': {
          target: 'https://dapi.kakao.com',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/dapi\.kakao\.com/, '')
        }
      }
    },
    build: {
      sourcemap: true,
      chunkSizeWarningLimit: 1000
    },
    define: {
      '%VITE_KAKAO_MAP_API_KEY%': JSON.stringify(env.VITE_KAKAO_MAP_API_KEY)
    }
  }
}) 
