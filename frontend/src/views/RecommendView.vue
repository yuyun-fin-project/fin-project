<template>
  <div class="recommend-view min-h-screen bg-gradient-to-b from-blue-50 to-white">
    <div class="max-w-4xl mx-auto px-4 py-12">
      <div
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="200"
      >
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl md:text-4xl font-bold text-gray-900">
            맞춤 금융상품 추천
          </h1>
        </div>

        <!-- 단계별 진행 표시 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-8">
          <div class="flex items-center justify-between">
            <div v-for="(step, index) in steps" :key="index"
              class="flex items-center flex-1">
              <div class="flex flex-col items-center flex-1">
                <div :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center mb-3 transition-all duration-300',
                  currentStep > index ? 'bg-blue-500 text-white shadow-md' : 
                  currentStep === index ? 'bg-blue-100 text-blue-500 border-2 border-blue-500 scale-110' :
                  'bg-gray-100 text-gray-500'
                ]">
                  {{ index + 1 }}
                </div>
                <div class="text-sm font-medium text-center whitespace-nowrap"
                  :class="currentStep === index ? 'text-blue-500' : 'text-gray-500'">
                  {{ step }}
                </div>
              </div>
              <div v-if="index < steps.length - 1" class="w-full h-1 mx-2 mt-[-20px]"
                :class="currentStep > index ? 'bg-blue-500' : 'bg-gray-200'"></div>
            </div>
          </div>
        </div>

        <!-- 단계별 컨텐츠 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <!-- 상품 유형 선택 -->
          <div v-if="currentStep === 0" 
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900">원하시는 금융상품 유형을 선택해주세요</h2>
            <div class="grid grid-cols-2 gap-6">
              <button v-for="type in productTypes" :key="type.value"
                @click="selectProductType(type.value)"
                :class="[
                  'p-6 rounded-xl text-black border-2 text-center transition-all duration-300 hover:shadow-md',
                  formData.product_type === type.value ? 
                  'border-blue-500 bg-blue-50 shadow-md scale-[1.02]' : 
                  'border-gray-200 hover:border-blue-200'
                ]">
                <div class="text-3xl mb-3">{{ type.icon }}</div>
                <div class="font-semibold text-lg mb-2">{{ type.label }}</div>
                <div class="text-sm text-gray-500">{{ type.description }}</div>
              </button>
            </div>
          </div>

          <!-- 저축 기간 선택 -->
          <div v-if="currentStep === 1"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900">저축 기간을 선택해주세요</h2>
            <div class="bg-gray-50 rounded-xl p-6 space-y-6">
              <div class="flex items-center space-x-4">
                <input type="range" v-model="formData.save_trm" 
                  min="6" max="36" step="6"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                <span class="text-lg font-semibold text-blue-500 w-24 text-right">
                  {{ formData.save_trm }}개월
                </span>
              </div>
              <div class="flex justify-between text-sm text-gray-500 font-medium">
                <span>6개월</span>
                <span>36개월</span>
              </div>
            </div>
          </div>

          <!-- 월 저축 가능액 입력 -->
          <div v-if="currentStep === 2"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900">월 저축 가능액을 입력해주세요</h2>
            <div class="bg-gray-50 rounded-xl p-6 space-y-6">
              <div class="relative">
                <input type="number" v-model="formData.monthly_saving"
                  class="w-full px-4 pr-16 py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none text-lg"
                  placeholder="금액을 입력해주세요"
                  min="0" step="10000">
                <span class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">만원</span>
              </div>
              <div class="flex flex-wrap gap-3">
                <button v-for="amount in quickAmounts" :key="amount"
                  @click="formData.monthly_saving = amount"
                  class="px-5 py-2.5 text-sm font-medium border rounded-lg hover:bg-gray-50 bg-white transition-all duration-200"
                  :class="formData.monthly_saving === amount ? 'border-blue-500 text-blue-500 bg-blue-50' : 'border-gray-300 text-gray-700'">
                  {{ amount }}만원
                </button>
              </div>
            </div>
          </div>

          <!-- 추가 조건 입력 -->
          <div v-if="currentStep === 3"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900">원하시는 추가 조건이 있다면 입력해주세요</h2>
            <div class="bg-gray-50 rounded-xl p-6 space-y-4">
              <textarea
                v-model="formData.additional_requirements"
                rows="4"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 resize-none"
                placeholder="예시) 온라인 가입이 가능한 상품 위주로 추천해주세요.&#10;중도해지 수수료가 낮은 상품을 선호합니다.&#10;자동이체 기능이 있는 상품이면 좋겠어요."
              ></textarea>
              <div class="flex items-center text-sm text-gray-500 bg-blue-50 p-4 rounded-lg">
                <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                추가 조건은 선택사항입니다. 입력하지 않아도 기본 조건으로 추천해드립니다.
              </div>
            </div>
          </div>

          <!-- 추천 결과 -->
          <div v-if="currentStep === 4"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900">추천 금융상품</h2>
            <div v-if="loading" class="flex justify-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
            <div v-else-if="recommendations.length" class="space-y-4">
              <div v-for="(item, index) in recommendations" :key="index"
                class="p-6 border border-gray-200 rounded-xl hover:shadow-lg transition-all duration-300">
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-semibold text-lg text-gray-900">{{ item.product.fin_prdt_nm }}</h3>
                    <p class="text-gray-500 mt-1">{{ item.product.kor_co_nm }}</p>
                  </div>
                  <div class="px-3 py-1 bg-blue-50 text-blue-500 rounded-full text-sm font-medium">
                    유사도: {{ (1 - item.distance).toFixed(2) }}
                  </div>
                </div>
                <div class="mt-4 grid grid-cols-2 gap-4">
                  <div class="bg-gray-50 p-3 rounded-lg">
                    <span class="text-gray-500 text-sm">가입 기간</span>
                    <div class="font-medium mt-1">{{ item.product.options[0]?.save_trm }}개월</div>
                  </div>
                  <div class="bg-gray-50 p-3 rounded-lg">
                    <span class="text-gray-500 text-sm">최고 금리</span>
                    <div class="font-medium mt-1">{{ item.product.options[0]?.intr_rate2 }}%</div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 text-gray-500">
              추천할 수 있는 상품이 없습니다.
            </div>
          </div>

          <!-- 네비게이션 버튼 -->
          <div class="mt-8 flex justify-between">
            <button v-if="currentStep > 0" 
              @click="currentStep--"
              class="px-6 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 bg-white text-gray-700 font-medium transition-colors duration-200">
              이전
            </button>
            <div v-else class="w-[88px]"></div>
            <button v-if="currentStep < 4" 
              @click="nextStep"
              :disabled="!canProceed"
              :class="[
                'px-6 py-2.5 rounded-lg font-medium transition-all duration-200',
                canProceed ? 'bg-blue-500 text-white hover:bg-blue-600 transform hover:scale-[1.02]' : 'bg-gray-200 text-gray-500 cursor-not-allowed'
              ]">
              {{ currentStep === 3 ? '추천받기' : '다음' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const steps = ['상품 유형', '저축 기간', '저축 금액', '추가 조건', '추천 결과']
const currentStep = ref(0)
const loading = ref(false)
const recommendations = ref([])

const productTypes = [
  {
    value: 'D',
    label: '예금',
    icon: '💰',
    description: '목돈을 한번에 맡기고 이자를 받아요'
  },
  {
    value: 'S',
    label: '적금',
    icon: '🏦',
    description: '매월 일정액을 저축하고 이자를 받아요'
  }
]

const quickAmounts = [10, 30, 50, 100]

const formData = ref({
  product_type: '',
  save_trm: 12,
  monthly_saving: 50,
  additional_requirements: ''
})

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return !!formData.value.product_type
    case 1:
      return true
    case 2:
      return formData.value.monthly_saving > 0
    case 3:
      return true
    default:
      return false
  }
})

const selectProductType = (type) => {
  formData.value.product_type = type
}

const nextStep = async () => {
  if (currentStep.value === 3) {
    await getRecommendations()
  }
  currentStep.value++
}

const getRecommendations = async () => {
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/api/recommend/', formData.value)
    recommendations.value = response.data
  } catch (error) {
    console.error('추천 상품 조회 실패:', error)
  } finally {
    loading.value = false
  }
}
</script> 