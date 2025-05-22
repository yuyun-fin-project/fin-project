<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold text-gray-900">금융상품 금리 비교</h2>
      <slot name="action"></slot>
    </div>

    <!-- 필터 옵션 -->
    <div class="bg-white rounded-lg shadow p-6 mb-8" v-if="showFilters">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">은행명</label>
          <input
            v-model="selectedBank"
            type="text"
            placeholder="은행명으로 검색"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">가입기간 (개월)</label>
          <select
            v-model="selectedPeriod"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-8">
      {{ error }}
    </div>

    <!-- 상품 목록 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="product in sortedProducts.slice(0, maxItems)"
        :key="product.id"
        class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
      >
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3>
            <p class="text-sm text-gray-600">{{ product.bank_name }}</p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-bold text-blue-600">{{ product.interest_rate }}%</p>
          </div>
        </div>
        
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">가입기간</span>
            <span class="font-medium">{{ product.period }}개월</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">최소가입금액</span>
            <span class="font-medium">{{ formatAmount(product.min_amount) }}원</span>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t">
          <a
            :href="product.link"
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center justify-center"
          >
            상품 가입하기
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps } from 'vue'
import { useFinanceStore } from '../stores/finance.js'

const props = defineProps({
  maxItems: {
    type: Number,
    default: Infinity
  },
  showFilters: {
    type: Boolean,
    default: true
  },
  initialProducts: {
    type: Array,
    default: () => []
  },
  isSearching: {
    type: Boolean,
    default: false
  }
})

const financeStore = useFinanceStore()
const selectedBank = ref('')
const selectedPeriod = ref('')
const sortBy = ref('rate')
const isLoading = computed(() => props.isSearching)
const products = ref(props.initialProducts || [])
const error = ref(null)

// 은행 목록
const banks = [
  { code: 'KB', name: '국민은행' },
  { code: 'SH', name: '신한은행' },
  { code: 'WR', name: '우리은행' },
  { code: 'NH', name: '농협은행' },
  { code: 'IBK', name: '기업은행' }
]

// 상품 목록 감시
watch(() => props.initialProducts, (newProducts) => {
  if (Array.isArray(newProducts)) {
    products.value = [...newProducts]
  } else {
    products.value = []
  }
}, { immediate: true, deep: true })

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  if (!Array.isArray(products.value)) return []
  
  return products.value.filter(product => {
    if (!product) return false
    const bankMatch = !selectedBank.value || product.bank_code === selectedBank.value
    const periodMatch = !selectedPeriod.value || product.period === parseInt(selectedPeriod.value)
    return bankMatch && periodMatch
  })
})

// 정렬된 상품 목록
const sortedProducts = computed(() => {
  if (!Array.isArray(filteredProducts.value)) return []

  return [...filteredProducts.value].sort((a, b) => {
    if (!a || !b) return 0
    if (sortBy.value === 'rate') {
      return b.interest_rate - a.interest_rate
    } else {
      return a.bank_name.localeCompare(b.bank_name)
    }
  })
})

// 금액 포맷팅
const formatAmount = (amount) => {
  if (amount === undefined || amount === null) return '0';
  return Number(amount).toLocaleString('ko-KR');
}
</script> 