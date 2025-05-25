import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
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

export const accountService = {
  // 프로필 정보 가져오기
  getProfile: async () => {
    try {
      const response = await api.get('/accounts/profile/')
      return response.data
    } catch (error) {
      console.error('프로필 정보 조회 실패:', error)
      throw error
    }
  },

  // 프로필 수정
  updateProfile: async (profileData) => {
    try {
      const formData = new FormData()
      
      // 기본 정보 추가
      if (profileData.nickname) formData.append('nickname', profileData.nickname)
      if (profileData.email) formData.append('email', profileData.email)
      if (profileData.introduction) formData.append('introduction', profileData.introduction)
      
      // 프로필 이미지가 있는 경우 추가
      if (profileData.profile_image && profileData.profile_image instanceof File) {
        formData.append('profile_image', profileData.profile_image)
      }

      const response = await api.patch('/accounts/profile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('프로필 수정 실패:', error)
      throw error
    }
  },

  // 비밀번호 변경
  changePassword: async (passwordData) => {
    try {
      const response = await api.post('/accounts/password/change/', {
        old_password: passwordData.oldPassword,
        new_password1: passwordData.newPassword,
        new_password2: passwordData.confirmPassword
      })
      return response.data
    } catch (error) {
      console.error('비밀번호 변경 실패:', error)
      throw error
    }
  }
} 