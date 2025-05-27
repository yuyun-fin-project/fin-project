<template>
  <div class="products-view">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-6xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        금융상품 비교
      </h1>

      <!-- 검색 컴포넌트 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="400"
        class="mb-6"
      >
        <ProductSearch
          @search="handleSearch"
        />
      </div>

      <!-- 상품 비교 테이블 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="500"
        class="bg-white rounded-xl shadow-sm"
      >
        <ProductComparison
          :products="products"
          :is-loading="isLoading"
          :error="error"
          :is-authenticated="isAuthenticated"
          :sort-by="currentSort"
          @bookmark-updated="handleBookmarkUpdated"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductComparison from '@/components/product/ProductComparison.vue'
import ProductSearch from '@/components/product/ProductSearch.vue'
import { useFinanceStore } from '@/stores/finance'
import axios from 'axios'
import { useModalStore } from '../stores/modalStore'

const financeStore = useFinanceStore()
const isLoading = ref(false)
const error = ref(null)
const products = ref([])
const isAuthenticated = ref(false)
const authError = ref(null)
const currentSort = ref('rate_desc')
const modalStore = useModalStore()

const API_BASE_URL = 'http://localhost:8000'

// 인증 상태 확인
const checkAuthStatus = async () => {
  try {
    const accessToken = localStorage.getItem('access_token')
    if (!accessToken) {
      isAuthenticated.value = false
      return
    }

    // 토큰 유효성 검증
    try {
      const response = await axios.get('/accounts/verify-token/', {
        headers: { Authorization: `Bearer ${accessToken}` }
      })
      isAuthenticated.value = true
      authError.value = null
    } catch (tokenError) {
      // 토큰이 만료된 경우 리프레시 토큰으로 갱신 시도
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const refreshResponse = await axios.post('/accounts/token/refresh/', {
            refresh: refreshToken
          })
          localStorage.setItem('access_token', refreshResponse.data.access)
          isAuthenticated.value = true
          authError.value = null
        } catch (refreshError) {
          console.error('토큰 갱신 실패:', refreshError)
          handleAuthError()
        }
      } else {
        handleAuthError()
      }
    }
  } catch (error) {
    console.error('인증 상태 확인 실패:', error)
    handleAuthError()
  }
}

// 인증 에러 처리
const handleAuthError = () => {
  isAuthenticated.value = false
  authError.value = '로그인이 필요합니다.'
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

// 상품 데이터 가져오기
const fetchProducts = async (searchParams = {}) => {
  isLoading.value = true
  error.value = null
  
  try {
    // 인증 상태 확인
    await checkAuthStatus()
    
    const accessToken = localStorage.getItem('access_token')
    const response = await axios.get(`${API_BASE_URL}/finrecom/`, {
      headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
      params: {
        bank: searchParams.bank || '',
        product_type: searchParams.productType !== 'all' ? searchParams.productType : '',
        sort_by: searchParams.sortBy || 'rate_desc'
      }
    })
    console.log('API 응답:', response.data)

    if (!response.data?.results?.prd || !response.data?.results?.opt) {
      throw new Error('API 응답 데이터 형식이 올바르지 않습니다.')
    }

    const prdList = response.data.results.prd
    const optList = response.data.results.opt

    // 상품별 옵션 매핑
    let mappedProducts = prdList.map(prd => {
      // 해당 상품의 옵션들을 찾습니다
      const productOptions = optList.filter(opt => opt.prd === prd.id)
      
      // 선택된 가입기간에 해당하는 옵션만 필터링
      const filteredOptions = searchParams.save_trm
        ? productOptions.filter(opt => opt.save_trm === parseInt(searchParams.save_trm))
        : productOptions

      // 옵션 데이터 변환
      const processedOptions = filteredOptions.map(opt => ({
        ...opt,
        save_trm: opt.save_trm ? parseInt(opt.save_trm) : null,
        intr_rate: opt.intr_rate !== null ? parseFloat(opt.intr_rate) : 0,
        intr_rate2: opt.intr_rate2 !== null ? parseFloat(opt.intr_rate2) : 0
      }))

      // 최종 상품 데이터 구성
      return {
        ...prd,
        options: processedOptions
      }
    })

    products.value = mappedProducts

  } catch (err) {
    console.error('금융상품 데이터 가져오기 실패:', err)
    error.value = '금융상품 데이터를 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 검색 처리
const handleSearch = (searchParams) => {
  console.log('검색 파라미터:', searchParams) // 디버깅용
  currentSort.value = searchParams.sortBy || 'rate_desc'
  fetchProducts({
    bank: searchParams.bank || '',
    productType: searchParams.productType || 'all',
    sortBy: searchParams.sortBy || 'rate_desc'
  })
}

// 북마크 업데이트 처리
const handleBookmarkUpdated = () => {
  fetchProducts()
}

onMounted(async () => {
  await checkAuthStatus()
  await fetchProducts()
})
</script>

<style scoped>
.products-view {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem;
  padding-top: 5rem;
}

.product-comparison-container {
  @apply container mx-auto px-4 py-8;
}

.comparison-title {
  @apply text-3xl font-bold text-center mb-8;
}

.filters-section {
  @apply bg-white rounded-lg shadow-sm p-6 mb-8;
}
</style> 