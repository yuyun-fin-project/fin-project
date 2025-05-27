<template>
  <div class="h-full flex flex-col">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">월별 지출 추이</h2>
    
    <!-- 그래프 영역 -->
    <div class="flex-grow relative">
      <Line
        :data="chartData"
        :options="chartOptions"
        style="height: 100%"
      />
    </div>

    <!-- 요약 정보 -->
    <div class="grid grid-cols-2 gap-4 mt-4">
      <div class="bg-blue-50 rounded-xl p-3">
        <div class="text-sm text-gray-600">최근 6개월 평균</div>
        <div class="text-lg font-bold text-blue-600">
          {{ formatNumber(averageSpending) }}원
        </div>
      </div>
      <div :class="['rounded-xl p-3', getComparisonClass()]">
        <div class="text-sm text-gray-600">전월 대비</div>
        <div class="text-lg font-bold" :class="getComparisonTextClass()">
          {{ formatPercentage(monthOverMonthChange) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  monthlyData: {
    type: Object,
    required: true
  }
})

// 차트 데이터 준비
const chartData = computed(() => {
  const labels = Object.keys(props.monthlyData).sort()
  const data = labels.map(month => props.monthlyData[month])

  return {
    labels: labels.map(month => month.slice(4) + '월'),
    datasets: [
      {
        label: '월별 지출',
        data: data,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        fill: true
      }
    ]
  }
})

// 차트 옵션
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          return `${formatNumber(context.raw)}원`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value: number) => {
          return value.toLocaleString() + '원'
        }
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}

// 최근 6개월 평균 계산
const averageSpending = computed(() => {
  const values = Object.values(props.monthlyData)
  if (values.length === 0) return 0
  return Math.round(values.reduce((a, b) => a + b, 0) / values.length)
})

// 전월 대비 변화율 계산
const monthOverMonthChange = computed(() => {
  const months = Object.keys(props.monthlyData).sort()
  if (months.length < 2) return 0

  const currentMonth = props.monthlyData[months[months.length - 1]]
  const previousMonth = props.monthlyData[months[months.length - 2]]

  if (!previousMonth) return 0
  return ((currentMonth - previousMonth) / previousMonth) * 100
})

// 숫자 포맷팅
const formatNumber = (num: number) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

// 퍼센트 포맷팅
const formatPercentage = (num: number) => {
  const sign = num > 0 ? '+' : ''
  return `${sign}${num.toFixed(1)}%`
}

// 비교 결과에 따른 배경색 클래스
const getComparisonClass = () => {
  if (monthOverMonthChange.value > 0) return 'bg-red-50'
  if (monthOverMonthChange.value < 0) return 'bg-green-50'
  return 'bg-gray-50'
}

// 비교 결과에 따른 텍스트 색상 클래스
const getComparisonTextClass = () => {
  if (monthOverMonthChange.value > 0) return 'text-red-600'
  if (monthOverMonthChange.value < 0) return 'text-green-600'
  return 'text-gray-600'
}
</script>

<style scoped>
:deep(.chartjs-render-monitor) {
  height: 100% !important;
}
</style>
