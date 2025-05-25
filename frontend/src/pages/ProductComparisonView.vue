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

      <!-- 검색 필터 섹션 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="400"
        class="bg-white rounded-xl shadow-sm p-6 mb-6"
      >
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          <!-- 은행 선택 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">은행</label>
            <select 
              v-model="selectedBank" 
              class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">전체</option>
              <option v-for="bank in banks" :key="bank.code" :value="bank.name">
                {{ bank.name }}
              </option>
            </select>
          </div>
          
          <!-- 상품 유형 선택 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">상품 유형</label>
            <select 
              v-model="selectedType" 
              class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option v-for="type in productTypes" :key="type.value" :value="type.value">
                {{ type.label }}
              </option>
            </select>
          </div>
          
          <!-- 가입 기간 선택 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">가입 기간</label>
            <select 
              v-model="selectedPeriod" 
              class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">전체</option>
              <option v-for="period in periods" :key="period" :value="period">
                {{ period }}개월
              </option>
            </select>
          </div>

          <!-- 최소금액 입력 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">최소금액</label>
            <div class="mt-1 relative rounded-lg shadow-sm">
              <input
                type="number"
                v-model="minAmount"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 pl-3 pr-12"
                placeholder="0"
              />
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <span class="text-gray-500 sm:text-sm">원</span>
              </div>
            </div>
          </div>
          
          <!-- 정렬 기준 선택 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">정렬 기준</label>
            <select 
              v-model="sortBy" 
              class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="rate">금리순</option>
              <option value="bank">은행명순</option>
            </select>
          </div>
        </div>
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
          :selected-bank="selectedBank"
          :selected-type="selectedType"
          :selected-period="selectedPeriod"
          :sort-by="sortBy"
          @bookmark-updated="handleBookmarkUpdated"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ProductComparison from '@/components/product/ProductComparison.vue'
import { useFinanceStore } from '@/stores/finance'
import axios from 'axios'

const financeStore = useFinanceStore()
const isLoading = ref(false)
const error = ref(null)
const products = ref([])
const isAuthenticated = ref(false)
const authError = ref(null)

// 필터 상태
const selectedBank = ref('')
const selectedType = ref('all')
const selectedPeriod = ref('')
const sortBy = ref('rate')
const minAmount = ref('')

// 은행 목록
const banks = [
  { code: 'KB', name: '국민은행' },
  { code: 'SH', name: '신한은행' },
  { code: 'WR', name: '우리은행' },
  { code: 'NH', name: '농협은행' },
  { code: 'IBK', name: '기업은행' }
]

// 상품 유형 옵션
const productTypes = [
  { value: 'all', label: '전체' },
  { value: 'D', label: '예금' },
  { value: 'S', label: '적금' }
]

// 가입 기간 옵션
const periods = [6, 12, 24, 36]

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
const fetchProducts = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // 인증 상태 확인
    await checkAuthStatus()
    
    const accessToken = localStorage.getItem('access_token')
    const response = await axios.get('/finrecom/', {
      headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {}
    })
    console.log('API 응답:', response.data)

    if (!response.data?.results?.prd || !response.data?.results?.opt) {
      throw new Error('API 응답 데이터 형식이 올바르지 않습니다.')
    }

    const prdList = response.data.results.prd
    const optList = response.data.results.opt

    // 상품별 옵션 매핑
    const mappedProducts = prdList.map(prd => {
      // 1. 해당 상품의 옵션들 찾기
      const productOptions = optList.filter(opt => 
        opt.fin_prdt_cd === prd.fin_prdt_cd
      )

      // 2. 옵션들을 저축 기간별로 정리
      const optionsByPeriod = {}
      productOptions.forEach(opt => {
        const period = parseInt(opt.save_trm)
        if (!isNaN(period)) {
          if (!optionsByPeriod[period]) {
            optionsByPeriod[period] = []
          }
          optionsByPeriod[period].push({
            save_trm: period,
            intr_rate: parseFloat(opt.intr_rate || '0'),
            intr_rate2: parseFloat(opt.intr_rate2 || '0'),
            intr_rate_type: opt.intr_rate_type,
            intr_rate_type_nm: opt.intr_rate_type_nm,
            rsrv_type: opt.rsrv_type,
            rsrv_type_nm: opt.rsrv_type_nm
          })
        }
      })

      // 3. 각 기간별로 최적의 금리 옵션 선택
      const finalOptions = Object.entries(optionsByPeriod).map(([period, opts]) => {
        // 각 기간별로 가장 높은 기본금리와 우대금리 선택
        const bestOption = opts.reduce((best, current) => {
          if (!best || current.intr_rate > best.intr_rate) {
            return current
          }
          return best
        }, null)

        return bestOption
      })

      // 4. 최종 상품 데이터 구성
      return {
        ...prd,
        options: finalOptions
      }
    })

    console.log('처리된 상품 데이터:', mappedProducts)
    products.value = mappedProducts

  } catch (err) {
    console.error('금융상품 데이터 가져오기 실패:', err)
    error.value = '금융상품 데이터를 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 북마크 업데이트 처리
const handleBookmarkUpdated = () => {
  fetchProducts()
}

// 필터 변경 감시
watch([selectedBank, selectedType, selectedPeriod, sortBy, minAmount], () => {
  fetchProducts()
})

onMounted(async () => {
  await checkAuthStatus()
  await fetchProducts()
})
</script>

<style scoped>
.products-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style> 