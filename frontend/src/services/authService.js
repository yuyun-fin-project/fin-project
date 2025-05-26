import axios from '../utils/axios'
import { jwtDecode } from 'jwt-decode'

const BASE_URL = 'http://localhost:8000'

// axios 인스턴스 생성
const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // 리프레시 토큰 요청에서 실패한 경우 로그아웃
    if (originalRequest.url.includes('/accounts/api/token/refresh/')) {
      authService.logout()
      return Promise.reject(error)
    }

    // 토큰 만료로 인한 401 에러이고, 재시도하지 않은 요청인 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        try {
          const token = await new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        } catch (err) {
          return Promise.reject(err)
        }
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refreshResponse = await axios.post('/accounts/api/token/refresh/', {}, {
          baseURL: BASE_URL,
          withCredentials: true
        })

        const newToken = refreshResponse.data.access
        if (newToken) {
          localStorage.setItem('access_token', newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          processQueue(null, newToken)
          return api(originalRequest)
        }
      } catch (refreshError) {
        processQueue(refreshError, null)
        authService.logout()
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }
    
    return Promise.reject(error)
  }
)

const authService = {
  // 사용자 정보 가져오기
  getUserInfo: async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('토큰이 없습니다.')
      }
      
      const decoded = jwtDecode(token)
      const userId = decoded.user_id
      
      if (!userId) {
        throw new Error('토큰에서 사용자 ID를 찾을 수 없습니다.')
      }
      
      const response = await axios.get(`/accounts/profile/${userId}/`)
      return response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      throw error
    }
  },

  // 액세스 토큰 갱신
  refreshToken: async () => {
    try {
      const cookies = document.cookie.split(';')
      const refreshToken = cookies.find(cookie => cookie.trim().startsWith('refresh_token='))
      
      if (!refreshToken) {
        throw new Error('리프레시 토큰이 없습니다.')
      }

      const response = await axios.post('/accounts/api/token/refresh/', {}, {
        withCredentials: true,
        headers: {
          'X-CSRFTOKEN': document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1")
        }
      })

      if (!response.data.access) {
        throw new Error('새로운 액세스 토큰을 받지 못했습니다.')
      }

      return response.data
    } catch (error) {
      console.error('토큰 갱신 실패:', error)
      throw error
    }
  },

  // 소셜 로그인 콜백 처리
  handleSocialLogin: async (provider, code) => {
    try {
      const response = await api.post(`/accounts/${provider}/callback/`, { code })
      
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access)
      }
      
      return response.data
    } catch (error) {
      console.error('소셜 로그인 실패:', error)
      throw error
    }
  },

  // 로그아웃
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_id')
    document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=localhost;'
    window.location.href = '/login'
  },

  // 토큰 유효성 검사
  isTokenValid: (token) => {
    if (!token) return false
    
    try {
      const decoded = jwtDecode(token)
      const currentTime = Date.now() / 1000
      return decoded.exp > currentTime
    } catch {
      return false
    }
  }
}

export default authService 