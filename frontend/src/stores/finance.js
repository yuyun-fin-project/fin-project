import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { getFinanceProducts } from '../services/financeApi'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    products: [],
    loading: false,
    error: null,
    currentType: 'deposit'
  }),

  getters: {
    getProducts: (state) => state.products,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null
  },

  actions: {
    async fetchProducts() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/financial-products/')
        this.products = response.data
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch products:', error)
      } finally {
        this.loading = false
      }
    },

    async searchProducts(searchTerm = '') {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`/api/financial-products/search/?q=${encodeURIComponent(searchTerm)}`)
        this.products = response.data
      } catch (error) {
        this.error = error.message
        console.error('Failed to search products:', error)
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    },

    // ChatGPT API 설정
    OPENAI_API_KEY() {
      return import.meta.env.VITE_OPENAI_API_KEY
    },

    // 금융상품 데이터 가져오기
    async fetchProductsByType(type = 'deposit') {
      this.loading = true
      this.error = null
      this.currentType = type

      try {
        const { baseList, optionList } = await getFinanceProducts(type)

        // 기본 정보와 옵션 정보 결합
        this.products = baseList.map(item => {
          const productOptions = optionList.filter(opt => opt.id === item.id)
          
          // 최고 금리 계산
          const maxRate = productOptions.length > 0
            ? Math.max(...productOptions.map(opt => {
                const baseRate = opt.intr_rate
                const specialRate = opt.intr_rate2
                return Math.max(baseRate, specialRate)
              }))
            : 0

          // 가입기간 추출
          let period = 12
          if (productOptions.length > 0) {
            const uniquePeriods = [...new Set(productOptions.map(opt => opt.save_trm))]
            period = Math.min(...uniquePeriods)
          }

          // 최소 가입금액 추출
          let minAmount = 0
          if (item.etc_note) {
            const matches = item.etc_note.match(/최소[가입금액|예치금액]?\s*:\s*(\d+)[만]?원/i)
            if (matches) {
              minAmount = parseInt(matches[1]) * (matches[0].includes('만원') ? 10000 : 1)
            }
          }

          return {
            id: item.id,
            name: item.name,
            bank_code: item.bank_code,
            bank_name: item.bank_name,
            type: item.type,
            interest_rate: maxRate,
            period: period,
            min_amount: minAmount,
            join_way: item.join_way,
            etc_note: item.etc_note,
            join_member: item.join_member,
            options: productOptions
          }
        })

        return this.products
      } catch (err) {
        this.error = err.message
        console.error('금융상품 데이터 로딩 실패:', err)
        return []
      } finally {
        this.loading = false
      }
    },

    // 검색 및 필터링
    searchProducts(term = '', filters = {}) {
      if (!Array.isArray(this.products)) return []

      return this.products.filter(product => {
        // 검색어 필터링
        const searchMatch = !term || 
          product.name.toLowerCase().includes(term.toLowerCase()) ||
          product.bank_name.toLowerCase().includes(term.toLowerCase())

        // 은행 필터링
        const bankMatch = !filters.bank || 
          product.bank_code === filters.bank

        // 가입기간 필터링
        const periodMatch = !filters.period || 
          product.period === parseInt(filters.period)

        // 최소금액 필터링
        const minAmountMatch = !filters.minAmount || 
          product.min_amount >= filters.minAmount

        // 최대금액 필터링
        const maxAmountMatch = !filters.maxAmount || 
          product.min_amount <= filters.maxAmount

        return searchMatch && bankMatch && periodMatch && 
               minAmountMatch && maxAmountMatch
      })
    },

    // AI 상품 추천 받기
    async getProductRecommendation(product) {
      try {
        const prompt = `
다음 금융 상품에 대해 전문가의 관점에서 분석해주세요:

상품명: ${product.name}
은행: ${product.bank_name}
금리: ${product.interest_rate}%
가입기간: ${product.period}개월
최소가입금액: ${product.min_amount}원

다음 항목들을 포함해서 분석해주세요:
1. 상품의 주요 특징
2. 현재 시장 상황에서의 금리 경쟁력
3. 누구에게 적합한 상품인지
4. 가입 시 고려해야 할 사항
5. 리스크 요소
`

        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: '당신은 금융상품 분석 전문가입니다. 일반 소비자가 이해하기 쉽게 설명해주세요.'
            },
            {
              role: 'user',
              content: prompt
            }
          ]
        }, {
          headers: {
            'Authorization': `Bearer ${this.OPENAI_API_KEY}`,
            'Content-Type': 'application/json'
          }
        })

        return response.data.choices[0].message.content.replace(/\n/g, '<br>')
      } catch (err) {
        console.error('AI 추천 데이터 로딩 실패:', err)
        throw err
      }
    }
  }
}) 