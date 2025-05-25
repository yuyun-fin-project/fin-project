<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <!-- 헤더 영역 -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-900">시세 차트</h2>
      <div class="flex items-center space-x-4">
        <!-- 날짜 선택 -->
        <div class="flex items-center space-x-3">
          <div class="relative date-input-container">
            <label class="absolute -top-2 left-2 text-xs bg-white px-1 text-gray-500">시작일</label>
            <input
              type="date"
              v-model="startDate"
              :max="endDate"
              class="px-4 py-2.5 pr-8 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700 appearance-none cursor-pointer hover:border-gray-300 transition-colors w-[160px]"
            />
          </div>
          <span class="text-gray-400">~</span>
          <div class="relative date-input-container">
            <label class="absolute -top-2 left-2 text-xs bg-white px-1 text-gray-500">종료일</label>
            <input
              type="date"
              v-model="endDate"
              :min="startDate"
              class="px-4 py-2.5 pr-8 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700 appearance-none cursor-pointer hover:border-gray-300 transition-colors w-[160px]"
            />
          </div>
        </div>
        <!-- 자산 선택 버튼 -->
        <div class="flex items-center space-x-2">
          <button
            v-for="asset in assets"
            :key="asset.value"
            @click="selectAsset(asset.value)"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              selectedAsset === asset.value
                ? asset.activeClass
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ asset.label }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex-1 flex items-center justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="flex-1 flex items-center justify-center text-red-600">
      {{ error }}
    </div>

    <!-- 차트 -->
    <div v-else class="flex-1 relative min-h-[350px]">
      <div ref="chartContainer" class="absolute inset-0"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

// 상태 관리
const chartContainer = ref(null)
const chart = ref(null)
const isLoading = ref(false)
const error = ref(null)
const startDate = ref(getDefaultStartDate())
const endDate = ref(getDefaultEndDate())
const selectedAsset = ref('gold')

// 자산 정의
const assets = [
  { value: 'gold', label: '금', activeClass: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200' },
  { value: 'oil', label: '석유', activeClass: 'bg-blue-100 text-blue-800 hover:bg-blue-200' },
  { value: 'carbon', label: '탄소', activeClass: 'bg-green-100 text-green-800 hover:bg-green-200' }
]

// 기본 날짜 설정 함수
function getDefaultStartDate() {
  const date = new Date()
  date.setMonth(date.getMonth() - 1)
  return date.toISOString().split('T')[0]
}

function getDefaultEndDate() {
  return new Date().toISOString().split('T')[0]
}

// 차트 리사이즈 핸들러
const handleResize = () => {
  if (chart.value && !chart.value.isDisposed()) {
    chart.value.resize()
  }
}

// 데이터 가져오기
const fetchData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const formattedStartDate = startDate.value.replace(/-/g, '')
    const formattedEndDate = endDate.value.replace(/-/g, '')
    
    // API 호출
    let response
    try {
      response = await axios.get('/finrecom/spot/', {
        params: {
          start_date: formattedStartDate,
          end_date: formattedEndDate,
          type: selectedAsset.value.toLowerCase() // 소문자로 변환
        }
      })

      console.log('API 전체 응답:', response)
      console.log('응답 데이터 구조:', {
        data: response.data,
        type: typeof response.data,
        keys: Object.keys(response.data || {})
      })
    } catch (apiError) {
      console.error('API 호출 실패:', apiError)
      if (apiError.response?.status === 500) {
        error.value = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      } else {
        error.value = '데이터를 불러오는데 실패했습니다.'
      }
      return
    }

    // 데이터 구조 확인 및 처리
    if (!response.data) {
      throw new Error('API 응답이 없습니다.')
    }

    let rawData = response.data
    console.log('원본 데이터:', rawData)

    // items 객체에서 데이터 추출
    let chartData
    if (rawData.items) {
      const assetKey = selectedAsset.value.toLowerCase()
      chartData = rawData.items[assetKey] || []
      
      // 응답 데이터가 response.body.items.item 구조인 경우 처리
      if (chartData.response?.body?.items?.item) {
        chartData = chartData.response.body.items.item
      }
      
      console.log('선택된 자산:', assetKey)
      console.log('추출된 데이터:', chartData)
    } else {
      console.warn('items 객체를 찾을 수 없음:', rawData)
      chartData = []
    }

    if (!Array.isArray(chartData)) {
      console.error('처리된 데이터가 배열이 아님:', chartData)
      throw new Error('데이터를 처리할 수 없는 형식입니다.')
    }

    if (chartData.length === 0) {
      error.value = '선택한 기간에 데이터가 없습니다.'
      return
    }

    updateChart(chartData)
  } catch (err) {
    console.error('시세 데이터 처리 실패:', err)
    error.value = '데이터 처리 중 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 차트 초기화
const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    if (chart.value && !chart.value.isDisposed()) {
      chart.value.dispose()
    }
    
    chart.value = echarts.init(chartContainer.value)
    
    // 차트 기본 옵션 설정
    const baseOption = {
      grid: {
        left: '8%',
        right: '5%',
        bottom: '12%',
        top: '5%',
        containLabel: true
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        formatter: (params) => {
          const date = new Date(params[0].value[0])
          const formattedDate = `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
          const value = params[0].value[1].toLocaleString('ko-KR')
          return `${formattedDate}<br/>${params[0].seriesName}: ${value}원`
        }
      },
      xAxis: {
        type: 'time',
        boundaryGap: false,
        axisLabel: {
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}.${date.getDate()}`
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: (value) => `${value.toLocaleString('ko-KR')}`
        },
        scale: true
      },
      series: [
        {
          name: getAssetLabel(selectedAsset.value),
          type: 'line',
          data: [],
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            width: 2
          },
          itemStyle: {
            color: getAssetColor(selectedAsset.value)
          }
        }
      ]
    }

    chart.value.setOption(baseOption)
  } catch (error) {
    console.error('차트 초기화 실패:', error)
    chart.value = null
  }
}

// 차트 업데이트
const updateChart = (data) => {
  if (!chart.value || chart.value.isDisposed()) {
    initChart()
  }

  try {
    console.log('차트 데이터 포맷팅 전:', data)

    // 데이터 포맷팅
    const formattedData = data
      .filter(item => {
        // 필수 필드 확인
        const hasDate = item && item.basDt
        const hasPrice = selectedAsset.value === 'Oil' 
          ? item.wtAvgPrcCptn !== undefined || item.wt_avg_prc_cptn !== undefined
          : item.clpr !== undefined
        return hasDate && hasPrice
      })
      .map(item => {
        // 날짜 변환 (YYYYMMDD 형식)
        const dateStr = item.basDt
        const date = new Date(
          dateStr.substring(0, 4),
          parseInt(dateStr.substring(4, 6)) - 1,
          dateStr.substring(6, 8)
        )

        // 가격 데이터 추출
        let price
        if (selectedAsset.value === 'Oil') {
          price = parseFloat(item.wtAvgPrcCptn || item.wt_avg_prc_cptn)
        } else {
          price = parseFloat(item.clpr)
        }

        // 등락률 추출
        const change = selectedAsset.value !== 'Oil'
          ? parseFloat(item.fltRt || item.flt_rt)
          : null

        return [date.getTime(), price, change]
      })
      .sort((a, b) => a[0] - b[0])

    console.log('포맷팅된 데이터:', formattedData)

    if (formattedData.length === 0) {
      error.value = '선택한 기간에 데이터가 없습니다.'
      return
    }

    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        formatter: (params) => {
          const date = new Date(params[0].value[0])
          const formattedDate = `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
          const value = params[0].value[1].toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })
          const unit = selectedAsset.value === 'Oil' ? '원/L' : '원/g'
          const change = params[0].value[2] !== null
            ? `<br/>등락률: ${params[0].value[2] > 0 ? '+' : ''}${params[0].value[2].toFixed(2)}%`
            : ''
          return `${formattedDate}<br/>${params[0].seriesName}: ${value}${unit}${change}`
        }
      },
      xAxis: {
        type: 'time',
        boundaryGap: false,
        axisLabel: {
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}.${date.getDate()}`
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: (value) => {
            return value.toLocaleString('ko-KR', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })
          }
        },
        scale: true
      },
      series: [{
        name: getAssetLabel(selectedAsset.value),
        type: 'line',
        data: formattedData.map(item => {
          const [timestamp, price, change] = item
          const dataItem = selectedAsset.value === 'Oil' 
            ? [timestamp, price]
            : [timestamp, price, change]
          return dataItem
        }),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3
        },
        itemStyle: {
          color: getAssetColor(selectedAsset.value),
          borderWidth: 2,
          borderColor: '#fff',
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 4
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: getAssetColor(selectedAsset.value) + 'CC' // 시작 색상 (80% 투명도)
            }, {
              offset: 1,
              color: getAssetColor(selectedAsset.value) + '11' // 끝 색상 (7% 투명도)
            }]
          }
        }
      }]
    }

    chart.value.setOption(option)
  } catch (error) {
    console.error('차트 데이터 업데이트 실패:', error)
    error.value = '차트 업데이트 중 오류가 발생했습니다.'
  }
}

// 자산 관련 헬퍼 함수
const getAssetLabel = (asset) => {
  const assetMap = {
    Gold: '금 시세 (1Kg)',
    Oil: '석유 시세 (1L)',
    Carbon: '탄소 시세 (1톤)'
  }
  return assetMap[asset] || asset
}

const getAssetColor = (asset) => {
  const colorMap = {
    Gold: '#FFB800',    // 금색
    Oil: '#3B82F6',     // 파란색
    Carbon: '#10B981'   // 녹색
  }
  return colorMap[asset] || '#94A3B8'
}

// 자산 선택
const selectAsset = (asset) => {
  const assetTypeMap = {
    gold: 'Gold',
    oil: 'Oil',
    carbon: 'Carbon'
  }
  selectedAsset.value = assetTypeMap[asset] || asset
  fetchData()
}

// 날짜 변경 감시
watch([startDate, endDate], () => {
  fetchData()
})

// 컴포넌트 라이프사이클 훅
onMounted(async () => {
  await nextTick()
  initChart()
  window.addEventListener('resize', handleResize)
  fetchData()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chart.value) {
    chart.value.dispose()
    chart.value = null
  }
})
</script>

<style scoped>
.date-input-container {
  position: relative;
}

input[type="date"] {
  position: relative;
  background-color: transparent;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

input[type="date"]::-webkit-datetime-edit {
  color: #374151;
  font-size: 0.875rem;
  padding: 0;
}

input[type="date"]::-webkit-datetime-edit-fields-wrapper {
  padding: 0;
  display: flex;
  align-items: center;
}

input[type="date"]::-webkit-datetime-edit-year-field,
input[type="date"]::-webkit-datetime-edit-month-field,
input[type="date"]::-webkit-datetime-edit-day-field {
  padding: 0 2px;
}

input[type="date"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.date-input-container:hover input {
  border-color: #9ca3af;
}
</style> 