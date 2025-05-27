<template>
  <div class="bg-white rounded-xl shadow-sm p-6">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">시세 차트</h2>
      <p class="mt-1 text-sm text-gray-500">금, 석유, 탄소 시세를 확인하세요</p>
    </div>

    <!-- 상품 선택 탭 -->
    <div class="mb-6">
      <div class="flex justify-center p-1 bg-gray-50 rounded-xl">
        <nav class="flex space-x-2" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.name"
            @click="currentTab = tab.id"
            :class="[
              currentTab === tab.id
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100',
              'flex items-center px-6 py-3 rounded-lg text-sm font-medium transition-all duration-200 ease-in-out'
            ]"
          >
            <span class="flex items-center">
              <!-- 자산 이모티콘 -->
              <span class="text-xl mr-2">{{ tab.emoji }}</span>
              {{ tab.name }}
              <!-- 가격 변동 표시기 -->
              <span 
                v-if="currentTab === tab.id && priceChange"
                :class="[
                  priceChange > 0 ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-600',
                  'ml-2 px-2 py-0.5 rounded-full text-xs font-medium'
                ]"
              >
                {{ priceChange > 0 ? '▲' : '▼' }}
                {{ Math.abs(priceChangePercent).toFixed(1) }}%
              </span>
            </span>
          </button>
        </nav>
      </div>
    </div>

    <!-- 기간 선택 -->
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
        <div class="flex items-center space-x-3">
        <div class="relative">
            <input
              type="date"
              v-model="startDate"
              :max="endDate"
            class="block w-full text-black rounded-lg border-gray-300 pl-3 pr-10 py-2.5 text-sm focus:border-blue-500 focus:ring-blue-500 shadow-sm"
            @change="handleDateChange"
            />
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        <span class="text-gray-500 font-medium">~</span>
        <div class="relative">
            <input
              type="date"
              v-model="endDate"
              :min="startDate"
            class="block w-full text-black rounded-lg border-gray-300 pl-3 pr-10 py-2.5 text-sm focus:border-blue-500 focus:ring-blue-500 shadow-sm"
            @change="handleDateChange"
            />
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
          <button
          v-for="period in quickPeriods"
          :key="period.days"
          @click="setQuickPeriod(period.days)"
          class="px-4 py-2 text-sm rounded-lg transition-all duration-200 ease-in-out shadow-sm"
            :class="[
            isCurrentPeriod(period.days)
              ? 'bg-blue-500 text-white shadow-md transform scale-105'
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
          ]"
        >
          {{ period.label }}
          </button>
      </div>
    </div>

    <!-- 데이터 없음 상태 표시 -->
    <div v-if="showNoDataMessage" class="mb-6 p-4 bg-yellow-50 rounded-lg">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-yellow-800">데이터 없음</h3>
          <div class="mt-2 text-sm text-yellow-700">
            <p>선택하신 기간에 데이터가 없습니다. 다른 기간을 선택해주세요.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 차트 영역 -->
    <div class="relative h-80 mb-6">
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-lg">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
      <div v-if="showChartError" class="absolute inset-0 flex items-center justify-center bg-white rounded-lg">
        <div class="text-center p-4">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">차트 로딩 오류</h3>
          <p class="mt-1 text-sm text-gray-500">페이지를 새로고침 해주세요</p>
          <div class="mt-4">
            <button
              type="button"
              @click="handleRefresh"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="mr-2 -ml-1 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
              </svg>
              새로고침
            </button>
          </div>
        </div>
      </div>
      <canvas ref="chartRef" class="rounded-lg"></canvas>
    </div>

    <!-- 현재 시세 정보 -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="rounded-lg bg-gray-50 p-4 transition-colors duration-200 hover:bg-gray-100">
        <h3 class="text-sm font-medium text-gray-500">현재 시세</h3>
        <p class="mt-2 text-lg font-semibold text-gray-900">
          {{ currentPrice ? formatPrice(currentPrice) : '-' }}
        </p>
      </div>
      <div class="rounded-lg bg-gray-50 p-4 transition-colors duration-200 hover:bg-gray-100">
        <h3 class="text-sm font-medium text-gray-500">전일 대비</h3>
        <p :class="['mt-2 text-lg font-semibold', getPriceChangeColor()]">
          {{ priceChange ? (priceChange > 0 ? '+' : '') + formatPrice(priceChange) : '-' }}
        </p>
      </div>
      <div class="rounded-lg bg-gray-50 p-4 transition-colors duration-200 hover:bg-gray-100">
        <h3 class="text-sm font-medium text-gray-500">변동률</h3>
        <p :class="['mt-2 text-lg font-semibold', getPriceChangeColor()]">
          {{ priceChangePercent ? (priceChangePercent > 0 ? '+' : '') + priceChangePercent.toFixed(2) + '%' : '-' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'
import { format, subDays, parseISO } from 'date-fns'
import 'chartjs-adapter-date-fns'
import { ko } from 'date-fns/locale'

// 상태 관리
const chartRef = ref(null)
const chart = ref(null)
const isLoading = ref(false)
const currentTab = ref('gold')
const startDate = ref('')
const endDate = ref('')
const minDate = ref('')
const maxDate = ref('')
const currentPrice = ref(null)
const priceChange = ref(null)
const priceChangePercent = ref(null)

// 데이터 캐싱
const cachedData = ref({
  gold: null,
  oil: null,
  carbon: null
})

// API 호출 디바운스 타이머
let debounceTimer = null

// 탭 정의
const tabs = [
  { id: 'gold', name: '금', emoji: '💰' },
  { id: 'oil', name: '석유', emoji: '⛽' },
  { id: 'carbon', name: '탄소', emoji: '🌱' }
]

// 빠른 기간 선택 옵션
const quickPeriods = [
  { days: 7, label: '1주' },
  { days: 30, label: '1개월' },
  { days: 90, label: '3개월' },
  { days: 180, label: '6개월' },
  { days: 365, label: '1년' }
]

// 현재 선택된 기간이 빠른 선택 옵션과 일치하는지 확인
const isCurrentPeriod = (days) => {
  if (!startDate.value || !endDate.value) return false
  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  const diff = Math.round((end - start) / (1000 * 60 * 60 * 24))
  return diff === days
}

// 빠른 기간 선택
const setQuickPeriod = (days) => {
  const end = new Date()
  const start = subDays(end, days)
  
  // 시작일이 종료일보다 늦지 않도록 보장
  if (start <= end) {
    startDate.value = format(start, 'yyyy-MM-dd')
    endDate.value = format(end, 'yyyy-MM-dd')
  } else {
    // 만약 날짜가 거꾸로 되었다면 바로잡기
    startDate.value = format(end, 'yyyy-MM-dd')
    endDate.value = format(start, 'yyyy-MM-dd')
  }
  
  console.log('기간 설정:', { start: startDate.value, end: endDate.value })
  fetchData()
}

// 데이터 없음 상태 관리
const showNoDataMessage = ref(false)

// 차트 에러 상태 관리
const showChartError = ref(false)

// 날짜 변경 핸들러
const handleDateChange = () => {
  if (startDate.value && endDate.value) {
    const start = new Date(startDate.value)
    const end = new Date(endDate.value)
    
    // 시작일이 종료일보다 늦은 경우 날짜를 교환
    if (start > end) {
      const temp = startDate.value
      startDate.value = endDate.value
      endDate.value = temp
    }
    
    fetchData()
  }
}

// 데이터 가져오기
const fetchData = async () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  debounceTimer = setTimeout(async () => {
  isLoading.value = true
    try {
      let response;
      
      // 날짜가 선택되지 않은 경우 전체 데이터 조회
      if (!startDate.value || !endDate.value) {
        response = await axios.get('/finrecom/spot/')
      } else {
        const formattedStartDate = format(new Date(startDate.value), 'yyyyMMdd')
        const formattedEndDate = format(new Date(endDate.value), 'yyyyMMdd')
        response = await axios.get('/finrecom/spot/' + formattedStartDate + '/' + formattedEndDate + '/')
      }

      const data = response.data.items

      // 데이터 캐싱
      cachedData.value = {
        gold: data.Gold || [],
        oil: data.Oil || [],
        carbon: data.Carbon || []
      }

      // 날짜 범위 설정
      const allDates = []
      Object.values(data).forEach(items => {
        if (Array.isArray(items)) {
          items.forEach(item => {
            if (item.basDt) {
              const year = item.basDt.substring(0, 4)
              const month = item.basDt.substring(4, 6)
              const day = item.basDt.substring(6, 8)
              allDates.push(new Date(year + '-' + month + '-' + day))
            }
          })
        }
      })

      if (allDates.length > 0) {
        const minDateTime = new Date(Math.min(...allDates))
        const maxDateTime = new Date(Math.max(...allDates))
        
        minDate.value = format(minDateTime, 'yyyy-MM-dd')
        maxDate.value = format(maxDateTime, 'yyyy-MM-dd')
        
        if (!startDate.value || !endDate.value) {
          startDate.value = minDate.value
          endDate.value = maxDate.value
        }
      }

      processAndUpdateChart()
    } catch (error) {
      console.error('시세 데이터 가져오기 실패:', error)
  } finally {
    isLoading.value = false
  }
  }, 300) // 300ms 디바운스
}

// 데이터 처리 및 차트 업데이트
const processAndUpdateChart = () => {
  const data = cachedData.value
  if (!data) return

  try {
    showChartError.value = false
    let spotData = []
    switch (currentTab.value) {
      case 'gold':
        spotData = data.gold || []
        break
      case 'oil':
        const oilTypes = ['등유', '경유', '휘발유']
        spotData = oilTypes.map(type => ({
          type,
          data: (data.oil || []).filter(item => item.oilCtg === type)
        }))
        break
      case 'carbon':
        spotData = (data.carbon || []).filter(item => item.itmsNm === 'KAU24')
        break
    }

    // 선택된 기간 내의 데이터만 필터링
    const startTimestamp = new Date(startDate.value).getTime()
    const endTimestamp = new Date(endDate.value).getTime()

    let filteredData
    if (currentTab.value === 'oil') {
      filteredData = spotData.map(group => ({
        type: group.type,
        data: group.data.filter(item => {
          const itemDate = new Date(
            item.basDt.substring(0, 4),
            parseInt(item.basDt.substring(4, 6)) - 1,
            item.basDt.substring(6, 8)
          ).getTime()
          return itemDate >= startTimestamp && itemDate <= endTimestamp
        })
      }))
      
      // 데이터 존재 여부 확인
      showNoDataMessage.value = !filteredData.some(group => group.data.length > 0)
    } else {
      filteredData = spotData.filter(item => {
        const itemDate = new Date(
          item.basDt.substring(0, 4),
          parseInt(item.basDt.substring(4, 6)) - 1,
          item.basDt.substring(6, 8)
        ).getTime()
        return itemDate >= startTimestamp && itemDate <= endTimestamp
      })
      
      // 데이터 존재 여부 확인
      showNoDataMessage.value = filteredData.length === 0
    }

    // 데이터가 있는 경우에만 차트 업데이트
    if (!showNoDataMessage.value) {
      let chartData
      if (currentTab.value === 'oil') {
        chartData = filteredData.map(group => ({
          type: group.type,
          data: group.data.map(item => ({
            x: new Date(
              item.basDt.substring(0, 4),
              parseInt(item.basDt.substring(4, 6)) - 1,
              item.basDt.substring(6, 8)
            ).getTime(),
            y: parseFloat(item.wtAvgPrcDisc)
          })).sort((a, b) => a.x - b.x)
        }))
      } else {
        chartData = filteredData.map(item => ({
          x: new Date(
            item.basDt.substring(0, 4),
            parseInt(item.basDt.substring(4, 6)) - 1,
            item.basDt.substring(6, 8)
          ).getTime(),
          y: parseFloat(currentTab.value === 'gold' ?
            (item.clpr || item.basePrice || item.price) :
            item.clpr)
        })).sort((a, b) => a.x - b.x)
      }

      // 현재 시세 정보 업데이트
      if (currentTab.value === 'oil') {
        const gasolineData = chartData.find(group => group.type === '휘발유')?.data || []
        if (gasolineData.length > 0) {
          updatePriceInfo(gasolineData)
        }
      } else if (chartData.length > 0) {
        updatePriceInfo(chartData)
      }

      // 차트 업데이트
      setTimeout(() => {
        updateChart(chartData)
      }, 50)
    } else {
      // 데이터가 없는 경우 차트 초기화
      if (chart.value) {
        chart.value.destroy()
        chart.value = null
      }
      // 가격 정보 초기화
      currentPrice.value = null
      priceChange.value = null
      priceChangePercent.value = null
    }
  } catch (error) {
    console.error('데이터 처리 중 오류 발생:', error)
    showChartError.value = true
    showNoDataMessage.value = true
  }
}

// 가격 정보 업데이트 함수
const updatePriceInfo = (data) => {
  const latestPrice = data[data.length - 1].y
  const previousPrice = data[data.length - 2]?.y || data[data.length - 1].y
  
  currentPrice.value = latestPrice
  priceChange.value = latestPrice - previousPrice
  priceChangePercent.value = (priceChange.value / previousPrice) * 100
}

// 새로고침 핸들러
const handleRefresh = () => {
  window.location.reload()
}

// 차트 업데이트
const updateChart = (data) => {
  // 데이터 유효성 검사
  if (!data || (Array.isArray(data) && data.length === 0)) {
    if (chart.value) {
      chart.value.destroy()
      chart.value = null
    }
    return
  }

  try {
    showChartError.value = false
    if (chart.value) {
      chart.value.destroy()
      chart.value = null
    }

    const ctx = chartRef.value?.getContext('2d')
    if (!ctx) {
      showChartError.value = true
      return
    }

    // 데이터셋 구성
    const datasets = currentTab.value === 'oil'
      ? data.filter(group => group.data && group.data.length > 0).map(group => ({
          label: `${group.type} 도매가`,
          data: group.data,
          borderColor: group.type === '휘발유' ? 'rgb(239, 68, 68)' :
                      group.type === '경유' ? 'rgb(59, 130, 246)' :
                      'rgb(34, 197, 94)',
          backgroundColor: group.type === '휘발유' ? 'rgba(239, 68, 68, 0.1)' :
                          group.type === '경유' ? 'rgba(59, 130, 246, 0.1)' :
                          'rgba(34, 197, 94, 0.1)',
          fill: true,
          tension: 0.4
        }))
      : [{
          label: getChartLabel(),
          data: data,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4
        }]

    // 데이터셋이 비어있으면 차트를 그리지 않음
    if (datasets.length === 0 || datasets.some(dataset => !dataset.data || dataset.data.length === 0)) {
      return
    }

    chart.value = new Chart(ctx, {
      type: 'line',
      data: {
        datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 300 // 애니메이션 시간 단축
        },
        interaction: {
          intersect: false,
          mode: 'index'
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'MM.dd'
              }
            },
            adapters: {
              date: {
                locale: ko
              }
            },
            title: {
              display: true,
              text: '날짜'
            }
          },
          y: {
            title: {
              display: true,
              text: getYAxisLabel()
            },
            ticks: {
              callback: function(value) {
                return formatPrice(value)
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                return context.dataset.label + ': ' + formatPrice(context.parsed.y)
              }
            }
          },
          legend: {
            display: currentTab.value === 'oil',
            position: 'top'
          }
        }
      }
    })
  } catch (error) {
    console.error('차트 업데이트 중 오류 발생:', error)
    showChartError.value = true
    if (chart.value) {
      chart.value.destroy()
      chart.value = null
    }
  }
}

// 차트 레이블 가져오기
const getChartLabel = () => {
  switch (currentTab.value) {
    case 'gold':
      return '금 시세'
    case 'oil':
      return '석유 도매가'  // 레이블 변경
    case 'carbon':
      return 'KAU24 탄소배출권 시세'
  }
}

// Y축 레이블 가져오기
const getYAxisLabel = () => {
  switch (currentTab.value) {
    case 'gold':
      return '원/g'
    case 'oil':
      return '원/L'
    case 'carbon':
      return '원/톤'
  }
}

// 가격 포맷팅
const formatPrice = (price) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'decimal',
    maximumFractionDigits: 2
  }).format(price)
}

// 가격 변동에 따른 색상
const getPriceChangeColor = () => {
  if (!priceChange.value) return 'text-gray-900'
  return priceChange.value > 0 ? 'text-red-600' : priceChange.value < 0 ? 'text-blue-600' : 'text-gray-900'
}

// 탭 변경 감시
watch(currentTab, () => {
  processAndUpdateChart()
})

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
input[type="date"] {
  min-width: 160px;
  position: relative;
  cursor: pointer;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  padding: 4px;
  opacity: 0;
  width: 100%;
  height: 100%;
}

/* 모바일 대응 */
@media (max-width: 640px) {
  input[type="date"] {
    width: 100%;
  }
  
  .date-range-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
  
  .quick-periods {
    margin-top: 1rem;
    justify-content: flex-start;
  }
}

/* 다크모드 대응 */
@media (prefers-color-scheme: dark) {
  input[type="date"] {
    background-color: rgb(255, 255, 255);
    border-color: rgb(209, 213, 219);
  }
}

/* 탭 버튼 호버 효과 */
.tab-button {
  position: relative;
  overflow: hidden;
}

.tab-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: currentColor;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.tab-button:hover::after {
  width: 100%;
}

/* 활성 탭 효과 */
.tab-button.active {
  position: relative;
}

.tab-button.active::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: currentColor;
  opacity: 0.1;
  border-radius: inherit;
}

/* 이모티콘 애니메이션 */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

button:hover .text-xl {
  animation: bounce 0.5s ease infinite;
}

/* 활성 탭의 이모티콘 크기 증가 */
button.active .text-xl {
  transform: scale(1.2);
  transition: transform 0.2s ease;
}
</style> 