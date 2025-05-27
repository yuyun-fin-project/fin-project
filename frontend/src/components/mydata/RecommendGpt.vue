<template>
  <div class="bg-white rounded-xl shadow-sm p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl text-black font-semibold">AI 금융 분석</h2>
      <button 
        @click="analyzeData" 
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        :disabled="isLoading"
      >
        {{ isLoading ? '분석 중...' : '분석하기' }}
      </button>
    </div>

    <!-- 소득 입력 폼 -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        월 소득
      </label>
      <div class="flex gap-2">
        <input
          v-model="income"
          type="number"
          class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          placeholder="월 소득을 입력하세요"
        />
        <span class="inline-flex items-center text-gray-500">원</span>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex justify-center items-center h-32">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 상태 -->
    <div v-else-if="error" class="bg-red-50 p-4 rounded-lg">
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- 분석 결과 -->
    <div v-else-if="recommendation" class="space-y-6">
      <!-- 주요 지표 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-blue-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-600">현재 소비</h3>
          <p class="text-2xl font-bold text-blue-600">{{ recommendation.current_spending }}</p>
        </div>
        <div class="bg-blue-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-600">절감 가능 금액</h3>
          <p class="text-2xl font-bold text-green-600">{{ recommendation.possible_reduction }}</p>
        </div>
      </div>

      <!-- 상세 분석 -->
      <div class="space-y-4">
        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">소득 대비 소비율</h3>
          <p>{{ recommendation.income_spending_ratio }}</p>
        </div>

        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">불필요한 지출 항목</h3>
          <ul class="list-disc list-inside space-y-1">
            <li v-for="item in recommendation.unnecessary_items" :key="item" class="text-gray-600">
              {{ item }}
            </li>
          </ul>
        </div>

        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">비상금 저축 조언</h3>
          <p>{{ recommendation.emergency_saving_advice }}</p>
        </div>

        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">카드 사용 패턴</h3>
          <p>{{ recommendation.card_spending_focus }}</p>
        </div>

        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">지출 추이</h3>
          <p>{{ recommendation.spending_trend }}</p>
        </div>

        <div class="border-b pb-4">
          <h3 class="font-medium mb-2">정기 결제 서비스 점검</h3>
          <p>{{ recommendation.subscription_check }}</p>
        </div>

        <div>
          <h3 class="font-medium mb-2">종합 추천</h3>
          <p class="text-gray-800 whitespace-pre-line">{{ recommendation.recommendation }}</p>
        </div>
      </div>
    </div>

    <!-- 초기 상태 -->
    <div v-else class="text-center text-gray-500 py-8">
      소득을 입력하고 분석하기 버튼을 눌러주세요.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  cardData: {
    type: Object,
    required: true
  }
})


const emit = defineEmits(['update-recommendation'])

const income = ref('')
const isLoading = ref(false)
const error = ref(null)
const recommendation = ref(null)

// API 기본 설정
const API_BASE_URL = 'http://localhost:8000'


// 데이터 분석
const analyzeData = async () => {
  if (!income.value) {
    error.value = '월 소득을 입력해주세요.'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await axios.post(
      `${API_BASE_URL}/mydata/ai/`,
      {
        income: Number(income.value)
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    )

    recommendation.value = response.data.recommendation
    emit('update-recommendation', response.data.recommendation)
  } catch (err) {
    error.value = '분석에 실패했습니다. 다시 시도해주세요.'
    console.error('AI 분석 실패:', err)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
input[type="number"] {
  @apply px-4 py-2;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>