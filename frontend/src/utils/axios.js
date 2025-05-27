import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import router from '../router'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // CORS 관련 설정 추가
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

// 요청 인터셉터
axiosInstance.interceptors.request.use(
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

// 응답 인터셉터
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    // 401 에러가 아니면 바로 에러 반환
    if (error.response?.status !== 401) {
      return Promise.reject(error)
    }

    // 리프레시 토큰 요청에서 실패한 경우 로그아웃
    if (originalRequest.url.includes('/accounts/api/token/refresh/')) {
      const authStore = useAuthStore()
      authStore.clearAuth()
      router.push('/login')
      return Promise.reject(error)
    }

    try {
      const authStore = useAuthStore()
      const newToken = await authStore.refreshToken()
      
      if (!newToken) {
        throw new Error('토큰 갱신 실패')
      }

      // 새 토큰으로 원래 요청 재시도
      originalRequest.headers.Authorization = `Bearer ${newToken}`
      return axiosInstance(originalRequest)
    } catch (refreshError) {
      const authStore = useAuthStore()
      authStore.clearAuth()
      router.push('/login')
      return Promise.reject(refreshError)
    }
  }
)

export default axiosInstance 