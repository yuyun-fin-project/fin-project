import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'
import { loadEnv } from 'vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    server: {
      port: 5173,
      host: true,
      hmr: {
        overlay: false
      },
      proxy: {
        '/api/finlife': {
          target: 'http://finlife.fss.or.kr/finlifeapi',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api\/finlife/, ''),
          configure: (proxy, options) => {
            proxy.on('proxyReq', (proxyReq, req, res) => {
              proxyReq.setHeader('Origin', 'http://finlife.fss.or.kr');
              proxyReq.setHeader('Referer', 'http://finlife.fss.or.kr/');
              proxyReq.setHeader('Accept', 'application/json');
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
        },
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
        '/finrecom': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/finrecom/, '/finrecom'),
          configure: (proxy, options) => {
            proxy.on('error', (err, req, res) => {
              console.error('프록시 에러:', err);
            });
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.log('프록시 요청:', req.method, req.url);
            });
            proxy.on('proxyRes', (proxyRes, req, res) => {
              console.log('프록시 응답:', proxyRes.statusCode);
            });
          }
        }
      }
    },
    build: {
      sourcemap: true,
      chunkSizeWarningLimit: 1000
    },
    define: {
      __VITE_KAKAO_MAP_API_KEY__: JSON.stringify(env.VITE_KAKAO_MAP_API_KEY)
    }
    // 빌드 실패로 인해 주석 처리
    // define: {
    //   '%VITE_KAKAO_MAP_API_KEY%': JSON.stringify(env.VITE_KAKAO_MAP_API_KEY)
    // }
  }
}) 
