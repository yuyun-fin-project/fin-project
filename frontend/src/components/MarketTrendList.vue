<template>
  <div class="market-trend-list">
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="error" class="text-red-500 p-4 text-center">
      {{ error }}
    </div>

    <div v-else class="divide-y divide-gray-100">
      <!-- 주요 지수 -->
      <div class="p-4">
        <h4 class="font-medium text-gray-900 mb-3">주요 지수</h4>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="(index, key) in marketIndices" :key="key" class="bg-gray-50 p-3 rounded-lg">
            <div class="text-sm text-gray-600 mb-1">{{ index.name }}</div>
            <div class="font-semibold">{{ formatNumber(index.value) }}</div>
            <div :class="[
              'text-xs',
              index.change >= 0 ? 'text-red-500' : 'text-blue-500'
            ]">
              {{ formatChange(index.change) }}%
            </div>
          </div>
        </div>
      </div>

      <!-- 환율 정보 -->
      <div class="p-4">
        <h4 class="font-medium text-gray-900 mb-3">환율 정보</h4>
        <div class="space-y-2">
          <div v-for="(rate, key) in exchangeRates" :key="key" 
            class="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
            <div>
              <div class="text-sm text-gray-600">{{ rate.name }}</div>
              <div class="font-semibold">{{ formatNumber(rate.value, 2) }}</div>
            </div>
            <div :class="[
              'text-sm',
              rate.change >= 0 ? 'text-red-500' : 'text-blue-500'
            ]">
              {{ formatChange(rate.change, 2) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 금리 정보 -->
      <div class="p-4">
        <h4 class="font-medium text-gray-900 mb-3">금리 정보</h4>
        <div class="space-y-2">
          <div v-for="(rate, key) in interestRates" :key="key"
            class="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
            <div>
              <div class="text-sm text-gray-600">{{ rate.name }}</div>
              <div class="font-semibold">{{ formatNumber(rate.value, 2) }}%</div>
            </div>
            <div :class="[
              'text-sm',
              rate.change >= 0 ? 'text-red-500' : 'text-blue-500'
            ]">
              {{ formatChange(rate.change, 2) }}%p
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error && !hasData" class="text-center py-8 text-gray-500">
      시장 동향 정보를 불러올 수 없습니다.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const loading = ref(true)
const error = ref(null)

// 시장 데이터
const marketIndices = ref({
  kospi: { name: 'KOSPI', value: 0, change: 0 },
  kosdaq: { name: 'KOSDAQ', value: 0, change: 0 }
})

const exchangeRates = ref({
  usd: { name: 'USD/KRW', value: 0, change: 0 },
  jpy: { name: 'JPY/KRW', value: 0, change: 0 }
})

const interestRates = ref({
  base: { name: '기준금리', value: 3.50, change: 0 },
  cd: { name: 'CD(91일)', value: 0, change: 0 }
})

const hasData = computed(() => {
  return Object.values(marketIndices.value).some(index => index.value !== 0) ||
         Object.values(exchangeRates.value).some(rate => rate.value !== 0) ||
         Object.values(interestRates.value).some(rate => rate.value !== 0)
})

const fetchMarketData = async () => {
  loading.value = true
  error.value = null

  try {
    // 프록시 URL (CORS 우회)
    const proxyUrl = 'https://api.allorigins.win/raw?url='
    
    // KOSPI & KOSDAQ 데이터
    const stockUrl = encodeURIComponent('https://m.stock.naver.com/api/stocks/marketValue/KOSPI,KOSDAQ')
    const stockResponse = await axios.get(`${proxyUrl}${stockUrl}`)
    
    if (stockResponse.data) {
      const [kospiData, kosdaqData] = stockResponse.data
      // KOSPI
      marketIndices.value.kospi.value = parseFloat(kospiData.closePrice)
      marketIndices.value.kospi.change = parseFloat(kospiData.fluctuationsRatio)

      // KOSDAQ
      marketIndices.value.kosdaq.value = parseFloat(kosdaqData.closePrice)
      marketIndices.value.kosdaq.change = parseFloat(kosdaqData.fluctuationsRatio)
    }

    // 환율 데이터
    const exchangeUrl = encodeURIComponent('https://m.stock.naver.com/api/exchanges/marketValue')
    const exchangeResponse = await axios.get(`${proxyUrl}${exchangeUrl}`)
    
    if (exchangeResponse.data?.marketValues) {
      // USD/KRW
      const usdData = exchangeResponse.data.marketValues.find(item => item.name === 'USD/KRW')
      if (usdData) {
        exchangeRates.value.usd.value = parseFloat(usdData.closePrice)
        exchangeRates.value.usd.change = parseFloat(usdData.fluctuationsRatio)
      }

      // JPY/KRW
      const jpyData = exchangeResponse.data.marketValues.find(item => item.name === 'JPY/KRW')
      if (jpyData) {
        exchangeRates.value.jpy.value = parseFloat(jpyData.closePrice)
        exchangeRates.value.jpy.change = parseFloat(jpyData.fluctuationsRatio)
      }
    }

    // 금리 정보 (고정 데이터 사용)
    interestRates.value.base = { 
      name: '기준금리', 
      value: 3.50, 
      change: 0 
    }
    
    interestRates.value.cd = { 
      name: 'CD(91일)', 
      value: 3.46, 
      change: -0.02 
    }

  } catch (err) {
    console.error('시장 데이터 조회 실패:', err)
    error.value = '시장 동향을 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 숫자 포맷팅 함수 수정
const formatNumber = (value: number, decimals: number = 2) => {
  if (typeof value !== 'number' || isNaN(value)) {
    return '0.00'
  }
  
  if (Math.abs(value) >= 100) {
    decimals = 0  // 100 이상인 경우 소수점 없이 표시
  }
  return new Intl.NumberFormat('ko-KR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value)
}

// 변화량 포맷팅 함수 수정
const formatChange = (value: number, decimals: number = 2) => {
  if (typeof value !== 'number' || isNaN(value)) {
    return '+0.00'
  }
  
  const prefix = value >= 0 ? '+' : ''
  return prefix + formatNumber(value, decimals)
}

// 1분마다 새로고침
const startMarketDataRefresh = () => {
  setInterval(() => {
    fetchMarketData()
  }, 60000)
}

onMounted(() => {
  fetchMarketData()
  startMarketDataRefresh()
})
</script>

<style scoped>
.market-trend-list {
  @apply bg-white rounded-lg overflow-hidden;
}
</style> 