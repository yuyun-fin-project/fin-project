<template>
  <div>
    <h2 class="text-xl font-semibold text-black mb-4">지출 캘린더</h2>
    <div class="calendar-container">
      <div class="calendar-header flex justify-between items-center mb-4">
        <button 
          @click="previousMonth" 
          class="p-2 hover:bg-gray-100 rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
        >
          <span class="sr-only">이전 달</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h3 class="text-lg text-black font-medium">{{ currentYearMonth }}</h3>
        <button 
          @click="nextMonth" 
          class="p-2 hover:bg-gray-100 rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
        >
          <span class="sr-only">다음 달</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- 요일 헤더 -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div v-for="day in ['일', '월', '화', '수', '목', '금', '토']" 
          :key="day"
          class="text-center text-sm font-medium py-2"
          :class="day === '일' ? 'text-red-500' : day === '토' ? 'text-blue-500' : 'text-gray-600'"
        >
          {{ day }}
        </div>
      </div>

      <!-- 달력 날짜 -->
      <div class="grid grid-cols-7 gap-2">
        <div
          v-for="day in calendarDays"
          :key="day.date.toISOString()"
          class="aspect-square relative border rounded-lg"
          :class="[
            {
              'bg-gray-50': !isCurrentMonth(day.date),
              'bg-white hover:bg-blue-50 cursor-pointer': isCurrentMonth(day.date) && hasDayTransactions(day.date),
              'bg-white': isCurrentMonth(day.date) && !hasDayTransactions(day.date),
              'border-blue-500': isToday(day.date),
              'border-gray-200': !isToday(day.date)
            }
          ]"
          @click="hasDayTransactions(day.date) && handleDateClick(day.date)"
        >
          <div class="absolute inset-0 p-2 flex flex-col">
            <span class="text-sm font-medium" :class="getDayClass(day.date)">
              {{ day.date.getDate() }}
            </span>
            <div v-if="day.spending > 0" class="mt-auto">
              <div class="text-xs font-medium text-gray-900">
                {{ formatNumber(day.spending) }}원
              </div>
              <div class="w-full h-1 rounded-full mt-1"
                :class="getSpendingColorClass(day.spending)"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 일별 지출 내역 모달 -->
      <DailySpendModal
        v-if="selectedDate"
        :show="showDailyModal"
        :date="selectedDate"
        :transactions="selectedDayTransactions"
        @close="closeDailyModal"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format, startOfMonth, endOfMonth, eachDayOfInterval, addMonths, subMonths } from 'date-fns'
import { ko } from 'date-fns/locale'
import { PropType } from 'vue'
import DailySpendModal from './DailySpendModal.vue'

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
  numeric_id: number;
  card_id: string;
  card_name: string;
  card_num: string;
  card_type: string;
  org_code: string;
  card_member: string;
}

const props = defineProps({
  approvals: {
    type: Array as PropType<Transaction[]>,
    required: true,
    default: () => []
  },
  cards: {
    type: Array as PropType<Card[]>,
    required: true,
    default: () => []
  }
})

const currentDate = ref(new Date())

// 현재 연월 표시
const currentYearMonth = computed(() => {
  return format(currentDate.value, 'yyyy년 M월', { locale: ko })
})

// 날짜 문자열을 Date 객체로 변환
const parseDate = (dateStr: string) => {
  const year = parseInt(dateStr.slice(0, 4))
  const month = parseInt(dateStr.slice(4, 6)) - 1 // 0-based month
  const day = parseInt(dateStr.slice(6, 8))
  return new Date(year, month, day)
}

// 거래 내역이 있는 날짜 확인 함수
const hasDayTransactions = (date: Date) => {
  const targetDate = format(date, 'yyyyMMdd')
  return props.approvals.some(approval => approval.approved_dtime.startsWith(targetDate))
}

// 카드 정보 찾기 함수
const findCardInfo = (cardId: number) => {
  console.log('Finding card for ID:', cardId)
  console.log('Available cards:', props.cards)
  
  const matchingCard = props.cards.find(card => {
    console.log('Comparing:', card.numeric_id, cardId)
    return Number(card.numeric_id) === Number(cardId)
  })
  
  console.log('Found card:', matchingCard)
  return matchingCard ? matchingCard.card_name : '알 수 없는 카드'
}

// 날짜 클릭 핸들러
const handleDateClick = (date: Date) => {
  const targetDate = format(date, 'yyyyMMdd')
  console.log('Selected date:', targetDate)
  
  // 해당 날짜의 거래 내역 필터링 및 카드 정보 추가
  const dayTransactions = props.approvals
    .filter(approval => approval.approved_dtime.startsWith(targetDate))
    .map(approval => {
      console.log('Processing approval:', approval)
      const cardName = findCardInfo(approval.card_id)
      console.log('Found card name:', cardName)
      return {
        ...approval,
        card_name: cardName
      }
    })

  console.log('Final transactions:', dayTransactions)

  // 거래 내역이 있는 경우에만 모달 표시
  if (dayTransactions.length > 0) {
    selectedDate.value = date
    selectedDayTransactions.value = dayTransactions
    showDailyModal.value = true
  }
}

// 달력 데이터 생성
const calendarDays = computed(() => {
  const start = startOfMonth(currentDate.value)
  const end = endOfMonth(currentDate.value)
  
  // 첫 주의 시작일과 마지막 주의 마지막일을 포함
  const firstDay = new Date(start)
  firstDay.setDate(firstDay.getDate() - firstDay.getDay())
  const lastDay = new Date(end)
  lastDay.setDate(lastDay.getDate() + (6 - lastDay.getDay()))

  const days = eachDayOfInterval({ start: firstDay, end: lastDay })

  return days.map(date => {
    const targetDate = format(date, 'yyyyMMdd')
    const spending = props.approvals
      .filter(approval => 
        approval.approved_dtime.startsWith(targetDate) && 
        approval.status === '승인'
      )
      .reduce((sum, approval) => sum + approval.approved_amt, 0)

    return {
      date,
      spending,
      isCurrentMonth: date.getMonth() === currentDate.value.getMonth()
    }
  })
})

// 날짜 이동
const previousMonth = () => {
  currentDate.value = subMonths(currentDate.value, 1)
}

const nextMonth = () => {
  currentDate.value = addMonths(currentDate.value, 1)
}

// 오늘 날짜 확인
const isToday = (date: Date) => {
  const today = new Date()
  return format(date, 'yyyyMMdd') === format(today, 'yyyyMMdd')
}

// 날짜 스타일 클래스
const getDayClass = (date: Date) => {
  const day = date.getDay()
  if (day === 0) return 'text-red-500'
  if (day === 6) return 'text-blue-500'
  return 'text-gray-900'
}

// 지출 금액에 따른 색상 클래스
const getSpendingColorClass = (amount: number) => {
  if (amount > 1000000) return 'bg-red-500'
  if (amount > 500000) return 'bg-orange-500'
  if (amount > 100000) return 'bg-yellow-500'
  return 'bg-green-500'
}

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

// 모달 상태 관리
const showDailyModal = ref(false)
const selectedDate = ref<Date | null>(null)
const selectedDayTransactions = ref<Transaction[]>([])

// 모달 닫기
const closeDailyModal = () => {
  showDailyModal.value = false
  selectedDate.value = null
  selectedDayTransactions.value = []
}

// 현재 월의 날짜인지 확인
const isCurrentMonth = (date: Date) => {
  return date.getMonth() === currentDate.value.getMonth()
}
</script>

<style scoped>
.calendar-container {
  @apply bg-white rounded-lg;
}

.aspect-square {
  aspect-ratio: 1;
}
</style>
