<template>
  <div class="product-comparison">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      class="max-w-7xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        금융상품 금리 비교
      </h1>

      <!-- 상품 유형 선택 -->
      <div class="mb-8">
        <div class="flex space-x-4">
          <button
            @click="productType = 'deposit'"
            :class="[
              'px-6 py-3 rounded-lg font-medium',
              productType === 'deposit'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            예금 상품
          </button>
          <button
            @click="productType = 'saving'"
            :class="[
              'px-6 py-3 rounded-lg font-medium',
              productType === 'saving'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            적금 상품
          </button>
        </div>
      </div>

      <!-- 필터 섹션 -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">검색 조건</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              은행 선택
            </label>
            <select
              v-model="selectedBank"
              class="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">전체</option>
              <option v-for="bank in banks" :key="bank.code" :value="bank.code">
                {{ bank.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              가입 기간
            </label>
            <select
              v-model="selectedPeriod"
              class="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">전체</option>
              <option value="6">6개월</option>
              <option value="12">12개월</option>
              <option value="24">24개월</option>
              <option value="36">36개월</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              정렬 기준
            </label>
            <select
              v-model="sortBy"
              class="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="rate">금리 높은 순</option>
              <option value="bank">은행명 순</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 상품 목록 -->
      <div v-if="isLoading" class="loading">
        <div class="loading-spinner"></div>
      </div>
      <div v-else class="carousel-wrapper">
        <Carousel
          :items-to-show="1"
          :wrap-around="true"
          :autoplay="3000"
          :snap-align="'center'"
          :transition="600"
          :breakpoints="{
            '768': {
              itemsToShow: 2,
              snapAlign: 'center',
            },
            '1024': {
              itemsToShow: 3,
              snapAlign: 'center',
            }
          }"
        >
          <Slide
            v-for="product in sortedProducts"
            :key="product.id"
            class="carousel__slide"
          >
            <div class="carousel__item">
              <div class="bg-white rounded-xl shadow-lg p-6 mx-2">
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="text-xl font-semibold text-gray-900">{{ product.name }}</h3>
                    <p class="text-gray-600 mt-1">{{ product.bank_name }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-3xl font-bold text-blue-600">{{ product.interest_rate }}%</p>
                    <p class="text-sm text-gray-500">기본금리</p>
                  </div>
                </div>
                <div class="mt-4">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-600">가입 기간</p>
                      <p class="font-medium">{{ product.period }}개월</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-600">최소 가입금액</p>
                      <p class="font-medium">{{ formatAmount(product.min_amount) }}원</p>
                    </div>
                  </div>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <button
                    @click="getRecommendation(product)"
                    class="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    AI 상품 분석
                  </button>
                  <a
                    :href="product.link"
                    target="_blank"
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    가입하기
                  </a>
                </div>
              </div>
            </div>
          </Slide>

          <template #addons>
            <Navigation />
            <Pagination />
          </template>
        </Carousel>
      </div>

      <!-- AI 추천 모달 -->
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4"
      >
        <div class="bg-white rounded-xl max-w-2xl w-full p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-semibold">AI 상품 분석</h3>
            <button
              @click="showModal = false"
              class="text-gray-400 hover:text-gray-600"
            >
              <span class="sr-only">닫기</span>
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div v-if="isLoadingRecommendation" class="loading">
            <div class="loading-spinner"></div>
          </div>
          <div v-else class="prose max-w-none">
            <div v-html="recommendation"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useFinanceStore } from '../stores/finance.js'
import { Carousel, Navigation, Pagination, Slide } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'

const financeStore = useFinanceStore()
const productType = ref('deposit')
const selectedBank = ref('')
const selectedPeriod = ref('')
const sortBy = ref('rate')
const showModal = ref(false)
const recommendation = ref('')
const isLoadingRecommendation = ref(false)
const isLoading = ref(false)
const products = ref([])

// 은행 목록
const banks = [
  { code: 'KB', name: '국민은행' },
  { code: 'SH', name: '신한은행' },
  { code: 'WR', name: '우리은행' },
  { code: 'NH', name: '농협은행' },
  { code: 'IBK', name: '기업은행' }
]

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const bankMatch = !selectedBank.value || product.bank_code === selectedBank.value
    const periodMatch = !selectedPeriod.value || product.period === parseInt(selectedPeriod.value)
    return bankMatch && periodMatch
  })
})

// 정렬된 상품 목록
const sortedProducts = computed(() => {
  return [...filteredProducts.value].sort((a, b) => {
    if (sortBy.value === 'rate') {
      return b.interest_rate - a.interest_rate
    } else {
      return a.bank_name.localeCompare(b.bank_name)
    }
  })
})

// 금액 포맷팅
const formatAmount = (amount) => {
  return amount.toLocaleString('ko-KR')
}

// AI 추천 받기
const getRecommendation = async (product) => {
  isLoadingRecommendation.value = true
  showModal.value = true
  try {
    recommendation.value = await financeStore.getProductRecommendation(product)
  } catch (error) {
    recommendation.value = '죄송합니다. 현재 AI 분석을 불러올 수 없습니다.'
  } finally {
    isLoadingRecommendation.value = false
  }
}

// 상품 데이터 로드
const loadProducts = async () => {
  isLoading.value = true
  try {
    products.value = await financeStore.fetchProducts(productType.value)
  } catch (error) {
    console.error('상품 데이터 로드 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 상품 유형 변경 시 데이터 다시 로드
watch(productType, () => {
  loadProducts()
})

// 초기 데이터 로드
loadProducts()
</script>

<style scoped>
.product-comparison {
  @apply min-h-screen bg-gray-50;
}

.carousel-wrapper {
  @apply py-8 max-w-7xl mx-auto;
}

.carousel__slide {
  @apply h-full;
  height: 400px;
  padding: 0.5rem;
}

.carousel__item {
  @apply h-full transition-all duration-300;
}

.carousel__item:hover {
  @apply transform -translate-y-1 shadow-xl;
}

:deep(.carousel__viewport) {
  @apply py-4;
}

:deep(.carousel__track) {
  @apply items-stretch;
}

:deep(.carousel__pagination) {
  @apply mt-4;
}

:deep(.carousel__pagination-button) {
  @apply w-3 h-3 rounded-full bg-gray-300;
}

:deep(.carousel__pagination-button--active) {
  @apply bg-blue-500;
}

:deep(.carousel__prev),
:deep(.carousel__next) {
  @apply bg-white rounded-full shadow-lg p-2;
}

:deep(.carousel__prev:hover),
:deep(.carousel__next:hover) {
  @apply bg-gray-50;
}

.loading {
  @apply flex items-center justify-center min-h-[200px];
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}

:deep(.prose) {
  @apply text-gray-600;
}

:deep(.prose strong) {
  @apply text-gray-900;
}

:deep(.prose h4) {
  @apply text-gray-900 font-semibold;
}
</style> 