<template>
  <div class="recommend-page">
    <div class="recommend-container">
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
            <div class="mt-2 p-4 bg-blue-50 rounded-lg">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="text-sm text-gray-600">
                  <p class="font-medium text-blue-900 mb-1">추천 기준</p>
                  <ul class="list-disc list-inside space-y-1">
                    <li>선택하신 {{ formData.product_type === 'D' ? '예금' : '적금' }} 상품 중에서 선별했어요</li>
                    <li>{{ formData.save_trm }}개월의 저축 기간을 고려했어요</li>
                    <li v-if="formData.monthly_saving">월 {{ formData.monthly_saving }}만원의 저축 금액을 고려했어요</li>
                    <li v-if="formData.additional_requirements">
                      입력하신 "{{ formData.additional_requirements }}" 조건을 반영했어요
                    </li>
                    <li v-if="!formData.additional_requirements">
                      금리가 가장 높은 상품을 우선적으로 추천했어요
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div v-if="loading" class="flex justify-center py-12">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
            <div v-else-if="recommendations.length" class="space-y-4">
              <div v-for="(item, index) in recommendations" :key="index"
                class="bg-white rounded-lg shadow-md p-6 space-y-4">
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-semibold text-lg text-gray-900">{{ item['상품명'] || item.product?.fin_prdt_nm }}</h3>
                    <p class="text-gray-500 mt-1">{{ item['금융사'] || item.product?.kor_co_nm }}</p>
                  </div>
                  <div class="px-3 py-1 bg-blue-50 text-blue-500 rounded-full text-sm font-medium">
                    {{ item.distance ? `유사도: ${(1 - item.distance).toFixed(2)}` : `금리: ${item['금리']}%` }}
                  </div>
                </div>
                <div class="mt-4 grid grid-cols-2 gap-4">
                  <div class="bg-gray-50 p-3 rounded-lg">
                    <span class="text-gray-500 text-sm">상품 유형</span>
                    <div class="font-medium mt-1 text-black">
                      {{ item['금융상품유형'] === 'D' ? '예금' : '적금' }}
                    </div>
                  </div>
                  <div class="bg-gray-50 p-3 rounded-lg">
                    <span class="text-gray-500 text-sm">최고 금리</span>
                    <div class="font-medium mt-1 text-black">{{ item['금리'] }}%</div>
                  </div>
                </div>
                <div class="mt-4 flex justify-end space-x-4">
                  <button
                    @click="openDetailModal(item)"
                    class="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200"
                  >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    자세히 보기
                  </button>
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useModalStore } from '@/stores/modalStore.js'

const steps = ['상품 유형', '저축 기간', '저축 금액', '추가 조건', '추천 결과']
const currentStep = ref(0)
const loading = ref(false)
const recommendations = ref([])
const router = useRouter()
const modalStore = useModalStore()

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

const getToken = () => {
  // 여러 가능한 키에서 토큰을 찾습니다
  const token = localStorage.getItem('access_token') || 
                localStorage.getItem('access') || 
                localStorage.getItem('token')
  if (token) {
    console.log('토큰 확인:', token.substring(0, 10) + '...')  // 토큰의 앞부분만 출력
  }
  return token
}

// axios 기본 설정 추가
axios.defaults.baseURL = 'http://localhost:8000'

const getRecommendations = async () => {
  loading.value = true
  try {
    // const token = getToken()

    // if (!token) {
    //   alert('로그인이 필요한 서비스입니다.')
    //   router.push('/login')
    //   return
    // }

    const params = {
      product_type: formData.value.product_type,
      save_term: formData.value.save_trm,
      query: formData.value.additional_requirements
    }
    
    // 1. 추천 상품 목록 조회
    const recommendResponse = await axios.get('/finrecom/recommend/', {
      params,
      // headers: {
      //   'Authorization': `Bearer ${token}`
      // }
    })

    console.log('추천 API 응답:', recommendResponse.data)

    // 2. 전체 상품 목록 조회
    const productsResponse = await axios.get('/finrecom/', {
      // headers: {
      //   'Authorization': `Bearer ${token}`
      // }
    })

    const allProducts = productsResponse.data.results.prd || []
    console.log('전체 상품 목록:', allProducts)

    // 3. 추천 상품과 전체 상품 매칭하여 상세 정보 결합
    recommendations.value = await Promise.all(recommendResponse.data.map(async (item, index) => {
      console.log('처리 중인 추천 항목:', item)

      // 상품명과 금융사로 매칭되는 상품 찾기
      const matchingProduct = allProducts.find(p => 
        p.fin_prdt_nm === item['상품명'] && 
        p.kor_co_nm === item['금융사']
      )

      console.log('매칭된 전체 상품 정보:', matchingProduct)

      // 금리 정보 구성
      const productRates = matchingProduct?.options || []
      if (productRates.length === 0 && matchingProduct) {
        // options가 없는 경우 기본 금리 정보 생성
        const baseRate = {
          save_trm: formData.value.save_trm,
          intr_rate: item['금리'],
          intr_rate2: item['우대금리'] || item['금리'],
          intr_rate_type: 'S',
          intr_rate_type_nm: '단리'
        }
        productRates.push(baseRate)
      }

      // 저축 기간으로 정렬
      productRates.sort((a, b) => parseInt(a.save_trm) - parseInt(b.save_trm))

      console.log('상품 금리 정보:', productRates)

      // 고유 ID 생성 (실제 상품 ID가 있으면 사용, 없으면 생성)
      const uniqueId = matchingProduct?.id || `${item['금융사']}_${item['상품명']}_${index}`

      // 상품 정보 통합
      const processedItem = {
        ...item,
        id: uniqueId,
        '상품명': item['상품명'],
        '금융사': item['금융사'],
        '금융상품유형': item['금융상품유형'],
        '금리': item['금리'],
        '가입방법': matchingProduct?.join_way || '정보 없음',
        '가입제한': matchingProduct?.join_deny || '정보 없음',
        '가입대상': matchingProduct?.join_member || '정보 없음',
        '부가정보': matchingProduct?.etc_note || '정보 없음',
        // 원본 상품 정보도 저장 (전체 정보를 그대로 유지하고 options 추가)
        originalProduct: matchingProduct ? {
          ...matchingProduct,
          options: productRates
        } : null
      }

      console.log('처리된 추천 항목:', processedItem)
      return processedItem
    }))

    console.log('최종 추천 목록:', recommendations.value)

  } catch (error) {
    console.error('추천 상품 조회 실패:', error)
    console.log('에러 상세:', error.response?.data)
    if (error.response?.status === 401) {
      alert('인증이 만료되었습니다. 다시 로그인해주세요.')
      router.push('/login')
    } else {
      alert('추천 상품을 불러오는데 실패했습니다. 잠시 후 다시 시도해주세요.')
    }
  } finally {
    loading.value = false
  }
}

const openDetailModal = async (item) => {
  try {
    console.log('모달에 전달할 상품 데이터:', item.originalProduct)

    // 상품 ID 확인
    const productId = item.originalProduct?.id || item.id
    if (!productId) {
      console.error('상품 ID를 찾을 수 없습니다:', item)
      throw new Error('상품 ID가 없습니다.')
    }

    // 금리 정보 중복 제거 (save_trm 기준)
    const uniqueOptions = []
    const seenTerms = new Set()
    
    // 먼저 options를 금리 기준으로 정렬 (높은 금리가 먼저 오도록)
    const sortedOptions = [...(item.originalProduct?.options || [])].sort((a, b) => {
      const rateA = parseFloat(a.intr_rate2) || parseFloat(a.intr_rate) || 0
      const rateB = parseFloat(b.intr_rate2) || parseFloat(b.intr_rate) || 0
      return rateB - rateA
    })

    // 정렬된 options에서 각 save_trm당 가장 높은 금리만 선택
    sortedOptions.forEach(option => {
      if (!seenTerms.has(option.save_trm)) {
        seenTerms.add(option.save_trm)
        uniqueOptions.push(option)
      }
    })

    // 기간순으로 재정렬
    uniqueOptions.sort((a, b) => parseInt(a.save_trm) - parseInt(b.save_trm))

    // 상품 데이터 구성 - 원본 데이터를 최대한 활용
    const product = {
      ...item.originalProduct,
      id: productId,
      fin_prdt_nm: item['상품명'],
      kor_co_nm: item['금융사'],
      prd_type: item['금융상품유형'],
      options: uniqueOptions  // 중복이 제거된 금리 정보 사용
    }

    console.log('모달에 최종 전달되는 상품 데이터:', product)

    // 모달 열기
    modalStore.openProductDetailModal(product, {
      onBookmarkUpdated: () => {
        getRecommendations()
      }
    })
  } catch (error) {
    console.error('상품 상세 정보 처리 실패:', error)
    alert('상품 정보를 불러오는데 실패했습니다.')
  }
}

// 컴포넌트 마운트 시 토큰 확인
onMounted(() => {
  const token = getToken()
  if (!token) {
    console.warn('토큰이 없습니다!')
  }
})

// axios 인터셉터 추가
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.log('401 에러 발생. 요청 헤더:', error.config?.headers)
    }
    return Promise.reject(error)
  }
)
</script>

<style scoped>
.recommend-page {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem; /* 헤더 높이만큼 위로 올림 */
  padding-top: 5rem; /* 헤더 영역만큼 패딩 추가 */
}

.recommend-container {
  @apply max-w-6xl mx-auto px-4 py-8;
}
</style> 