<template>
  <div class="products-view">
    <div
      v-motion-slide-visible-once-bottom
      class="max-w-7xl mx-auto px-4 py-12"
    >
      <!-- 제목 -->
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">금융상품 금리 비교</h1>

      <!-- 검색 컴포넌트 -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <ProductSearch @search="handleSearch" />
      </div>

      <!-- 상품 유형 선택 -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div class="flex space-x-4">
          <button 
            @click="loadProducts('deposit')"
            :class="[
              'px-6 py-2 rounded-lg font-medium',
              currentType === 'deposit' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]"
          >
            정기예금
          </button>
          <button 
            @click="loadProducts('saving')"
            :class="[
              'px-6 py-2 rounded-lg font-medium',
              currentType === 'saving' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]"
          >
            적금
          </button>
        </div>
      </div>

      <!-- 상품 목록 -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <ProductComparison 
          :maxItems="Infinity"
          :showFilters="false"
          :initialProducts="filteredProducts"
          :isSearching="isLoading"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ProductSearch from '../components/ProductSearch.vue'
import ProductComparison from '../components/ProductComparison.vue'
import { useFinanceStore } from '../stores/finance.js'
import { filterProducts, sortFunctions } from '../utils/search'

const financeStore = useFinanceStore()
const products = ref([])
const isLoading = ref(false)
const currentType = ref('deposit')
const searchParams = ref({
  term: '',
  filters: {},
  sortBy: 'interestRate'
})

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  let filtered = filterProducts(products.value, {
    searchTerm: searchParams.value.term,
    ...searchParams.value.filters
  })

  // 정렬 적용
  return filtered.sort(sortFunctions[searchParams.value.sortBy])
})

// 검색 처리
const handleSearch = ({ term, filters, sortBy }) => {
  searchParams.value = { term, filters, sortBy }
}

// 상품 데이터 로드
const loadProducts = async (type) => {
  isLoading.value = true
  currentType.value = type
  try {
    products.value = await financeStore.fetchProducts(type)
  } catch (error) {
    console.error('상품 데이터 로드 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 초기 데이터 로드
loadProducts('deposit')
</script>

<style scoped>
.products-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}
</style> 