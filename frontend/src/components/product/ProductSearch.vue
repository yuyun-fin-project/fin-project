<template>
  <div class="bg-white rounded-xl shadow-sm p-6">
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <!-- 은행 선택 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">은행</label>
        <select 
          v-model="searchParams.bank" 
          class="w-full text-black rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          @change="handleSearch"
        >
          <option value="">전체</option>
          <option v-for="bank in banks" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
      
      <!-- 상품 유형 선택 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">상품 유형</label>
        <select 
          v-model="searchParams.productType" 
          class="w-full rounded-lg text-black border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          @change="handleSearch"
        >
          <option value="all">전체</option>
          <option value="D">예금</option>
          <option value="S">적금</option>
        </select>
      </div>
      
      <!-- 정렬 기준 선택 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">정렬 기준</label>
        <select 
          v-model="searchParams.sortBy" 
          class="w-full rounded-lg text-black border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          @change="handleSearch"
        >
          <option value="rate_desc">금리 높은순</option>
          <option value="rate_asc">금리 낮은순</option>
          <option value="bank">은행명순</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const emit = defineEmits(['search'])

// 검색 파라미터
const searchParams = ref({
  bank: '',
  productType: 'all',
  sortBy: 'rate_desc'
})

// 은행 목록
const banks = ref([])

// 상품 데이터
const products = ref([])
const options = ref([])

// API 기본 설정
const API_BASE_URL = 'http://localhost:8000'

// 최대 금리 계산 함수
const getMaxRate = (product, allOptions) => {
  const productOptions = allOptions.filter(opt => opt.prd === product.id)
  let maxRate = 0
  
  productOptions.forEach(option => {
    const rate = parseFloat(option.intr_rate2 || option.intr_rate || 0)
    if (!isNaN(rate) && rate > maxRate) {
      maxRate = rate
    }
  })
  
  return maxRate
}

// 정렬 함수
const sortProducts = (products, options, sortBy) => {
  return [...products].sort((a, b) => {
    if (sortBy === 'rate_desc' || sortBy === 'rate_asc') {
      const rateA = getMaxRate(a, options)
      const rateB = getMaxRate(b, options)
      return sortBy === 'rate_desc' ? rateB - rateA : rateA - rateB
    } else if (sortBy === 'bank') {
      return a.kor_co_nm.localeCompare(b.kor_co_nm, 'ko-KR')
    }
    return 0
  })
}

// 은행 목록 가져오기
const fetchBanks = async () => {
  try {
    const params = new URLSearchParams()
    if (searchParams.value.bank) {
      params.append('bank', searchParams.value.bank)
    }
    if (searchParams.value.productType !== 'all') {
      params.append('product_type', searchParams.value.productType)
    }
    if (searchParams.value.sortBy) {
      params.append('sort_by', searchParams.value.sortBy)
    }

    const response = await axios.get(`${API_BASE_URL}/finrecom/`, {
      params: params
    })

    if (response.data?.results?.prd) {
      // 중복 제거된 은행 목록 생성 및 정렬
      const uniqueBanks = [...new Set(
        response.data.results.prd
          .map(item => item.kor_co_nm)
          .filter(bank => bank)
      )].sort((a, b) => a.localeCompare(b, 'ko-KR'))

      banks.value = uniqueBanks
      products.value = response.data.results.prd
      options.value = response.data.results.opt

      // 검색 결과 emit
      emit('search', {
        products: response.data.results.prd,
        options: response.data.results.opt
      })
    }
  } catch (err) {
    console.error('은행 목록 가져오기 실패:', err)
  }
}

// 검색 및 정렬 처리
const handleSearch = async () => {
  try {
    // 검색 결과 emit
    emit('search', {
      bank: searchParams.value.bank,
      productType: searchParams.value.productType,
      sortBy: searchParams.value.sortBy
    })
  } catch (error) {
    console.error('검색 실패:', error)
  }
}

// 컴포넌트 마운트 시 초기 데이터 가져오기
onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/finrecom/`)
    if (response.data?.results?.prd) {
      // 중복 제거된 은행 목록 생성 및 정렬
      const uniqueBanks = [...new Set(
        response.data.results.prd
          .map(item => item.kor_co_nm)
          .filter(bank => bank)
      )].sort((a, b) => a.localeCompare(b, 'ko-KR'))

      banks.value = uniqueBanks
      
      // 초기 검색 결과 emit
      emit('search', {
        bank: searchParams.value.bank,
        productType: searchParams.value.productType,
        sortBy: searchParams.value.sortBy
      })
    }
  } catch (err) {
    console.error('초기 데이터 로딩 실패:', err)
  }
})

// 검색 파라미터 변경 감시
watch(searchParams, () => {
  handleSearch()
}, { deep: true })
</script>

<style scoped>
select {
  @apply appearance-none bg-white;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236B7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

select:focus {
  @apply ring-2 ring-blue-500 border-blue-500;
}
</style> 