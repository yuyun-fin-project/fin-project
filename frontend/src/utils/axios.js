import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
})

// 요청 인터셉터
axiosInstance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
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
    const authStore = useAuthStore()

    // 액세스 토큰 만료로 인한 401 에러 && 재시도하지 않은 요청
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // 토큰 갱신 시도
        const newAccessToken = await authStore.refreshToken()
        
        // 새로운 토큰으로 헤더 업데이트
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        
        // 실패했던 요청 재시도
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        // 리프레시 토큰도 만료된 경우
        authStore.logout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default axiosInstance 