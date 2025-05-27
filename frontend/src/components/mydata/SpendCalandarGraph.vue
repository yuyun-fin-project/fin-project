<template>
  <div>
    <h2 class="text-xl font-semibold text-black mb-4">월별 지출 추이</h2>
    <div class="chart-container">
      <canvas ref="chartRef"></canvas>
    </div>
    <div class="mt-4 grid grid-cols-2 gap-4">
      <div class="bg-blue-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-600">최근 6개월 평균</h3>
        <p class="text-2xl font-bold text-blue-600">{{ formatNumber(averageSpending) }}원</p>
      </div>
      <div class="bg-blue-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-600">전월 대비</h3>
        <p class="text-2xl font-bold" :class="monthOverMonthColor">
          {{ monthOverMonthChange }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  monthlyData: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const chartRef = ref(null)
let chart = null

// 데이터 정렬 및 변환
const sortedData = computed(() => {
  return Object.entries(props.monthlyData)
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-6)
})

// 차트 데이터
const chartData = computed(() => ({
  labels: sortedData.value.map(([month]) => `${month.slice(4)}월`),
  datasets: [{
    label: '월별 지출',
    data: sortedData.value.map(([, amount]) => amount),
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
    borderColor: 'rgb(59, 130, 246)',
    borderWidth: 2,
    tension: 0.4
  }]
}))

// 차트 옵션
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value) => `${new Intl.NumberFormat('ko-KR').format(value)}원`
      }
    }
  }
}

// 평균 지출
const averageSpending = computed(() => {
  const amounts = sortedData.value.map(([, amount]) => amount)
  return Math.round(amounts.reduce((a, b) => a + b, 0) / amounts.length)
})

// 전월 대비 변화
const monthOverMonthChange = computed(() => {
  if (sortedData.value.length < 2) return '데이터 없음'
  
  const currentMonth = sortedData.value[sortedData.value.length - 1][1]
  const previousMonth = sortedData.value[sortedData.value.length - 2][1]
  const change = ((currentMonth - previousMonth) / previousMonth) * 100
  
  return `${change > 0 ? '+' : ''}${change.toFixed(1)}%`
})

// 전월 대비 색상
const monthOverMonthColor = computed(() => {
  const change = parseFloat(monthOverMonthChange.value)
  if (change > 0) return 'text-red-600'
  if (change < 0) return 'text-green-600'
  return 'text-gray-600'
})

// 차트 생성 및 업데이트
const createChart = () => {
  const ctx = chartRef.value.getContext('2d')
  chart = new Chart(ctx, {
    type: 'line',
    data: chartData.value,
    options: chartOptions
  })
}

const updateChart = () => {
  if (chart) {
    chart.data = chartData.value
    chart.update()
  }
}

// 데이터 변경 감지
watch(() => props.monthlyData, updateChart, { deep: true })

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

onMounted(() => {
  createChart()
})
</script>

<style scoped>
.chart-container {
  @apply h-64;
}
</style>
