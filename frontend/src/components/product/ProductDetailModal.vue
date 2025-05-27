<template>
  <div v-if="show" class="fixed inset-0 z-[1001] overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- 배경 오버레이 -->
      <div class="fixed inset-0 transition-opacity" @click="closeModal">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <!-- 모달 -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <!-- 헤더 -->
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-2xl font-bold text-gray-900">{{ product.fin_prdt_nm }}</h3>
              <p class="mt-1 text-lg text-gray-600">{{ product.kor_co_nm }}</p>
            </div>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 상품 정보 -->
          <div class="space-y-6">
            <!-- 기본 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-lg font-semibold text-gray-900 mb-3">기본 정보</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-500">상품 종류</p>
                  <p class="text-base text-gray-900">{{ product.prd_type === 'D' ? '예금' : '적금' }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">가입 방법</p>
                  <p class="text-base text-gray-900">{{ product.join_way }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">가입 대상</p>
                  <p class="text-base text-gray-900">{{ product.join_member }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">가입 제한</p>
                  <p class="text-base text-gray-900">{{ product.join_deny ? product.join_deny : '제한 없음' }}</p>
                </div>
              </div>
            </div>

            <!-- 금리 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-lg font-semibold text-gray-900 mb-3">금리 정보</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-100">
                    <tr>
                      <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">가입 기간</th>
                      <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">기본 금리</th>
                      <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">우대 금리</th>
                      <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">적립 유형</th>
                      <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">이자 지급 방식</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="option in uniqueOptions" :key="getOptionKey(option)" class="hover:bg-gray-50">
                      <td class="px-4 py-2 text-sm text-gray-900">{{ option.save_trm }}개월</td>
                      <td class="px-4 py-2 text-sm">
                        <span :class="getInterestRateColor(option.intr_rate)">
                          {{ formatRate(option.intr_rate) }}%
                        </span>
                      </td>
                      <td class="px-4 py-2 text-sm">
                        <span :class="getInterestRateColor(option.intr_rate2)">
                          {{ formatRate(option.intr_rate2) }}%
                        </span>
                      </td>
                      <td class="px-4 py-2 text-sm text-gray-900">{{ option.rsrv_type_nm || '-' }}</td>
                      <td class="px-4 py-2 text-sm text-gray-900">{{ option.intr_rate_type_nm || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 부가 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-lg font-semibold text-gray-900 mb-3">부가 정보</h4>
              <div class="space-y-3">
                <div>
                  <p class="text-sm text-gray-500">만기 후 이율</p>
                  <p class="text-base text-gray-900">{{ product.mtrt_int }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">특이사항</p>
                  <p class="text-base text-gray-900 whitespace-pre-line">{{ product.etc_note || '없음' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 푸터 -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            v-if="isAuthenticated"
            @click="toggleBookmark"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium sm:ml-3 sm:w-auto sm:text-sm"
            :class="isBookmarked ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-blue-600 hover:bg-blue-700 text-white'"
          >
            {{ isBookmarked ? '찜 해제' : '찜하기' }}
          </button>
          <button
            @click="closeModal"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { useModalStore } from '../../stores/modalStore'
import eventBus from '../../utils/eventBus'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  product: {
    type: Object,
    required: true
  },
  isAuthenticated: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'bookmark-updated'])

const modalStore = useModalStore()

const isBookmarked = ref(false)

// 중복 제거된 옵션 목록
const uniqueOptions = computed(() => {
  if (!props.product?.options) return []
  
  // 0개월 제외하고 가입기간 순으로 정렬
  const sortedOptions = [...props.product.options]
    .filter(opt => parseInt(opt.save_trm) > 0) // 0개월 제외
    .sort((a, b) => {
      return (parseInt(a.save_trm) || 0) - (parseInt(b.save_trm) || 0)
    })

  const uniqueMap = new Map()
  
  sortedOptions.forEach(opt => {
    const key = getOptionKey(opt)
    if (!uniqueMap.has(key)) {
      uniqueMap.set(key, {
        ...opt,
        save_trm: parseInt(opt.save_trm),
        intr_rate: parseFloat(opt.intr_rate) || 0,
        intr_rate2: parseFloat(opt.intr_rate2) || 0
      })
    } else {
      // 이미 존재하는 경우, 더 높은 금리를 가진 옵션으로 업데이트
      const existing = uniqueMap.get(key)
      const existingMaxRate = Math.max(existing.intr_rate, existing.intr_rate2)
      const newMaxRate = Math.max(parseFloat(opt.intr_rate) || 0, parseFloat(opt.intr_rate2) || 0)
      
      if (newMaxRate > existingMaxRate) {
        uniqueMap.set(key, {
          ...opt,
          save_trm: parseInt(opt.save_trm),
          intr_rate: parseFloat(opt.intr_rate) || 0,
          intr_rate2: parseFloat(opt.intr_rate2) || 0
        })
      }
    }
  })

  return Array.from(uniqueMap.values())
})

// 옵션의 고유 키 생성
const getOptionKey = (option) => {
  return `${option.save_trm}-${option.rsrv_type_nm}-${option.intr_rate_type_nm}`
}

// 금리에 따른 색상 반환
const getInterestRateColor = (rate) => {
  if (!rate) return 'text-gray-500'
  const numRate = parseFloat(rate)
  if (numRate >= 5) return 'text-red-600 font-semibold'
  if (numRate >= 4) return 'text-orange-600 font-semibold'
  if (numRate >= 3) return 'text-blue-600 font-semibold'
  return 'text-gray-900'
}

// 금리 포맷팅
const formatRate = (rate) => {
  if (rate === null || rate === undefined) return '-'
  const numRate = parseFloat(rate)
  return isNaN(numRate) ? '-' : numRate.toFixed(2)
}

// 북마크 상태 확인
const checkBookmarkStatus = async () => {
  if (!props.isAuthenticated || !props.product) return

  try {
    const accessToken = localStorage.getItem('access_token')
    if (!accessToken) return

    const response = await axios.get('/finrecom/bookmark/product/', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })
    
    isBookmarked.value = response.data.some(item => item.product_id === props.product.id)
  } catch (error) {
    console.error('북마크 상태 확인 실패:', error)
  }
}

// 북마크 토글
const toggleBookmark = async () => {
  if (!props.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const accessToken = localStorage.getItem('access_token')
    if (!accessToken) return

    await axios.post(`/finrecom/bookmark/product/${props.product.id}/`, {}, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })

    isBookmarked.value = !isBookmarked.value
    
    // 북마크 상태 변경 이벤트 발생
    const bookmarkResponse = await axios.get('/finrecom/bookmark/product/', {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })
    eventBus.emit('bookmark-count-updated', bookmarkResponse.data.length)
    
    // 콜백 호출
    emit('bookmark-updated', {
      productId: props.product.id,
      isBookmarked: isBookmarked.value
    })

    // 북마크 상태 업데이트 처리
    modalStore.handleBookmarkUpdate(props.product.id, isBookmarked.value)

    // 찜 해제 시에만 모달 닫기
    if (!isBookmarked.value) {
      modalStore.closeProductDetailModal()
    }
  } catch (error) {
    console.error('찜하기 토글 실패:', error)
    alert('찜하기 처리 중 오류가 발생했습니다.')
  }
}

// 모달 닫기
const closeModal = () => {
  modalStore.closeProductDetailModal()
  emit('close')
}

// 컴포넌트 마운트 시 북마크 상태 확인
onMounted(() => {
  checkBookmarkStatus()
})

// product prop이 변경될 때마다 북마크 상태 다시 확인
watch(() => props.product, () => {
  checkBookmarkStatus()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style> 