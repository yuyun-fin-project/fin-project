import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const BASE_URL = 'http://localhost:8000'

export const api = axios.create({
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

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const authStore = useAuthStore()
        const newToken = await authStore.refreshToken()
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return api(originalRequest)
      } catch (refreshError) {
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export const articleService = {
  // 게시글 목록 조회
  getArticles: async () => {
    try {
      const response = await api.get('/articles/')
      const articles = response.data.results

      // 각 게시글의 작성자 정보 설정
      const articlesWithUsers = articles.map(article => ({
        ...article,
        user: {
          id: article.user_id,
          nickname: article.nickname
        }
      }))

      return {
        count: response.data.count,
        results: articlesWithUsers
      }
    } catch (error) {
      console.error('게시글 목록 조회 실패:', error)
      throw error
    }
  },

  // 게시글 상세 조회
  getArticle: async (articleId) => {
    try {
      const response = await api.get(`/articles/${articleId}/`)
      const article = response.data
      
      return {
        ...article,
        user: {
          id: article.user_id,
          nickname: article.nickname
        }
      }
    } catch (error) {
      console.error('게시글 상세 조회 실패:', error)
      throw error
    }
  },

  // 사용자 정보 가져오기 (더 이상 사용하지 않음)
  async getUserInfo(userId) {
    return {
      id: userId,
      nickname: `사용자${userId}`  // 혹시 모를 경우를 위한 기본값
    }
  },

  // 게시글 생성
  createArticle: async (articleData) => {
    try {
      // FormData 객체 생성
      const formData = new FormData()
      formData.append('title', articleData.title)
      formData.append('content', articleData.content)

      const response = await api.post('/articles/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 생성 실패:', error)
      throw error
    }
  },

  // 게시글 수정
  updateArticle: async (articleId, articleData) => {
    try {
      // FormData 객체 생성
      const formData = new FormData()
      formData.append('title', articleData.title)
      formData.append('content', articleData.content)

      const response = await api.put(`/articles/${articleId}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 수정 실패:', error)
      throw error
    }
  },

  // 게시글 삭제
  deleteArticle: async (articleId) => {
    try {
      await api.delete(`/articles/${articleId}/`)
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
      throw error
    }
  }
} 