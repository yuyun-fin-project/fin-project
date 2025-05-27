<template>
  <div class="mydata-view">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-6xl mx-auto px-4 py-12"
    >
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900">
          마이데이터 분석
        </h1>
        <button 
          @click="refreshData" 
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          데이터 새로고침
        </button>
      </div>
      
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>

      <!-- 에러 상태 -->
      <div v-else-if="error" class="bg-red-50 p-4 rounded-lg mb-6">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <!-- 데이터 표시 -->
      <div v-else class="grid gap-6">
        <!-- 카드 요약 섹션 -->
        <CardSummarySection 
          :cards="cardData.card_list" 
          :total-spending="getTotalSpending"
          :card-approvals="cardData.card_approvals"
        />

        <!-- 지출 캘린더 및 그래프 -->
        <div class="grid md:grid-cols-2 gap-6">
          <SpendCalandar 
            :approvals="cardData.card_approvals"
            class="bg-white rounded-xl shadow-sm p-6" 
          />
          <SpendCalandarGraph 
            :monthly-data="getMonthlySpending"
            class="bg-white rounded-xl shadow-sm p-6" 
          />
        </div>

        <!-- GPT 추천 섹션 -->
        <RecommendGpt 
          :card-data="cardData"
          @update-recommendation="updateRecommendation"
        />

        <!-- 알림 섹션 -->
        <div v-if="notifications.length" class="bg-blue-50 p-4 rounded-lg">
          <h3 class="font-semibold mb-2">알림</h3>
          <ul class="space-y-2">
            <li 
              v-for="notification in notifications" 
              :key="notification.id"
              class="text-sm text-blue-800"
            >
              {{ notification.message }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import CardSummarySection from '../components/mydata/CardSummarySection.vue'
import SpendCalandar from '../components/mydata/SpendCalandar.vue'
import SpendCalandarGraph from '../components/mydata/SpendCalandarGraph.vue'
import RecommendGpt from '../components/mydata/RecommendGpt.vue'
import axios from 'axios'

// 상태 관리
const isLoading = ref(false)
const error = ref(null)
const cardData = ref({
  card_list: [],
  card_approvals: [],
  card_bills: []
})
const notifications = ref([])
const recommendation = ref(null)

// API 기본 설정
const API_BASE_URL = 'http://localhost:8000'

// 데이터 가져오기
const fetchData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`${API_BASE_URL}/mydata/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    // card_list에 numeric_id 추가
    const processedData = {
      ...response.data,
      card_list: response.data.card_list.map((card, index) => ({
        ...card,
        numeric_id: index + 1  // 1부터 시작하는 순차적인 ID 부여
      }))
    }
    cardData.value = processedData
    checkForNotifications()
  } catch (err) {
    error.value = '데이터를 불러오는데 실패했습니다.'
    console.error('데이터 로딩 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 데이터 새로고침
const refreshData = () => {
  fetchData()
}

// 총 지출액 계산
const getTotalSpending = computed(() => {
  return cardData.value.card_approvals.reduce((total, approval) => {
    if (approval.status === '승인') {
      return total + Number(approval.approved_amt)
    }
    return total
  }, 0)
})

// 월별 지출 데이터 계산
const getMonthlySpending = computed(() => {
  const monthlyData = {}
  cardData.value.card_bills.forEach(bill => {
    const month = bill.bill_year_month
    monthlyData[month] = (monthlyData[month] || 0) + Number(bill.total_amount)
  })
  return monthlyData
})

// 알림 체크
const checkForNotifications = () => {
  notifications.value = []
  
  // 높은 지출 알림
  const totalSpending = getTotalSpending.value
  if (totalSpending > 1000000) {
    notifications.value.push({
      id: 1,
      message: '이번 달 지출이 100만원을 초과했습니다.'
    })
  }

  // 결제 예정 알림
  const today = new Date()
  cardData.value.card_bills.forEach(bill => {
    if (bill.payment_date) {
      const paymentDate = new Date(bill.payment_date)
      const diffDays = Math.ceil((paymentDate - today) / (1000 * 60 * 60 * 24))
      
      if (diffDays > 0 && diffDays <= 7) {
        notifications.value.push({
          id: Date.now(),
          message: `${bill.payment_date} 결제 예정: ${bill.total_amount.toLocaleString()}원`
        })
      }
    }
  })
}

// GPT 추천 업데이트
const updateRecommendation = (newRecommendation) => {
  recommendation.value = newRecommendation
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.mydata-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}

.grid {
  @apply gap-6;
}

@media (max-width: 768px) {
  .grid {
    @apply grid-cols-1;
  }
}
</style>