<template>
  <div class="max-w-4xl mx-auto p-4">
    <!-- 검색 필터 -->
    <div class="mb-6 bg-white p-4 rounded-lg shadow">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">상품 유형</label>
          <select
            v-model="productType"
            class="w-full border rounded-md p-2"
          >
            <option value="deposit">예금</option>
            <option value="saving">적금</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">은행명</label>
          <input
            v-model="searchBank"
            type="text"
            placeholder="은행명 검색"
            class="w-full border rounded-md p-2"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">최소 금리</label>
          <input
            v-model="minRate"
            type="number"
            step="0.1"
            placeholder="최소 금리"
            class="w-full border rounded-md p-2"
          >
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="financeStore.isLoading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="financeStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ financeStore.error }}
    </div>

    <!-- 상품 목록 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="bg-white p-4 rounded-lg shadow hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3>
            <p class="text-sm text-gray-600">{{ product.bank_name }}</p>
          </div>
          <div class="text-right">
            <p class="text-xl font-bold text-blue-600">{{ product.interest_rate }}%</p>
            <p class="text-sm text-gray-500">{{ product.period }}개월</p>
          </div>
        </div>
        <div class="mt-4 flex justify-between items-center">
          <p class="text-sm text-gray-600">
            최소금액: {{ formatAmount(product.min_amount) }}원
          </p>
          <a
            :href="product.link"
            target="_blank"
            class="text-blue-500 hover:text-blue-700 text-sm"
          >
            상세보기 →
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFinanceStore } from '@/stores/finance.js'

const financeStore = useFinanceStore()

const productType = ref('deposit')
const searchBank = ref('')
const minRate = ref(null)
const products = ref([])

// 상품 목록 필터링
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const bankMatch = searchBank.value === '' || 
      product.bank_name.toLowerCase().includes(searchBank.value.toLowerCase())
    const rateMatch = !minRate.value || product.interest_rate >= minRate.value
    return bankMatch && rateMatch
  })
})

// 금액 포맷팅
const formatAmount = (amount) => {
  return amount.toLocaleString('ko-KR')
}

// 상품 데이터 로드
const loadProducts = async () => {
  products.value = await financeStore.fetchProducts(productType.value)
}

// 상품 유형 변경 시 데이터 다시 로드
watch(productType, () => {
  loadProducts()
})

onMounted(() => {
  loadProducts()
})
</script> 