import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

// axios 인스턴스 생성
const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true, // CORS 문제 해결을 위해 true로 변경
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

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    // 토큰 만료로 인한 401 에러이고, 재시도하지 않은 요청인 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // 토큰 갱신 시도
        const response = await authService.refreshToken()
        const newToken = response.access
        
        if (!newToken) {
          throw new Error('새로운 액세스 토큰을 받지 못했습니다.')
        }
        
        // 새 토큰 저장
        localStorage.setItem('access_token', newToken)
        
        // 원래 요청의 헤더 업데이트
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        
        // 원래 요청 재시도
        return api(originalRequest)
      } catch (refreshError) {
        // 토큰 갱신 실패 시 로그아웃 처리
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_id')
        document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export const authService = {
  // 사용자 정보 가져오기
  getUserInfo: async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('토큰이 없습니다.')
      }
      
      // JWT 토큰에서 user_id 추출
      const payload = JSON.parse(atob(token.split('.')[1]))
      const userId = payload.user_id
      
      if (!userId) {
        throw new Error('토큰에서 사용자 ID를 찾을 수 없습니다.')
      }
      
      const response = await api.get(`/accounts/profile/${userId}/`)
      return response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      throw error
    }
  },

  // 액세스 토큰 갱신
  refreshToken: async () => {
    try {
      const response = await api.post('/accounts/api/token/refresh/')
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
      return response.data
    } catch (error) {
      console.error('소셜 로그인 실패:', error)
      throw error
    }
  },

  // 로그아웃
  logout: async () => {
    try {
      const refreshToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('refresh_token='))
        ?.split('=')[1]

      if (refreshToken) {
        await api.post('/accounts/logout/', { refresh_token: refreshToken })
      }

      // 로컬 스토리지와 쿠키 모두 정리
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_id')
      document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      
      return { success: true }
    } catch (error) {
      console.error('로그아웃 실패:', error)
      // 에러가 발생하더라도 로컬 스토리지와 쿠키는 정리
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_id')
      document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      throw error
    }
  }
} 