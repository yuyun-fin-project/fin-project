import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { getFinanceProducts } from '../services/financeApi'

export const useFinanceStore = defineStore('finance', () => {
  const isLoading = ref(false)
  const error = ref(null)

  // ChatGPT API 설정
  const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY

  // 금융상품 데이터 가져오기
  const fetchProducts = async (type) => {
    isLoading.value = true
    error.value = null

    try {
      const { baseList, optionList } = await getFinanceProducts(type)

      // 기본 정보와 옵션 정보 결합
      const products = baseList.map(item => {
        const options = optionList.filter(opt => opt.fin_prdt_cd === item.fin_prdt_cd)
        const maxRate = options.length > 0
          ? Math.max(...options.map(opt => parseFloat(opt.intr_rate) || 0))
          : parseFloat(item.intr_rate) || 0

        return {
          id: item.fin_prdt_cd,
          name: item.fin_prdt_nm,
          bank_code: item.kor_co_nm,
          bank_name: item.kor_co_nm,
          interest_rate: maxRate,
          period: parseInt(item.save_trm) || 12,
          min_amount: parseInt(item.spcl_cnd) || 0,
          link: item.homp_url || '#'
        }
      })

      return products
    } catch (err) {
      error.value = err.message
      console.error('금융상품 데이터 로딩 실패:', err)
      return []
    } finally {
      isLoading.value = false
    }
  }

  // AI 상품 추천 받기
  const getProductRecommendation = async (product) => {
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
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      })

      return response.data.choices[0].message.content.replace(/\n/g, '<br>')
    } catch (err) {
      console.error('AI 추천 데이터 로딩 실패:', err)
      throw err
    }
  }

  return {
    isLoading,
    error,
    fetchProducts,
    getProductRecommendation
  }
}) 