<!-- 카드 상세 모달 -->
<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]">
      <div class="bg-white rounded-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <!-- 모달 헤더 -->
        <div class="p-6 border-b">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="text-xl font-semibold text-black">{{ card.card_name }} 거래내역</h3>
              <p class="text-sm text-gray-600 mt-1">{{ maskCardNumber(card.card_num) }}</p>
            </div>
            <button 
              @click="closeModal" 
              class="text-gray-500 hover:text-gray-700"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 카드 요약 정보 -->
        <div class="p-6 bg-blue-50">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-600">카드 종류</h4>
              <p class="text-lg font-semibold text-blue-600">{{ getCardTypeText(card.card_type) }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-600">이번 달 사용금액</h4>
              <p class="text-lg font-semibold text-blue-600">{{ formatNumber(currentMonthTotal) }}원</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-600">평균 결제금액</h4>
              <p class="text-lg font-semibold text-blue-600">{{ formatNumber(averageAmount) }}원</p>
            </div>
          </div>
        </div>
        
        <!-- 거래내역 필터 -->
        <div class="px-6 py-4 border-b bg-gray-50">
          <div class="flex flex-wrap gap-4 items-center">
            <div class="flex items-center space-x-2">
              <label class="text-sm font-medium text-gray-600">상태:</label>
              <select 
                v-model="filters.status" 
                class="rounded-lg border text-black border-gray-200 bg-white text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              >
                <option value="">전체</option>
                <option value="승인">승인</option>
                <option value="대기">대기</option>
                <option value="승인취소">승인취소</option>
              </select>
            </div>
            <div class="flex items-center space-x-2">
              <label class="text-sm font-medium text-gray-600">정렬:</label>
              <select 
                v-model="filters.sort" 
                class="rounded-lg border text-black border-gray-200 bg-white text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              >
                <option value="date-desc">최신순</option>
                <option value="date-asc">과거순</option>
                <option value="amount-desc">금액 높은순</option>
                <option value="amount-asc">금액 낮은순</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 거래내역 테이블 -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-20rem)]">
          <div class="overflow-x-auto">
            <table class="min-w-full">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">거래일시</th>
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">가맹점</th>
                  <th class="px-4 py-2 text-right text-sm font-medium text-gray-500">금액</th>
                  <th class="px-4 py-2 text-center text-sm font-medium text-gray-500">상태</th>
                  <th class="px-4 py-2 text-center text-sm font-medium text-gray-500">할부</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="approval in filteredApprovals" 
                    :key="approval.approved_num"
                    class="hover:bg-gray-50"
                >
                  <td class="px-4 py-2 text-sm text-gray-900">{{ formatDateTime(approval.approved_dtime) }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900">{{ approval.merchant_name }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900 text-right">{{ formatNumber(approval.approved_amt) }}원</td>
                  <td class="px-4 py-2 text-sm text-center">
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full',
                      {
                        'bg-green-100 text-green-800': approval.status === '승인',
                        'bg-yellow-100 text-yellow-800': approval.status === '대기',
                        'bg-red-100 text-red-800': approval.status === '승인취소'
                      }
                    ]">
                      {{ approval.status }}
                    </span>
                  </td>
                  <td class="px-4 py-2 text-sm text-center text-gray-900">
                    {{ approval.total_install_cnt > 1 ? `${approval.total_install_cnt}개월` : '일시불' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { PropType } from 'vue'

// Teleport 컴포넌트 import
import { Teleport } from 'vue'

interface Card {
  card_id: string;
  numeric_id: number;
  card_name: string;
  card_num: string;
  card_type: string;
  org_code: string;
  card_member: string;
}

interface CardApproval {
  card_id: number;
  approved_num: string;
  approved_dtime: string;
  approved_amt: number;
  merchant_name: string;
  status: string;
  total_install_cnt: number;
}

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  card: {
    type: Object as PropType<Card>,
    required: true
  },
  approvals: {
    type: Array as PropType<CardApproval[]>,
    required: true
  }
})

const emit = defineEmits(['close'])

// 필터 상태
const filters = ref({
  status: '',
  sort: 'date-desc'
})

// 모달 닫기
const closeModal = () => {
  emit('close')
}

// 카드 번호 마스킹
const maskCardNumber = (cardNum: string) => {
  if (!cardNum) return ''
  return cardNum.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/, '$1-****-****-$4')
}

// 카드 타입 텍스트 변환
const getCardTypeText = (type: string) => {
  const types = {
    '01': '신용',
    '02': '체크',
    '03': '소액신용체크'
  }
  return types[type] || '기타'
}

// 날짜 시간 포맷팅
const formatDateTime = (datetime: string) => {
  if (!datetime) return ''
  const year = datetime.slice(0, 4)
  const month = datetime.slice(4, 6)
  const day = datetime.slice(6, 8)
  const hour = datetime.slice(8, 10)
  const minute = datetime.slice(10, 12)
  return `${year}.${month}.${day} ${hour}:${minute}`
}

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

// 필터링된 승인 내역
const filteredApprovals = computed(() => {
  let result = [...props.approvals].filter(approval => approval.card_id === props.card.numeric_id)

  // 상태 필터
  if (filters.value.status) {
    result = result.filter(approval => approval.status === filters.value.status)
  }

  // 정렬
  switch (filters.value.sort) {
    case 'date-desc':
      result.sort((a, b) => b.approved_dtime.localeCompare(a.approved_dtime))
      break
    case 'date-asc':
      result.sort((a, b) => a.approved_dtime.localeCompare(b.approved_dtime))
      break
    case 'amount-desc':
      result.sort((a, b) => b.approved_amt - a.approved_amt)
      break
    case 'amount-asc':
      result.sort((a, b) => a.approved_amt - b.approved_amt)
      break
  }

  return result
})

// 이번 달 총 사용금액
const currentMonthTotal = computed(() => {
  return filteredApprovals.value
    .filter(approval => approval.status === '승인')
    .reduce((sum, approval) => sum + approval.approved_amt, 0)
})

// 평균 결제금액
const averageAmount = computed(() => {
  const approvedTransactions = filteredApprovals.value.filter(a => a.status === '승인')
  if (approvedTransactions.length === 0) return 0
  const total = approvedTransactions.reduce((sum, a) => sum + a.approved_amt, 0)
  return Math.round(total / approvedTransactions.length)
})
</script>

<style scoped>
/* 모달이 열려있을 때 스크롤 방지 */
:root {
  overflow: hidden;
}
</style> 