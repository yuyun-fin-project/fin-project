<template>
  <div class="ai-view">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      class="max-w-6xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        AI 금융상품 추천
      </h1>

      <!-- 상품 유형 선택 -->
      <div class="mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            v-for="type in productTypes"
            :key="type.value"
            @click="selectProductType(type.value)"
            :class="[
              'p-4 rounded-xl text-center transition-all transform hover:scale-105',
              selectedType === type.value
                ? 'bg-blue-500 text-white shadow-lg'
                : 'bg-white text-gray-700 border border-gray-200 hover:border-blue-500'
            ]"
          >
            <div class="text-2xl mb-2">{{ type.icon }}</div>
            <h3 class="font-medium">{{ type.name }}</h3>
            <p class="text-sm opacity-80">{{ type.description }}</p>
          </button>
        </div>
      </div>

      <!-- 추천 결과 -->
      <div class="space-y-6">
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p class="text-gray-600">AI가 최적의 금융상품을 찾고 있습니다...</p>
        </div>

        <div v-else-if="error" class="bg-red-50 text-red-600 p-4 rounded-lg">
          <p>{{ error }}</p>
          <button
            @click="fetchRecommendations"
            class="mt-2 text-sm underline hover:no-underline"
          >
            다시 시도
          </button>
        </div>

        <template v-else>
          <div
            v-for="(product, index) in recommendations"
            :key="index"
            v-motion
            :initial="{ opacity: 0, x: 20 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="index * 100"
            class="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100"
          >
            <div class="flex items-start justify-between">
              <div>
                <h3 class="text-xl font-semibold text-gray-900">{{ product.상품명 }}</h3>
                <p class="text-gray-600 mt-1">{{ product.금융사 }}</p>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-blue-600">
                  {{ formatRate(product.금리) }}%
                </div>
                <div class="text-sm text-gray-500">금리</div>
              </div>
            </div>
            
            <div class="mt-4 pt-4 border-t border-gray-100">
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">상품 유형</span>
                <span class="font-medium text-gray-900">
                  {{ getProductTypeName(product.금융상품유형) }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="recommendations.length === 0" class="text-center py-8 bg-gray-50 rounded-xl">
            <svg
              class="w-16 h-16 text-gray-400 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p class="text-gray-600">
              죄송합니다. 현재 추천할 수 있는 상품이 없습니다.
            </p>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { recommendService } from '@/services/recommendService'

const auth = useAuthStore()
const router = useRouter()

const productTypes = [
  {
    value: 'D',
    name: '예금',
    icon: '💰',
    description: '안정적인 수익을 원하시나요?'
  },
  {
    value: 'S',
    name: '적금',
    icon: '🏦',
    description: '목돈 마련이 목표인가요?'
  },
  {
    value: 'F',
    name: '펀드',
    icon: '📈',
    description: '높은 수익을 추구하시나요?'
  }
]

const selectedType = ref('D')
const recommendations = ref([])
const loading = ref(false)
const error = ref(null)

// 상품 유형 선택
const selectProductType = async (type) => {
  selectedType.value = type
  await fetchRecommendations()
}

// 추천 상품 조회
const fetchRecommendations = async () => {
  if (!auth.isAuthenticated) {
    router.push({
      name: 'Login',
      query: { redirect: router.currentRoute.value.fullPath }
    })
    return
  }

  loading.value = true
  error.value = null

  try {
    const data = await recommendService.getRecommendations(selectedType.value)
    recommendations.value = data
  } catch (err) {
    error.value = '추천 상품을 불러오는데 실패했습니다. 잠시 후 다시 시도해주세요.'
    console.error('추천 상품 조회 실패:', err)
  } finally {
    loading.value = false
  }
}

// 금리 포맷
const formatRate = (rate) => {
  return Number(rate).toFixed(2)
}

// 상품 유형 이름 가져오기
const getProductTypeName = (type) => {
  const productType = productTypes.find(t => t.value === type)
  return productType ? productType.name : type
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
.ai-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}
</style>
