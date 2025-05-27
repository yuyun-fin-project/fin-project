<template>
  <div class="bg-white rounded-xl shadow-sm p-6">
    <h2 class="text-xl text-black font-semibold mb-6">카드 사용 현황</h2>
    
    <!-- 전체 요약 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-blue-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-600">총 카드 수</h3>
        <p class="text-2xl font-bold text-blue-600">{{ cards.length }}장</p>
      </div>
      <div class="bg-blue-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-600">이번 달 총 지출</h3>
        <p class="text-2xl font-bold text-blue-600">{{ formatNumber(totalSpending) }}원</p>
      </div>
      <div class="bg-blue-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-600">평균 결제 금액</h3>
        <p class="text-2xl font-bold text-blue-600">{{ formatNumber(averageSpending) }}원</p>
      </div>
    </div>

    <!-- 카드 목록 -->
    <div class="space-y-4">
      <div 
        v-for="(card, index) in displayedCards" 
        :key="card.card_id" 
        class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
        @click="openCardDetails(card)"
      >
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-semibold text-black text-lg">{{ card.card_name }}</h3>
              <span v-if="isPrimaryCard(card)" 
                    class="px-2 py-0.5 text-xs bg-blue-600 text-white rounded-full">
                주거래
              </span>
            </div>
            <p class="text-sm text-gray-600">{{ maskCardNumber(card.card_num) }}</p>
          </div>
          <span :class="[
            'px-2 py-1 text-sm rounded-full',
            card.card_type === '01' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'
          ]">
            {{ getCardTypeText(card.card_type) }}
          </span>
        </div>
        <div class="mt-2 text-sm text-gray-600">
          <p>{{ card.org_code }} | {{ card.card_member === '1' ? '본인' : '가족' }}</p>
          <p v-if="isPrimaryCard(card)" class="mt-1 text-blue-600">
            최근 거래 {{ getCardStats(card).transactionCount }}건 · {{ formatNumber(getCardStats(card).totalAmount) }}원 사용
          </p>
        </div>
      </div>

      <!-- 펼치기/접기 버튼 -->
      <div v-if="cards.length > 3" class="text-center mt-4">
        <button
          @click="toggleExpand"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-800"
        >
          <span>{{ isExpanded ? '접기' : '더보기' }}</span>
          <svg
            class="w-4 h-4 ml-1 transition-transform duration-200"
            :class="{ 'transform rotate-180': isExpanded }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 카드 상세 모달 -->
    <CardDetailModal
      :show="!!selectedCard"
      :card="selectedCard"
      :approvals="cardApprovals"
      @close="closeModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { PropType } from 'vue'
import CardDetailModal from './CardDetailModal.vue'

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
  cards: {
    type: Array as PropType<Card[]>,
    required: true,
    default: () => []
  },
  totalSpending: {
    type: Number,
    required: true,
    default: 0
  },
  cardApprovals: {
    type: Array as PropType<CardApproval[]>,
    required: true,
    default: () => []
  }
})

const selectedCard = ref<Card | null>(null)

// 펼치기/접기 상태 관리
const isExpanded = ref(false)

// 표시할 카드 목록
const displayedCards = computed(() => {
  // 카드 목록을 주거래카드 우선으로 정렬
  const sortedCards = [...props.cards].sort((a, b) => {
    if (isPrimaryCard(a) && !isPrimaryCard(b)) return -1
    if (!isPrimaryCard(a) && isPrimaryCard(b)) return 1
    return 0
  })

  // 펼치기/접기 상태에 따라 표시할 카드 수 결정
  if (isExpanded.value || sortedCards.length <= 3) {
    return sortedCards
  }
  return sortedCards.slice(0, 3)
})

// 펼치기/접기 토글
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

// 카드 상세 모달 열기
const openCardDetails = (card: Card) => {
  selectedCard.value = card
}

// 카드 상세 모달 닫기
const closeModal = () => {
  selectedCard.value = null
}

// 평균 결제 금액 계산
const averageSpending = computed(() => {
  if (props.cards.length === 0) return 0
  return Math.round(props.totalSpending / props.cards.length)
})

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

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

// 카드별 통계 계산
const getCardStats = (card: Card) => {
  const cardTransactions = props.cardApprovals.filter(
    approval => approval.card_id === card.numeric_id && approval.status === '승인'
  )
  
  return {
    transactionCount: cardTransactions.length,
    totalAmount: cardTransactions.reduce((sum, t) => sum + t.approved_amt, 0)
  }
}

// 주거래카드 판별
const isPrimaryCard = (card: Card) => {
  // 모든 카드의 통계 계산
  const cardStats = props.cards.map(c => ({
    card: c,
    stats: getCardStats(c)
  }))

  // 거래량과 금액을 기준으로 점수 계산
  const scoredCards = cardStats.map(({ card, stats }) => {
    const transactionScore = stats.transactionCount / Math.max(...cardStats.map(c => c.stats.transactionCount))
    const amountScore = stats.totalAmount / Math.max(...cardStats.map(c => c.stats.totalAmount))
    return {
      card,
      score: (transactionScore + amountScore) / 2
    }
  })

  // 가장 높은 점수를 받은 카드 찾기
  const maxScore = Math.max(...scoredCards.map(c => c.score))
  const primaryCard = scoredCards.find(c => c.score === maxScore)

  return primaryCard?.card.card_id === card.card_id
}
</script>

<style scoped>
.card-type-credit {
  @apply bg-red-100 text-red-800;
}

.card-type-debit {
  @apply bg-blue-100 text-blue-800;
}

/* 애니메이션 효과 */
.space-y-4 > * {
  transition: all 0.3s ease-in-out;
}

/* 주거래카드 뱃지 애니메이션 */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.bg-blue-600 {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>