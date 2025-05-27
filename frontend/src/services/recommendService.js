import axios from 'axios'

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

export const recommendService = {
  // 금융 상품 추천 받기
  getRecommendations: async (productType = 'D') => {
    try {
      const response = await api.get('/finance/recommend/', {
        params: {
          product_type: productType
        }
      })
      return response.data
    } catch (error) {
      console.error('추천 상품 조회 실패:', error)
      throw error
    }
  }
} 