<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">찜한 금융상품</h2>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
      {{ error }}
    </div>

    <!-- 찜한 상품이 없는 경우 -->
    <div v-else-if="bookmarkedProducts.length === 0" class="text-center py-8">
      <p class="text-gray-500">찜한 금융상품이 없습니다.</p>
      <router-link 
        to="/products" 
        class="mt-2 inline-block text-sm text-blue-600 hover:text-blue-800"
      >
        금융상품 둘러보기
      </router-link>
    </div>

    <!-- 상품 목록 -->
    <div v-else class="space-y-3">
      <div
        v-for="product in displayedProducts"
        :key="product.id"
        class="p-4 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer"
        @click="openProductDetail(product)"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium text-gray-900">{{ product.fin_prdt_nm }}</h3>
            <p class="text-sm text-gray-600">{{ product.kor_co_nm }}</p>
          </div>
          <div class="text-right">
            <p class="text-lg font-bold text-blue-600">{{ product.displayRate.toFixed(2) }}%</p>
            <p class="text-sm text-gray-600">{{ product.displayPeriod }}개월</p>
          </div>
        </div>
        
        <div class="mt-2 flex justify-end items-center">
          <button 
            @click.stop="removeBookmark(product)"
            class="text-yellow-500 hover:text-yellow-600"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 펼치기/접기 버튼 -->
      <div v-if="bookmarkedProducts.length > 3" class="text-center mt-4">
        <button 
          @click="toggleExpand"
          class="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
        >
          <span>{{ isExpanded ? '접기' : '더보기' }}</span>
          <svg 
            class="w-4 h-4 ml-1 transition-transform"
            :class="{ 'transform rotate-180': isExpanded }"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import ProductDetailModal from '../product/ProductDetailModal.vue'
import { useModalStore } from '../../stores/modalStore'
import eventBus from '../../utils/eventBus'

const bookmarkedProducts = ref([])
const isLoading = ref(false)
const error = ref(null)
const showModal = ref(false)
const selectedProduct = ref(null)
const accessToken = ref(localStorage.getItem('access_token'))
const modalStore = useModalStore()
const isExpanded = ref(false)

// 프리뷰에서는 펼침 상태에 따라 전체 또는 3개만 표시
const displayedProducts = computed(() => {
  const products = bookmarkedProducts.value.map(product => ({
    ...product,
    displayRate: calculateMaxRate(product),
    displayPeriod: calculatePeriod(product)
  }))
  return isExpanded.value ? products : products.slice(0, 3)
})

// 찜한 상품 목록 가져오기
const fetchBookmarkedProducts = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await axios.get('/finrecom/bookmark/product/', {
      headers: {
        'Authorization': `Bearer ${accessToken.value}`
      }
    })
    console.log('찜한 상품 목록:', response.data)

    // 각 북마크된 상품의 상세 정보 가져오기
    const bookmarks = response.data || []
    const productsWithDetails = await Promise.all(
      bookmarks.map(async (bookmark) => {
        try {
          const productResponse = await axios.get(`/finrecom/`, {
            params: {
              id: bookmark.product_id
            }
          })
          
          // 해당 ID의 상품 찾기
          const product = productResponse.data.results.prd.find(p => p.id === bookmark.product_id)
          if (!product) {
            console.error(`상품을 찾을 수 없습니다 (ID: ${bookmark.product_id})`)
            return null
          }

          // 옵션 정보도 함께 가져오기
          const options = productResponse.data.results.opt || []
          const productOptions = options.filter(opt => opt.prd === product.id)
          
          // 옵션 정보 가공
          const processedOptions = productOptions.map(opt => ({
            ...opt,
            save_trm: parseInt(opt.save_trm) || 12,
            intr_rate: parseFloat(opt.intr_rate) || 0,
            intr_rate2: parseFloat(opt.intr_rate2) || 0,
            rsrv_type_nm: opt.rsrv_type_nm || '자유적립식',
            intr_rate_type_nm: opt.intr_rate_type_nm || '단리'
          }))

          // 원본 데이터 구조 유지
          return {
            ...product,
            options: processedOptions,
            bookmarkId: bookmark.id
          }
        } catch (error) {
          console.error(`상품 정보 로드 실패 (ID: ${bookmark.product_id}):`, error)
          return null
        }
      })
    )

    bookmarkedProducts.value = productsWithDetails.filter(product => product !== null)
  } catch (error) {
    console.error('찜한 상품 목록 로드 실패:', error)
    error.value = '찜한 상품 목록을 불러오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 금리 계산 헬퍼 함수
const calculateMaxRate = (product) => {
  if (!product.options?.length) return 0
  
  const rates = product.options.map(opt => 
    Math.max(parseFloat(opt.intr_rate) || 0, parseFloat(opt.intr_rate2) || 0)
  )
  return Math.max(...rates)
}

// 기간 계산 헬퍼 함수
const calculatePeriod = (product) => {
  if (!product.options?.length) return null
  
  const periods = product.options
    .map(opt => parseInt(opt.save_trm))
    .filter(p => !isNaN(p))
  
  if (periods.length === 0) return null
  return Math.min(...periods)
}

// 찜하기 제거
const removeBookmark = async (product) => {
  try {
    await axios.post(`/finrecom/bookmark/product/${product.id}/`, {}, {
      headers: {
        'Authorization': `Bearer ${accessToken.value}`
      }
    })
    
    // 즉시 목록에서 제거
    bookmarkedProducts.value = bookmarkedProducts.value.filter(p => p.id !== product.id)
    
    // 모달 닫기
    modalStore.closeModal()
    
    // 북마크 수 변경 이벤트 발생
    eventBus.emit('bookmark-count-updated', bookmarkedProducts.value.length)
    
    // 전체 목록 다시 불러오기
    await fetchBookmarkedProducts()
  } catch (error) {
    console.error('찜하기 제거 실패:', error)
    alert('찜하기 제거 중 오류가 발생했습니다.')
  }
}

// 금액 포맷팅
const formatAmount = (amount) => {
  if (amount === undefined || amount === null) return '0'
  return Number(amount).toLocaleString('ko-KR')
}

// 상품 상세 모달 관련 함수
const openProductDetail = (product) => {
  modalStore.openProductDetailModal(product, {
    onBookmarkUpdated: (data) => {
      if (!data.isBookmarked) {
        // 찜 해제된 상품을 즉시 목록에서 제거
        bookmarkedProducts.value = bookmarkedProducts.value.filter(p => p.id !== data.productId)
        // 북마크 수 변경 이벤트 발생
        eventBus.emit('bookmark-count-updated', bookmarkedProducts.value.length)
      }
    }
  })
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}

const handleBookmarkUpdated = async () => {
  await fetchBookmarkedProducts()
}

// 펼치기/접기 토글 함수
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

onMounted(() => {
  fetchBookmarkedProducts()
  
  // 모달 스토어 이벤트 구독
  modalStore.$subscribe((mutation, state) => {
    if (mutation.type === 'closeModal' && state.lastAction === 'bookmark_update') {
      fetchBookmarkedProducts().then(() => {
        // 북마크 수 변경 이벤트 발생
        eventBus.emit('bookmark-count-updated', bookmarkedProducts.value.length)
      })
    }
  })
})

// 컴포넌트 언마운트 시 구독 해제
onUnmounted(() => {
  if (modalStore.$unsubscribe) {
    modalStore.$unsubscribe()
  }
})
</script> 