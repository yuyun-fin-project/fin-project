<template>
  <div class="mydata-page">
    <!-- 비로그인 상태일 때 로그인 유도 HeroSection 표시 -->
    <template v-if="!isAuthenticated">
      <HeroSection />
    </template>

    <!-- 로그인 상태일 때 -->
    <template v-else>
      <!-- 카드 데이터가 없을 때 카드 연동 유도 HeroSection 표시 -->
      <template v-if="!hasCardData && !isLoading">
        <HeroSection />
      </template>

      <!-- 카드 데이터가 있을 때 마이데이터 분석 화면 표시 -->
      <template v-else>
        <div
          v-motion
          :initial="{ opacity: 0, y: 40 }"
          :enter="{ opacity: 1, y: 0 }"
          :delay="300"
          :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
          class="mydata-container"
        >
          <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900">
              마이데이터 분석
            </h1>
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
            <!-- 기존 컴포넌트들 -->
            <CardSummarySection 
              :cards="cardData.card_list" 
              :total-spending="getTotalSpending"
              :card-approvals="cardData.card_approvals"
            />

            <div class="grid md:grid-cols-2 gap-6">
              <SpendCalandar 
                :approvals="cardData.card_approvals"
                :cards="cardData.card_list"
                class="bg-white rounded-xl shadow-sm p-6" 
              />
              <SpendCalandarGraph 
                :monthly-data="getMonthlySpending"
                class="bg-white rounded-xl shadow-sm p-6" 
              />
            </div>

            <RecommendGpt 
              :card-data="cardData"
              @update-recommendation="updateRecommendation"
            />

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
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import CardSummarySection from '../components/mydata/CardSummarySection.vue'
import SpendCalandar from '../components/mydata/SpendCalandar.vue'
import SpendCalandarGraph from '../components/mydata/SpendCalandarGraph.vue'
import RecommendGpt from '../components/mydata/RecommendGpt.vue'
import HeroSection from '../components/HeroSection.vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'

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

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

// 로그인 상태 확인
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

// 카드 데이터 존재 여부 확인
const hasCardData = computed(() => {
  return cardData.value.card_list.length > 0
})

// API 기본 설정
const API_BASE_URL = 'http://localhost:8000'

// 마이데이터 가져오기
const fetchMyData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`${API_BASE_URL}/mydata/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    console.log('API Response:', response.data)
    
    // card_list에 numeric_id 추가
    const processedData = {
      ...response.data,
      card_list: response.data.card_list.map(card => ({
        ...card,
        numeric_id: card.id
      }))
    }
    
    console.log('Processed Data:', processedData)
    cardData.value = processedData
    checkForNotifications()
  } catch (err) {
    error.value = '데이터를 불러오는데 실패했습니다.'
    console.error('데이터 로딩 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  if (isLoggedIn.value) {
    fetchMyData()
  }
})

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
</script>

<style scoped>
.mydata-page {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem; /* 헤더 높이만큼 위로 올림 */
  padding-top: 5rem; /* 헤더 영역만큼 패딩 추가 */
}

.mydata-container {
  @apply max-w-6xl mx-auto px-4 py-8;
}

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