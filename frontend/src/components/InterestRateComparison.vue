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

      <!-- 상품 목록 -->
      <div v-else class="flex-1 overflow-hidden">
        <div 
          class="relative overflow-y-auto h-full" 
          ref="scrollContainer"
          @mouseenter="pauseAnimation"
          @mouseleave="resumeAnimation"
        >
          <div class="absolute inset-0">
            <table class="min-w-full table-fixed">
              <tbody>
                <tr 
                  v-for="product in products" 
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
                      {{ getMaxRate(product).toFixed(2) }}%
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import ProductDetailModal from './product/ProductDetailModal.vue'
import { useModalStore } from '../stores/modalStore'

// 상태 관리
const isLoading = ref(false)
const error = ref(null)
const products = ref([])
const showModal = ref(false)
const selectedProduct = ref(null)
const isAuthenticated = ref(false)
const scrollPosition = ref(0)
const scrollContainer = ref(null)
const modalStore = useModalStore()
let animationInterval = null
const ROW_HEIGHT = 60 // 각 행의 높이

// 현재 표시 시작 인덱스
const currentIndex = ref(0)

// 화면에 표시할 상품 개수 계산
const calculateVisibleProducts = () => {
  if (!scrollContainer.value) return 4 // 기본값

  const containerHeight = scrollContainer.value.clientHeight
  return Math.floor(containerHeight / ROW_HEIGHT)
}

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
      options: optList.filter(opt => opt.prd === prd.id)
    }))
    
    // 컨테이너 크기에 맞춰 표시할 상품 개수 조정
    const visibleCount = calculateVisibleProducts()
    if (products.value.length < visibleCount) {
      // 표시할 개수보다 상품이 적으면 상품을 복제하여 채움
      const additionalProducts = [...products.value]
      while (products.value.length < visibleCount) {
        products.value = [...products.value, ...additionalProducts]
      }
    }
    
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

  const SCROLL_INTERVAL = 50 // 스크롤 간격 (0.05초)
  const SCROLL_STEP = 1 // 한 번에 이동할 픽셀
  
  animationInterval = setInterval(() => {
    if (!scrollContainer.value) return

    const maxScroll = scrollContainer.value.scrollHeight - scrollContainer.value.clientHeight
    const currentScroll = scrollContainer.value.scrollTop

    if (currentScroll >= maxScroll) {
      // 마지막에 도달하면 처음으로 즉시 이동
      scrollContainer.value.scrollTop = 0
    } else {
      // 부드럽게 스크롤
      scrollContainer.value.scrollTop = currentScroll + SCROLL_STEP
    }
  }, SCROLL_INTERVAL)
}

// 마우스가 컨테이너 위에 있을 때 자동 스크롤 멈춤
const pauseAnimation = () => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
}

// 마우스가 컨테이너를 벗어날 때 자동 스크롤 재시작
const resumeAnimation = () => {
  startScrollAnimation()
}

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
  
  const periods = product.options
    .map(opt => parseInt(opt.save_trm))
    .filter(p => !isNaN(p))
  
  if (periods.length === 0) return '-'
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
  modalStore.openProductDetailModal(product)
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

// 창 크기 변경 감지
let resizeObserver = null

onMounted(async () => {
  await checkAuthStatus()
  await fetchProducts()

  // ResizeObserver를 사용하여 컨테이너 크기 변경 감지
  resizeObserver = new ResizeObserver(() => {
    const visibleCount = calculateVisibleProducts()
    if (products.value.length < visibleCount) {
      const additionalProducts = [...products.value]
      while (products.value.length < visibleCount) {
        products.value = [...products.value, ...additionalProducts]
      }
    }
  })

  if (scrollContainer.value) {
    resizeObserver.observe(scrollContainer.value)
  }
})

onUnmounted(() => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
  if (resizeObserver) {
    resizeObserver.disconnect()
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

/* 스크롤바 스타일링 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 