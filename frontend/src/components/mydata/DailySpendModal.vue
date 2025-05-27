<!-- 일별 지출 내역 모달 -->
<template>
  <Teleport to="body">
    <div v-if="show" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]"
         @click="handleBackdropClick"
    >
      <div class="bg-white rounded-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden"
           @click.stop
      >
        <!-- 모달 헤더 -->
        <div class="p-6 border-b">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="text-xl font-semibold text-black">{{ formatDate(date) }} 지출 내역</h3>
              <p class="text-sm text-gray-600 mt-1">총 {{ transactions.length }}건의 거래</p>
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

        <!-- 일별 요약 정보 -->
        <div class="p-6 bg-blue-50">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-600">총 지출 금액</h4>
              <p class="text-lg font-semibold text-blue-600">{{ formatNumber(totalAmount) }}원</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-600">최다 이용 카드</h4>
              <p class="text-lg font-semibold text-blue-600">{{ mostUsedCard }}</p>
            </div>
          </div>
        </div>

        <!-- 거래내역 필터 -->
        <div class="px-6 py-4 border-b bg-gray-50">
          <div class="flex flex-wrap gap-4 items-center">
            <div class="flex items-center space-x-2">
              <label class="text-sm font-medium text-gray-600">정렬:</label>
              <select 
                v-model="sortOption" 
                class="rounded-lg border text-black border-gray-200 bg-white text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              >
                <option value="time-desc">시간 내림차순</option>
                <option value="time-asc">시간 오름차순</option>
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
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">시간</th>
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">카드</th>
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">카드사</th>
                  <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">가맹점</th>
                  <th class="px-4 py-2 text-right text-sm font-medium text-gray-500">금액</th>
                  <th class="px-4 py-2 text-center text-sm font-medium text-gray-500">상태</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="transaction in sortedTransactions" 
                    :key="transaction.approved_num"
                    class="hover:bg-gray-50"
                >
                  <td class="px-4 py-2 text-sm text-gray-900">{{ formatTime(transaction.approved_dtime) }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900">{{ transaction.card_name }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900">{{ getCardCompany(transaction.card_id) }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900">{{ transaction.merchant_name }}</td>
                  <td class="px-4 py-2 text-sm text-gray-900 text-right">{{ formatNumber(transaction.approved_amt) }}원</td>
                  <td class="px-4 py-2 text-sm text-center">
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full',
                      {
                        'bg-green-100 text-green-800': transaction.status === '승인',
                        'bg-yellow-100 text-yellow-800': transaction.status === '대기',
                        'bg-red-100 text-red-800': transaction.status === '승인취소'
                      }
                    ]">
                      {{ transaction.status }}
                    </span>
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
import { ref, computed, watch } from 'vue'
import { PropType } from 'vue'
import { Teleport } from 'vue'

interface Transaction {
  id: number;
  card_id: number;
  approved_num: string;
  approved_dtime: string;
  approved_amt: number;
  merchant_name: string;
  status: string;
  total_install_cnt: number;
  card_name: string;
}

interface Card {
  id: number;
  card_id: string;
  card_name: string;
  card_num: string;
  card_type: string;
  org_code: string;
  card_member: string;
}

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  date: {
    type: Date,
    required: true
  },
  transactions: {
    type: Array as PropType<Transaction[]>,
    required: true
  },
  cards: {
    type: Array as PropType<Card[]>,
    default: () => []
  }
})

const emit = defineEmits(['close'])

// 정렬 옵션
const sortOption = ref('time-desc')

// 모달 닫기
const closeModal = () => {
  emit('close')
}

// 날짜 포맷팅
const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  }).format(date)
}

// 시간 포맷팅
const formatTime = (datetime: string) => {
  const hour = datetime.slice(8, 10)
  const minute = datetime.slice(10, 12)
  return `${hour}:${minute}`
}

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

// props 데이터 모니터링
watch(() => props.cards, (newCards) => {
  console.log('Cards in DailySpendModal:', newCards)
}, { immediate: true })

watch(() => props.transactions, (newTransactions) => {
  console.log('Transactions in DailySpendModal:', newTransactions)
}, { immediate: true })

// 카드 정보 찾기 함수
const findCardInfo = (cardId: number) => {
  console.log('Finding card for ID:', cardId)
  const matchingCard = props.cards.find(card => card.id === cardId)
  console.log('Found card:', matchingCard)
  return matchingCard ? matchingCard.card_name : '알 수 없는 카드'
}

// 정렬된 거래 내역
const sortedTransactions = computed(() => {
  const sorted = [...props.transactions].map(transaction => ({
    ...transaction,
    card_name: findCardInfo(transaction.card_id)
  }))
  
  switch (sortOption.value) {
    case 'time-desc':
      return sorted.sort((a, b) => b.approved_dtime.localeCompare(a.approved_dtime))
    case 'time-asc':
      return sorted.sort((a, b) => a.approved_dtime.localeCompare(b.approved_dtime))
    case 'amount-desc':
      return sorted.sort((a, b) => b.approved_amt - a.approved_amt)
    case 'amount-asc':
      return sorted.sort((a, b) => a.approved_amt - b.approved_amt)
    default:
      return sorted
  }
})

// 총 지출 금액
const totalAmount = computed(() => {
  return props.transactions
    .filter(t => t.status === '승인')
    .reduce((sum, t) => sum + t.approved_amt, 0)
})

// 최다 이용 카드
const mostUsedCard = computed(() => {
  const cardCounts = props.transactions.reduce((acc, t) => {
    acc[t.card_name] = (acc[t.card_name] || 0) + 1
    return acc
  }, {} as Record<string, number>)
  
  const mostUsed = Object.entries(cardCounts)
    .sort(([,a], [,b]) => b - a)[0]
  
  return mostUsed ? mostUsed[0] : '-'
})

// 카드사 정보 가져오기 함수
const getCardCompany = (cardId: number) => {
  const card = props.cards.find(card => card.id === cardId)
  if (!card) return '알 수 없음'
  
  const companyMap: { [key: string]: string } = {
    '002': '산업은행',
    '003': '기업은행',
    '004': 'KB국민',
    '011': 'NH농협',
    '020': '우리카드',
    '027': '시티카드',
    '031': '대구은행',
    '071': '롯데카드',
    '081': '하나카드',
    '091': '신한카드',
    '092': '삼성카드',
    '094': '현대카드',
    '096': '비씨카드'
  }
  
  return companyMap[card.org_code] || card.org_code
}

// 모달 외부 클릭 핸들러
const handleBackdropClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    closeModal()
  }
}
</script> 