<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- 배경 오버레이 -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <!-- 모달 헤더 -->
        <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">상품 상세 정보</h3>
          <div class="flex items-center space-x-4">
            <!-- 북마크 버튼 -->
            <button
              v-if="isAuthenticated"
              @click="toggleBookmark"
              class="text-gray-400 hover:text-yellow-500 focus:outline-none transition-colors duration-200"
            >
              <svg
                :class="[isBookmarked ? 'text-yellow-500 fill-current' : 'text-gray-400']"
                class="h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
                />
              </svg>
            </button>
            <!-- 닫기 버튼 -->
            <button
              @click="close"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <span class="sr-only">닫기</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 모달 본문 -->
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="space-y-4">
            <!-- 상품 기본 정보 -->
            <div>
              <h4 class="font-medium text-gray-900">{{ product.fin_prdt_nm }}</h4>
              <p class="text-sm text-gray-500">{{ product.kor_co_nm }}</p>
            </div>

            <!-- 상품 상세 정보 -->
            <div class="space-y-3">
              <!-- 가입 방법 -->
              <div>
                <dt class="text-sm font-medium text-gray-500">가입 방법</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatJoinWay(product.join_way) }}</dd>
              </div>

              <!-- 가입 대상 -->
              <div>
                <dt class="text-sm font-medium text-gray-500">가입 대상</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatJoinMember(product.join_member) }}</dd>
              </div>

              <!-- 만기 후 이자율 -->
              <div>
                <dt class="text-sm font-medium text-gray-500">만기 후 이자율</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ product.mtrt_int || '-' }}</dd>
              </div>

              <!-- 우대조건 -->
              <div>
                <dt class="text-sm font-medium text-gray-500">우대조건</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ product.spcl_cnd || '-' }}</dd>
              </div>

              <!-- 기간별 금리 정보 -->
              <div>
                <dt class="text-sm font-medium text-gray-500 mb-2">기간별 금리</dt>
                <dd class="mt-1">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="grid grid-cols-2 gap-4">
                      <div v-for="option in product.options" :key="option.save_trm" class="text-sm">
                        <p class="font-medium text-gray-900">{{ option.save_trm }}개월</p>
                        <p class="text-gray-600">
                          기본 {{ option.intr_rate }}%
                          <span v-if="option.intr_rate2" class="text-blue-600">
                            (우대 {{ option.intr_rate2 }}%)
                          </span>
                        </p>
                        <p class="text-xs text-gray-500">{{ option.intr_rate_type_nm }}</p>
                      </div>
                    </div>
                  </div>
                </dd>
              </div>

              <!-- 유의사항 -->
              <div>
                <dt class="text-sm font-medium text-gray-500">유의사항</dt>
                <dd class="mt-1 text-sm text-gray-900 whitespace-pre-line">{{ product.etc_note || '-' }}</dd>
              </div>
            </div>
          </div>
        </div>

        <!-- 모달 푸터 -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            @click="close"
            class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

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
const isBookmarked = ref(false)

const close = () => {
  emit('close')
}

// 북마크 상태 확인
const checkBookmarkStatus = async () => {
  if (!props.isAuthenticated) return

  try {
    const response = await axios.get('/finrecom/bookmark/product/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    isBookmarked.value = response.data.some(
      bookmark => bookmark.product_id === props.product.id
    )
  } catch (error) {
    console.error('북마크 상태 확인 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
    }
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

    const headers = { Authorization: `Bearer ${accessToken}` }

    // POST 메소드로 통일
    await axios({
      method: 'post',
      url: `/finrecom/bookmark/product/${props.product.id}/`,
      headers
    })

    isBookmarked.value = !isBookmarked.value
    emit('bookmark-updated')
  } catch (error) {
    console.error('북마크 처리 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
    } else if (error.response?.status === 404) {
      alert('해당 상품을 찾을 수 없습니다.')
    } else {
      alert('북마크 처리 중 오류가 발생했습니다.')
    }
  }
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

onMounted(() => {
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