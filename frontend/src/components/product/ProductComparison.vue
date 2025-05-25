<template>
  <div class="w-full">

    <!-- 로딩 상태 -->
    <div v-if="props.isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="props.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-8">
      {{ props.error }}
    </div>

    <!-- 상품 목록 -->
    <div v-else class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 tracking-wider">공시 제출월</th>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 tracking-wider">금융회사명</th>
            <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 tracking-wider">상품명</th>
            <th 
              v-for="period in periods" 
              :key="period"
              @click="sortByPeriod(period)"
              class="px-4 py-3 text-left text-xs font-medium text-gray-500 tracking-wider cursor-pointer hover:bg-gray-100"
            >
              {{ period }}개월
              <div class="text-xs text-gray-400">
                (Click to sort {{ sortDirection === 'asc' ? 'ascending' : 'descending' }})
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="product in sortedProducts" :key="product.fin_prdt_cd" @click="openDetail(product)" 
              class="hover:bg-gray-50 cursor-pointer transition-colors duration-150">
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{{ formatDate(product.fin_co_subm_day) }}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{{ product.kor_co_nm }}</td>
            <td class="px-4 py-3 text-sm text-gray-900">
              <div>{{ product.fin_prdt_nm }}</div>
              <div class="text-xs text-gray-500">{{ product.prd_type === 'D' ? '예금' : '적금' }}</div>
            </td>
            <td 
              v-for="period in periods" 
              :key="period"
              class="px-4 py-3 whitespace-nowrap"
            >
              <template v-if="getOptionForPeriod(product, period)">
                <div class="text-sm">
                  <span class="font-medium" :class="getInterestRateColor(getBaseRate(product, period))">
                    {{ getBaseRate(product, period) }}%
                  </span>
                  <template v-if="hasPreferentialRate(product, period)">
                    <span class="text-xs text-gray-500 ml-1">
                      최대 
                      <span :class="getInterestRateColor(getMaxRate(product, period))">
                        {{ getMaxRate(product, period) }}%
                      </span>
                    </span>
                  </template>
                </div>
                <div class="text-xs text-gray-500">
                  {{ getInterestRateType(product, period) }}
                </div>
              </template>
              <template v-else>
                <span class="text-gray-400">-</span>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 상품 상세 모달 -->
    <ProductDetailModal
      v-if="showModal"
      :show="showModal"
      :product="selectedProduct"
      :is-authenticated="props.isAuthenticated"
      @close="closeModal"
      @bookmark-updated="handleBookmarkUpdated"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useFinanceStore } from '../../stores/finance.js'
import axios from 'axios'
import ProductDetailModal from './ProductDetailModal.vue'

// axios 기본 설정
axios.defaults.withCredentials = true // 모든 요청에 쿠키 포함
axios.defaults.headers.common['X-CSRFToken'] = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''

const props = defineProps({
  maxItems: {
    type: Number,
    default: Infinity
  },
  showFilters: {
    type: Boolean,
    default: true
  },
  initialProducts: {
    type: Array,
    default: () => []
  },
  isSearching: {
    type: Boolean,
    default: false
  },
  products: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  isAuthenticated: {
    type: Boolean,
    default: false
  },
  selectedBank: {
    type: String,
    default: ''
  },
  selectedType: {
    type: String,
    default: 'all'
  },
  selectedPeriod: {
    type: String,
    default: ''
  },
  sortBy: {
    type: String,
    default: 'rate'
  }
})

const financeStore = useFinanceStore()
const selectedBank = ref('')
const selectedPeriod = ref('')
const selectedType = ref('all')
const sortBy = ref('rate')
const products = ref([])
const showModal = ref(false)
const selectedProduct = ref(null)
const bookmarkedProducts = ref([])
const currentUserId = ref(null)

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

// 상품 데이터 가져오기
const fetchProducts = async () => {
  try {
    const response = await axios.get('/finrecom/')
    console.log('금융상품 응답:', response.data)

    if (response.data && response.data.results) {
      const prdList = response.data.results.prd || []
      const optList = response.data.results.opt || []

      // 상품별 옵션 매핑
      products.value = prdList.map(prd => {
        const productOptions = optList.filter(opt => opt.fin_prdt_cd === prd.fin_prdt_cd)
        console.log('Product options for', prd.fin_prdt_cd, ':', productOptions)
        
        return {
          ...prd,
          options: productOptions.map(opt => ({
            ...opt,
            save_trm: opt.save_trm ? parseInt(opt.save_trm) : null,
            intr_rate: opt.intr_rate ? parseFloat(opt.intr_rate) : null,
            intr_rate2: opt.intr_rate2 ? parseFloat(opt.intr_rate2) : null
          }))
        }
      })

      console.log('변환된 상품 데이터:', products.value)
    }
  } catch (err) {
    console.error('금융상품 데이터 가져오기 실패:', err)
    props.error = '금융상품 데이터를 가져오는데 실패했습니다.'
  }
}

// 인증 상태 확인
const checkAuthStatus = async () => {
  try {
    // 먼저 현재 사용자의 access token이 유효한지 확인
    const accessToken = localStorage.getItem('access_token')
    console.log('저장된 액세스 토큰:', accessToken)

    if (!accessToken) {
      console.log('액세스 토큰이 없습니다.')
      props.isAuthenticated = false
      return false
    }

    // Authorization 헤더 설정
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`

    // 사용자 정보를 가져오는 API 호출
    const response = await axios.get('/accounts/profile/1/', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })
    console.log('인증 상태 확인 응답:', response.data)
    
    if (response.data) {
      currentUserId.value = response.data.id
      props.isAuthenticated = true
      console.log('인증 성공 - 현재 사용자 ID:', currentUserId.value)
      return true
    }
    
    console.log('사용자 정보가 없습니다.')
    props.isAuthenticated = false
    return false
  } catch (error) {
    console.error('인증 상태 확인 실패:', error)
    console.error('에러 상세:', error.response?.data)
    
    if (error.response?.status === 401 || error.response?.status === 404) {
      props.isAuthenticated = false
      bookmarkedProducts.value = []
      // 토큰이 만료되었을 수 있으므로 리프레시 토큰으로 새로운 액세스 토큰 요청
      try {
        const refreshResponse = await axios.post('/accounts/api/token/refresh/')
        console.log('토큰 갱신 응답:', refreshResponse.data)
        
        if (refreshResponse.data?.access) {
          localStorage.setItem('access_token', refreshResponse.data.access)
          console.log('토큰 갱신 성공 - 새 토큰:', refreshResponse.data.access)
          // 새로운 토큰으로 다시 시도
          return await checkAuthStatus()
        }
      } catch (refreshError) {
        console.error('토큰 갱신 실패:', refreshError)
        console.error('갱신 에러 상세:', refreshError.response?.data)
        // 리프레시 토큰도 만료된 경우 로그아웃 처리
        localStorage.removeItem('access_token')
      }
    }
    return false
  }
}

// 북마크된 상품 목록 가져오기
const fetchBookmarks = async () => {
  if (!props.isAuthenticated) {
    console.log('사용자가 로그인하지 않았습니다.')
    return
  }

  try {
    const accessToken = localStorage.getItem('access_token')
    if (!accessToken) {
      console.log('액세스 토큰이 없습니다.')
      return
    }

    const response = await axios.get('/finrecom/bookmark/product/', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })
    
    bookmarkedProducts.value = response.data
  } catch (error) {
    console.error('북마크 목록 로드 실패:', error)
    if (error.response?.status === 401) {
      emit('auth-error')
      return
    }
  }
}

// 북마크 상태 확인
const isBookmarked = (productId) => {
  return props.isAuthenticated && bookmarkedProducts.value.some(item => item.product_id === productId)
}

// 북마크 토글
const toggleBookmark = async (productId) => {
  if (!props.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const accessToken = localStorage.getItem('access_token')
    if (!accessToken) {
      console.log('액세스 토큰이 없습니다.')
      return
    }

    const isBookmarked = bookmarkedProducts.value.some(item => item.product_id === productId)
    
    if (isBookmarked) {
      await axios.delete(`/finrecom/bookmark/product/${productId}/`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })
      bookmarkedProducts.value = bookmarkedProducts.value.filter(item => item.product_id !== productId)
    } else {
      const response = await axios.post('/finrecom/bookmark/product/', 
        { product_id: productId },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      bookmarkedProducts.value.push(response.data)
    }
    
    emit('bookmark-updated')
  } catch (error) {
    console.error('북마크 처리 실패:', error)
    if (error.response?.status === 401) {
      emit('auth-error')
    }
  }
}

// 모달 관련 함수들
const openProductDetail = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}

const handleBookmarkUpdated = async () => {
  await fetchBookmarks()
}

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  if (!Array.isArray(props.products)) return []

  return props.products.filter(product => {
    if (!product) return false

    // 은행명 필터
    const bankMatch = !props.selectedBank || product.kor_co_nm.includes(props.selectedBank)

    // 상품 유형 필터
    const typeMatch = props.selectedType === 'all' || product.prd_type === props.selectedType

    // 가입기간 필터
    const periodMatch = !props.selectedPeriod || product.options?.some(opt => 
      opt?.save_trm === parseInt(props.selectedPeriod)
    )

    return bankMatch && typeMatch && periodMatch
  })
})

// 정렬된 상품 목록
const sortedProducts = computed(() => {
  if (!Array.isArray(filteredProducts.value)) return []

  return [...filteredProducts.value].sort((a, b) => {
    if (!a || !b) return 0

    if (currentSortPeriod.value) {
      const aOption = getOptionForPeriod(a, currentSortPeriod.value)
      const bOption = getOptionForPeriod(b, currentSortPeriod.value)

      const aRate = aOption ? (sortDirection.value === 'asc' ? aOption.intr_rate : aOption.intr_rate2) || 0 : 0
      const bRate = bOption ? (sortDirection.value === 'asc' ? bOption.intr_rate : bOption.intr_rate2) || 0 : 0

      return sortDirection.value === 'asc' ? aRate - bRate : bRate - aRate
    }

    return a.kor_co_nm.localeCompare(b.kor_co_nm)
  })
})

// 특정 기간에 대한 옵션 찾기
const getOptionForPeriod = (product, period) => {
  if (!product?.options?.length) {
    return null
  }

  return product.options.find(opt => opt?.save_trm === period)
}

// 특정 기간에 대한 기본 금리 반환
const getBaseRate = (product, period) => {
  const option = getOptionForPeriod(product, period)
  if (!option?.intr_rate) return '-'
  return option.intr_rate.toFixed(2)
}

// 특정 기간에 대한 최대 금리 반환
const getMaxRate = (product, period) => {
  const option = getOptionForPeriod(product, period)
  if (!option) return '-'

  const baseRate = option.intr_rate || 0
  const preferentialRate = option.intr_rate2 || 0
  const maxRate = Math.max(baseRate, preferentialRate)

  return maxRate.toFixed(2)
}

// 우대금리 여부 확인
const hasPreferentialRate = (product, period) => {
  const option = getOptionForPeriod(product, period)
  if (!option) return false

  return (option.intr_rate2 || 0) > (option.intr_rate || 0)
}

// 금리 유형 반환
const getInterestRateType = (product, period) => {
  const option = getOptionForPeriod(product, period)
  if (!option) return ''

  let type = option.intr_rate_type_nm || ''
  if (option.rsrv_type_nm) {
    type += ` / ${option.rsrv_type_nm}`
  }
  return type
}

// 금리에 따른 색상 반환
const getInterestRateColor = (rate) => {
  if (!rate || rate === '-') return 'text-gray-500'
  const numRate = parseFloat(rate)
  if (numRate >= 5) return 'text-red-600'
  if (numRate >= 4) return 'text-orange-600'
  if (numRate >= 3) return 'text-blue-600'
  return 'text-gray-900'
}

// 날짜 포맷팅
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const year = dateStr.substring(0, 4)
  const month = dateStr.substring(4, 6)
  return `${year}.${month}`
}

// 가입 방법 포맷팅
const formatJoinWay = (joinWay) => {
  if (!joinWay) return '-'
  return joinWay.split(',').map(way => way.trim()).join(', ')
}

// 가입 대상 포맷팅
const formatJoinMember = (joinMember) => {
  if (!joinMember) return '-'
  return joinMember.replace(/\n/g, ', ')
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  console.log('컴포넌트 마운트 - 데이터 로드 시작')
  const authStatus = await checkAuthStatus()
  console.log('인증 상태:', authStatus)
  await fetchProducts()
  if (authStatus) {
    await fetchBookmarks()
  }
  console.log('컴포넌트 마운트 - 데이터 로드 완료')
})

// 인증 상태 변경 감시
watch(() => props.isAuthenticated, async (newValue) => {
  if (newValue) {
    await fetchBookmarks()
  } else {
    bookmarkedProducts.value = []
  }
})

const periods = [6, 12, 24, 36]
const currentSortPeriod = ref(null)
const sortDirection = ref('asc')

// 정렬 함수
const sortByPeriod = (period) => {
  if (currentSortPeriod.value === period) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    currentSortPeriod.value = period
    sortDirection.value = 'asc'
  }
  console.log('Sorting by period:', period, 'direction:', sortDirection.value)
}

const openDetail = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

// 컴포넌트 마운트 시 데이터 감시
watch(() => props.products, (newProducts) => {
  console.log('Products updated:', newProducts)
}, { immediate: true })
</script>

<style scoped>
.table-container {
  @apply overflow-x-auto shadow-md rounded-lg;
}

th {
  @apply bg-gray-50 px-4 py-3 text-left text-xs font-medium text-gray-500 tracking-wider;
}

td {
  @apply px-4 py-3 text-sm;
}

tr:nth-child(even) {
  @apply bg-gray-50;
}

tr:hover {
  @apply bg-gray-100 transition-colors duration-150;
}

.interest-rate {
  @apply font-medium;
}
</style> 