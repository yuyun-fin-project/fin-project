<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-900">금융상품 금리비교</h2>
      <router-link
        to="/products"
        class="text-sm text-blue-600 hover:text-blue-800 font-medium"
      >
        더 알아보기 →
      </router-link>
    </div>

    <div class="flex-1 flex flex-col">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="flex-1 flex items-center justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>

      <!-- 에러 메시지 -->
      <div v-else-if="error" class="flex-1 flex items-center justify-center text-red-600">
        {{ error }}
      </div>

      <!-- 금리 비교 테이블 -->
      <div v-else class="flex-1 overflow-hidden">
        <table class="min-w-full table-fixed">
          <thead class="bg-white">
            <tr class="border-b border-gray-200">
              <th class="w-1/2 px-4 py-3 text-left text-sm font-semibold text-gray-600">상품명</th>
              <th class="w-1/4 px-4 py-3 text-right text-sm font-semibold text-gray-600">최고금리</th>
              <th class="w-1/4 px-4 py-3 text-right text-sm font-semibold text-gray-600">기간</th>
            </tr>
          </thead>
        </table>
        
        <div class="overflow-hidden" style="height: 240px"> <!-- 4개 항목이 보이도록 높이 고정 -->
          <div 
            ref="scrollContainer" 
            class="transition-transform duration-1000 ease-linear"
            :style="{ transform: `translateY(${-scrollPosition}px)` }"
          >
            <table class="min-w-full table-fixed">
              <tbody>
                <tr 
                  v-for="product in displayProducts" 
                  :key="product.id"
                  class="hover:bg-gray-50 cursor-pointer group h-15"
                  @click="openDetail(product)"
                >
                  <td class="w-1/2 px-4 py-3">
                    <div class="text-sm text-gray-900 truncate">{{ product.fin_prdt_nm }}</div>
                    <div class="text-xs text-gray-500 truncate">{{ product.kor_co_nm }}</div>
                  </td>
                  <td class="w-1/4 px-4 py-3 text-right">
                    <span :class="getInterestRateColor(getMaxRate(product))" class="text-sm whitespace-nowrap">
                      {{ getMaxRate(product) }}%
                    </span>
                  </td>
                  <td class="w-1/4 px-4 py-3 text-right">
                    <span class="text-sm text-gray-600 whitespace-nowrap">
                      {{ getMinPeriod(product) }}개월
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 상품 상세 모달 -->
    <ProductDetailModal
      v-if="showModal"
      :show="showModal"
      :product="selectedProduct"
      :is-authenticated="isAuthenticated"
      @close="closeModal"
      @bookmark-updated="fetchProducts"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import ProductDetailModal from './product/ProductDetailModal.vue'

// 상태 관리
const isLoading = ref(false)
const error = ref(null)
const products = ref([])
const showModal = ref(false)
const selectedProduct = ref(null)
const isAuthenticated = ref(false)
const scrollPosition = ref(0)
const scrollContainer = ref(null)
let animationInterval = null

// 상품 데이터 가져오기
const fetchProducts = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await axios.get('/finrecom/')
    
    if (!response.data?.results?.prd || !response.data?.results?.opt) {
      throw new Error('API 응답 데이터 형식이 올바르지 않습니다.')
    }

    const prdList = response.data.results.prd
    const optList = response.data.results.opt

    // 상품별 옵션 매핑
    products.value = prdList.map(prd => ({
      ...prd,
      options: optList.filter(opt => opt.fin_prdt_cd === prd.fin_prdt_cd)
        .map(opt => ({
          ...opt,
          save_trm: parseInt(opt.save_trm) || 12,
          intr_rate: parseFloat(opt.intr_rate) || 0,
          intr_rate2: parseFloat(opt.intr_rate2) || 0
        }))
    }))

    // 금리 기준으로 정렬
    products.value.sort((a, b) => getMaxRate(b) - getMaxRate(a))
    
    startScrollAnimation()
  } catch (err) {
    console.error('금융상품 데이터 가져오기 실패:', err)
    error.value = '금융상품 데이터를 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 스크롤 애니메이션 시작
const startScrollAnimation = () => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }

  const ROW_HEIGHT = 60 // 각 행의 높이
  const SCROLL_INTERVAL = 3000 // 스크롤 간격 (3초)
  
  animationInterval = setInterval(() => {
    if (scrollPosition.value >= (products.value.length - 4) * ROW_HEIGHT) {
      // 마지막에 도달하면 처음으로 돌아감
      scrollPosition.value = 0
    } else {
      scrollPosition.value += ROW_HEIGHT
    }
  }, SCROLL_INTERVAL)
}

// 표시할 전체 상품 목록
const displayProducts = computed(() => {
  // 원본 배열을 두 번 연결하여 무한 스크롤 효과 생성
  return [...products.value, ...products.value]
})

// 최고 금리 계산
const getMaxRate = (product) => {
  if (!product.options?.length) return 0
  
  const rates = product.options.map(opt => 
    Math.max(parseFloat(opt.intr_rate) || 0, parseFloat(opt.intr_rate2) || 0)
  )
  return parseFloat(Math.max(...rates).toFixed(2))
}

// 최소 가입기간 계산
const getMinPeriod = (product) => {
  if (!product.options?.length) return '-'
  
  const periods = product.options.map(opt => parseInt(opt.save_trm) || 12)
  return Math.min(...periods)
}

// 금리에 따른 색상 반환
const getInterestRateColor = (rate) => {
  if (rate >= 5) return 'text-red-600 font-semibold'
  if (rate >= 4) return 'text-orange-600 font-semibold'
  if (rate >= 3) return 'text-blue-600 font-semibold'
  return 'text-gray-900'
}

// 모달 관련 함수
const openDetail = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}

// 인증 상태 확인
const checkAuthStatus = async () => {
  const token = localStorage.getItem('access_token')
  isAuthenticated.value = !!token
}

onMounted(async () => {
  await checkAuthStatus()
  await fetchProducts()
})

onUnmounted(() => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
})
</script>

<style scoped>
.table-fixed {
  table-layout: fixed;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.h-15 {
  height: 60px;
}

tr {
  background-color: white;
}

.group:hover {
  background-color: #f9fafb;
}

/* 스크롤바 숨기기 */
.overflow-hidden::-webkit-scrollbar {
  display: none;
}
</style> 