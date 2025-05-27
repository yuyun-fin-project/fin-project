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
import { ref, onMounted } from 'vue'
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

// 은행 목록 가져오기
const fetchBanks = async () => {
  try {
    const response = await axios.get('/finrecom/')
    if (response.data?.results?.prd) {
      // 중복 제거된 은행 목록 생성
      const uniqueBanks = [...new Set(response.data.results.prd.map(item => item.kor_co_nm))]
      banks.value = uniqueBanks.sort() // 알파벳 순으로 정렬
    }
  } catch (err) {
    console.error('은행 목록 가져오기 실패:', err)
  }
}

// 검색 처리
const handleSearch = () => {
  const params = {
    kor_co_nm: searchParams.value.bank,
    prd_type: searchParams.value.productType === 'all' ? '' : searchParams.value.productType,
    sort: searchParams.value.sortBy
  }
  
  // 빈 값은 제외하고 emit
  Object.keys(params).forEach(key => {
    if (!params[key]) {
      delete params[key]
    }
  })
  
  emit('search', params)
}

// 컴포넌트 마운트 시 은행 목록 가져오기
onMounted(async () => {
  await fetchBanks()
  handleSearch() // 초기 검색 실행
})
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