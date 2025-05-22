<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">금융상품 금리 비교</h1>
    
    <!-- 상품 유형 선택 -->
    <div class="mb-8">
      <div class="flex space-x-4">
        <button 
          @click="selectProductType('deposit')"
          :class="[
            'px-6 py-2 rounded-lg font-medium',
            productType === 'deposit' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          정기예금
        </button>
        <button 
          @click="selectProductType('saving')"
          :class="[
            'px-6 py-2 rounded-lg font-medium',
            productType === 'saving' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          적금
        </button>
      </div>
    </div>

    <!-- 필터 옵션 -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">은행명</label>
          <input
            v-model="filters.bankName"
            type="text"
            placeholder="은행명으로 검색"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">최소 금리</label>
          <input
            v-model.number="filters.minRate"
            type="number"
            step="0.1"
            placeholder="최소 금리 입력"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">가입기간 (개월)</label>
          <select
            v-model="filters.period"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-8">
      {{ error }}
    </div>

    <!-- 상품 목록 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="product in filteredProducts"
        :key="product.fin_prdt_cd"
        class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
      >
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ product.fin_prdt_nm }}</h3>
            <p class="text-sm text-gray-600">{{ product.kor_co_nm }}</p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-bold text-blue-600">{{ product.intr_rate2 }}%</p>
            <p class="text-sm text-gray-500">기본금리 {{ product.intr_rate }}%</p>
          </div>
        </div>
        
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">가입기간</span>
            <span class="font-medium">{{ product.save_trm }}개월</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">최소가입금액</span>
            <span class="font-medium">{{ formatAmount(product.spcl_cnd) }}원</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">가입방법</span>
            <span class="font-medium">{{ product.join_way }}</span>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t">
          <a
            :href="product.homp_url"
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center justify-center"
          >
            상품 가입하기
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const productType = ref('deposit')
const products = ref([])
const isLoading = ref(false)
const error = ref(null)

const filters = ref({
  bankName: '',
  minRate: null,
  period: ''
})

const API_KEY = '7bff34b9cf6a77455782dcda23d2cccd' // 하드코딩된 API 키 사용
const API_BASE_URL = 'http://localhost:4000'

// 상품 목록 필터링
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const bankMatch = !filters.value.bankName || 
      product.kor_co_nm.toLowerCase().includes(filters.value.bankName.toLowerCase())
    
    const rateMatch = !filters.value.minRate || 
      parseFloat(product.intr_rate2 || product.intr_rate) >= filters.value.minRate
    
    const periodMatch = !filters.value.period || 
      product.save_trm === filters.value.period
    
    return bankMatch && rateMatch && periodMatch
  })
})

// 금액 포맷팅
const formatAmount = (amount) => {
  const num = parseInt(amount.replace(/[^0-9]/g, ''))
  return isNaN(num) ? '0' : num.toLocaleString('ko-KR')
}

// 상품 유형 선택
const selectProductType = async (type) => {
  productType.value = type
  await fetchProducts()
}

// 상품 데이터 가져오기
const fetchProducts = async () => {
  isLoading.value = true
  error.value = null
  products.value = []
  
  try {
    console.log('[요청] 상품 유형:', productType.value)
    
    const response = await axios.get(`${API_BASE_URL}/api/products/${productType.value}`, {
      params: {
        apiKey: API_KEY
      }
    })

    if (response.data.status === 'success') {
      const { baseList, optionList } = response.data.data

      // 상품 데이터 가공
      products.value = baseList.map(item => {
        // 해당 상품의 옵션 목록 찾기
        const productOptions = optionList.filter(opt => opt.fin_prdt_cd === item.fin_prdt_cd)
        
        // 최고 우대금리 계산
        let maxRate = parseFloat(item.intr_rate) || 0
        if (productOptions.length > 0) {
          const optionRates = productOptions.map(opt => {
            const rate2 = parseFloat(opt.intr_rate2) || 0
            const rate = parseFloat(opt.intr_rate) || 0
            return Math.max(rate2, rate)
          })
          maxRate = Math.max(...optionRates, maxRate)
        }

        return {
          ...item,
          intr_rate: parseFloat(item.intr_rate || '0').toFixed(2),
          intr_rate2: maxRate.toFixed(2),
          save_trm: item.save_trm || '0',
          spcl_cnd: item.spcl_cnd || '0'
        }
      })

      // 금리 내림차순 정렬
      products.value.sort((a, b) => parseFloat(b.intr_rate2) - parseFloat(a.intr_rate2))
    } else {
      throw new Error(response.data.message || '데이터를 불러오는데 실패했습니다.')
    }
  } catch (err) {
    console.error('상품 데이터 조회 실패:', err)
    error.value = err.message || '상품 데이터를 불러오는데 실패했습니다. 잠시 후 다시 시도해주세요.'
  } finally {
    isLoading.value = false
  }
}

// 컴포넌트 마운트 시 상품 데이터 로드
onMounted(fetchProducts)

// 필터 변경 감지
watch(filters, () => {
  console.log('필터 변경:', filters.value)
}, { deep: true })
</script> 