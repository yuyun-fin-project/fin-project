<template>
  <div class="search-container space-y-6">
    <!-- 검색바 -->
    <div class="relative">
      <div class="relative">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="상품명 또는 은행명으로 검색"
          class="w-full h-12 px-4 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
          @input="handleSearch"
          @focus="showHistory = true"
        >
        <button
          v-if="searchTerm"
          @click="clearSearch"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 검색 히스토리 -->
      <div
        v-if="showHistory && searchHistory.length > 0"
        class="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="p-3 border-b border-gray-100">
          <div class="flex justify-between items-center">
            <span class="text-sm font-medium text-gray-700">최근 검색어</span>
            <button
              @click="clearSearchHistory"
              class="text-sm text-gray-500 hover:text-gray-700 hover:underline"
            >
              전체 삭제
            </button>
          </div>
        </div>
        <div class="max-h-60 overflow-y-auto">
          <div
            v-for="term in searchHistory"
            :key="term"
            class="flex items-center justify-between px-4 py-2 hover:bg-gray-50 cursor-pointer"
            @click="selectSearchTerm(term)"
          >
            <span class="text-gray-700">{{ term }}</span>
            <button
              @click.stop="removeFromHistory(term)"
              class="p-1 rounded-full hover:bg-gray-200 text-gray-400 hover:text-gray-600"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 필터 옵션 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="relative">
        <select
          v-model="filters.bank"
          class="w-full h-12 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none text-gray-900"
          @change="applyFilters"
        >
          <option value="">은행 선택</option>
          <option v-for="bank in banks" :key="bank.code" :value="bank.code">
            {{ bank.name }}
          </option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      <div class="relative">
        <select
          v-model="filters.period"
          class="w-full h-12 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none text-gray-900"
          @change="applyFilters"
        >
          <option value="">가입기간</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      <div class="relative">
        <input
          v-model.number="filters.minAmount"
          type="text"
          placeholder="최소금액"
          class="w-full h-12 pl-4 pr-16 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          @input="applyFilters"
        >
        <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">원</span>
      </div>

      <div class="relative">
        <input
          v-model.number="filters.maxAmount"
          type="text"
          placeholder="최대금액"
          class="w-full h-12 pl-4 pr-16 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          @input="applyFilters"
        >
        <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">원</span>
      </div>
    </div>

    <!-- 정렬 옵션 -->
    <div class="flex justify-end">
      <div class="relative w-48">
        <select
          v-model="sortBy"
          class="w-full h-10 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none text-gray-900 text-sm"
          @change="applyFilters"
        >
          <option value="interestRate">금리순</option>
          <option value="bankName">은행명순</option>
          <option value="period">가입기간순</option>
          <option value="amount">가입금액순</option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 활성화된 필터 태그 -->
    <div class="flex flex-wrap gap-2">
      <div
        v-for="(value, key) in activeFilters"
        :key="key"
        class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full text-sm"
      >
        <span>{{ getFilterLabel(key, value) }}</span>
        <button 
          @click="removeFilter(key)" 
          class="ml-2 p-0.5 rounded-full hover:bg-blue-100"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDebounce, useSearchHistory, useQueryParams, sortFunctions } from '../utils/search'

const router = useRouter()
const { updateQueryParams, getQueryParams } = useQueryParams(router)
const { getHistory, addToHistory, clearHistory } = useSearchHistory()

// 상태 관리
const searchTerm = ref('')
const showHistory = ref(false)
const searchHistory = ref(getHistory())
const sortBy = ref('interestRate')
let debounceTimeout = null

const filters = ref({
  bank: '',
  period: '',
  minAmount: '',
  maxAmount: ''
})

// 은행 목록
const banks = [
  { code: 'KB', name: '국민은행' },
  { code: 'SH', name: '신한은행' },
  { code: 'WR', name: '우리은행' },
  { code: 'NH', name: '농협은행' },
  { code: 'IBK', name: '기업은행' }
]

// 활성화된 필터 계산
const activeFilters = computed(() => {
  return Object.entries(filters.value).reduce((acc, [key, value]) => {
    if (value && key !== 'productType') acc[key] = value
    return acc
  }, {})
})

// 필터 라벨 가져오기
const getFilterLabel = (key, value) => {
  switch (key) {
    case 'bank':
      return `${banks.find(b => b.code === value)?.name}`
    case 'period':
      return `${value}개월`
    case 'minAmount':
      return `최소 ${Number(value).toLocaleString()}원`
    case 'maxAmount':
      return `최대 ${Number(value).toLocaleString()}원`
    default:
      return value
  }
}

// 검색어 처리
const handleSearch = async () => {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout)
  }

  debounceTimeout = setTimeout(async () => {
    if (searchTerm.value.trim()) {
      addToHistory(searchTerm.value)
    }
    
    emit('search', { 
      term: searchTerm.value, 
      filters: filters.value, 
      sortBy: sortBy.value 
    })
  }, 500)
}

// 필터 적용
const applyFilters = () => {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout)
  }

  debounceTimeout = setTimeout(() => {
    emit('search', {
      term: searchTerm.value,
      filters: filters.value,
      sortBy: sortBy.value
    })
  }, 500)
}

// 검색어 선택
const selectSearchTerm = (term) => {
  searchTerm.value = term
  showHistory.value = false
  handleSearch()
}

// 검색어 지우기
const clearSearch = () => {
  searchTerm.value = ''
  emit('search', { term: '', filters: filters.value, sortBy: sortBy.value })
}

// 검색 기록 관리
const clearSearchHistory = () => {
  clearHistory()
  searchHistory.value = []
}

const removeFromHistory = (term) => {
  searchHistory.value = searchHistory.value.filter(t => t !== term)
  localStorage.setItem('search_history', JSON.stringify(searchHistory.value))
}

// 필터 제거
const removeFilter = (key) => {
  filters.value[key] = ''
  applyFilters()
}

// URL 쿼리 파라미터와 동기화 (초기 로드시에만)
onMounted(() => {
  const query = getQueryParams()
  if (query.q) searchTerm.value = query.q
  if (query.bank) filters.value.bank = query.bank
  if (query.period) filters.value.period = query.period
  if (query.minAmount) filters.value.minAmount = query.minAmount
  if (query.maxAmount) filters.value.maxAmount = query.maxAmount
  if (query.sort) sortBy.value = query.sort

  // 초기 검색 실행
  handleSearch()

  // 클릭 이벤트 리스너 추가
  document.addEventListener('click', handleClickOutside)
})

// 이벤트 정의
const emit = defineEmits(['search'])

// 클릭 이벤트 감지하여 히스토리 숨기기
const handleClickOutside = (event) => {
  if (!event.target.closest('.search-container')) {
    showHistory.value = false
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (debounceTimeout) {
    clearTimeout(debounceTimeout)
  }
})
</script>

<style scoped>
.search-container {
  @apply w-full;
}

/* 스크롤바 스타일링 */
.max-h-60 {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E1 #F1F5F9;
}

.max-h-60::-webkit-scrollbar {
  width: 6px;
}

.max-h-60::-webkit-scrollbar-track {
  background: #F1F5F9;
}

.max-h-60::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 3px;
}
</style> 