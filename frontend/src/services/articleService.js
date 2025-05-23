import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

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

export const articleService = {
  // 사용자 정보 가져오기
  async getUserInfo(userId) {
    try {
      const response = await api.get(`/accounts/profile/${userId}/`)
      return response.data
    } catch (error) {
      console.error('사용자 정보 조회 실패:', error)
      return null
    }
  },

  // 게시글 목록 조회
  getArticles: async () => {
    try {
      const response = await api.get('/articles/')
      const articles = response.data.results

      // 각 게시글의 작성자 정보 가져오기
      const articlesWithUsers = await Promise.all(
        articles.map(async (article) => {
          const user = await articleService.getUserInfo(article.user_id)
          return {
            ...article,
            user
          }
        })
      )

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
      
      // 작성자 정보 가져오기
      const user = await articleService.getUserInfo(article.user_id)
      return {
        ...article,
        user
      }
    } catch (error) {
      console.error('게시글 상세 조회 실패:', error)
      throw error
    }
  },

  // 게시글 생성
  createArticle: async (articleData) => {
    try {
      // URLSearchParams를 사용하여 form-data 형식으로 전송
      const params = new URLSearchParams()
      params.append('title', articleData.title)
      params.append('content', articleData.content)
      
      const response = await api.post('/articles/', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
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
      // URLSearchParams를 사용하여 form-data 형식으로 전송
      const params = new URLSearchParams()
      params.append('title', articleData.title)
      params.append('content', articleData.content)
      
      const response = await api.put(`/articles/${articleId}/`, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
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