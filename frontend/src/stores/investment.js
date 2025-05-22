import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useInvestmentStore = defineStore('investment', () => {
  const isLoading = ref(true)
  const isInitialized = ref(false)
  const userProfile = ref({
    riskLevel: '안정 추구형',
    period: '3년 이상',
    monthlyInvestment: '100만원'
  })

  const portfolio = ref([
    {
      name: '국내 채권형 ETF',
      description: '안정적인 이자 수익 추구',
      percentage: 40
    },
    {
      name: '글로벌 주식형 ETF',
      description: '장기 성장 잠재력',
      percentage: 30
    },
    {
      name: '금/원자재 ETF',
      description: '인플레이션 대비',
      percentage: 20
    },
    {
      name: '단기 자금',
      description: '유동성 확보',
      percentage: 10
    }
  ])

  const isDataReady = computed(() => !isLoading.value && isInitialized.value)

  const loadData = async () => {
    if (isInitialized.value) {
      isLoading.value = false
      return
    }

    isLoading.value = true
    try {
      // 실제 API 호출이 있다면 여기서 수행
      await new Promise(resolve => setTimeout(resolve, 300))
      isInitialized.value = true
    } catch (error) {
      console.error('데이터 로딩 실패:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    isInitialized,
    isDataReady,
    userProfile,
    portfolio,
    loadData
  }
}, {
  persist: {
    key: 'investment-store',
    paths: ['userProfile', 'portfolio', 'isInitialized']
  }
}) 