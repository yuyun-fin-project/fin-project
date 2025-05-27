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
        v-for="card in cards" 
        :key="card.card_id" 
        class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
        @click="openCardDetails(card)"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-semibold text-black text-lg">{{ card.card_name }}</h3>
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
        </div>
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
</script>

<style scoped>
.card-type-credit {
  @apply bg-red-100 text-red-800;
}

.card-type-debit {
  @apply bg-blue-100 text-blue-800;
}
</style>