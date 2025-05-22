<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-900">귀금속 시세</h2>
      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-3">
          <div class="relative date-input-container">
            <label class="absolute -top-2 left-2 text-xs bg-white px-1 text-gray-500">시작일</label>
            <input
              type="date"
              v-model="startDate"
              :max="endDate"
              min="2023-01-09"
              max="2024-12-01"
              class="px-4 py-2.5 pr-8 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700 appearance-none cursor-pointer hover:border-gray-300 transition-colors w-[160px]"
            />
            <span class="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
              </svg>
            </span>
          </div>
          <span class="text-gray-400">~</span>
          <div class="relative date-input-container">
            <label class="absolute -top-2 left-2 text-xs bg-white px-1 text-gray-500">종료일</label>
            <input
              type="date"
              v-model="endDate"
              :min="startDate"
              min="2023-01-09"
              max="2024-12-01"
              class="px-4 py-2.5 pr-8 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700 appearance-none cursor-pointer hover:border-gray-300 transition-colors w-[160px]"
            />
            <span class="absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
              </svg>
            </span>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="selectAsset('gold')"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              selectedAsset === 'gold'
                ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            금
          </button>
          <button
            @click="selectAsset('silver')"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              selectedAsset === 'silver'
                ? 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            은
          </button>
        </div>
      </div>
    </div>
    
    <div class="flex-1 relative min-h-[350px] pb-4">
      <div ref="chartContainer" class="absolute inset-0"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { read, utils } from 'xlsx'

const chartContainer = ref(null)
const chart = ref(null)
const startDate = ref('2023-01-09')
const endDate = ref('2024-12-01')
const selectedAsset = ref('gold')
const priceData = ref({
  gold: [],
  silver: []
})
const isLoading = ref(true)

// 차트 리사이즈 핸들러
const handleResize = () => {
  if (chart.value && !chart.value.isDisposed()) {
    chart.value.resize()
  }
}

// 차트 초기화
const initChart = () => {
  if (!chartContainer.value) return
  
  try {
    if (chart.value) {
      chart.value.dispose()
      chart.value = null
    }
    
    chart.value = echarts.init(chartContainer.value)
    
    // 기본 옵션 설정
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
        }
      },
      xAxis: {
        type: 'time',
        boundaryGap: false,
        axisLabel: {
          margin: 12,
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          margin: 16,
          formatter: (value) => `${value.toLocaleString()}`
        }
      },
      series: [
        {
          type: 'line',
          data: [],
          smooth: true
        }
      ]
    }

    chart.value.setOption(baseOption)
  } catch (error) {
    console.error('Error initializing chart:', error)
    chart.value = null
  }
}

// 차트 업데이트
const updateChart = () => {
  if (!chart.value) {
    console.warn('Chart not initialized')
    return
  }

  if (!priceData.value[selectedAsset.value]?.length) {
    console.warn('No data available for', selectedAsset.value)
    return
  }

  try {
    const startDateTime = new Date(startDate.value + 'T00:00:00')
    const endDateTime = new Date(endDate.value + 'T23:59:59')

    // 선택된 날짜 범위에 맞는 데이터만 필터링
    const filteredData = priceData.value[selectedAsset.value].filter(item => {
      const itemDate = new Date(item.date)
      return itemDate >= startDateTime && itemDate <= endDateTime
    })

    if (filteredData.length === 0) {
      console.warn('No data available for selected date range')
      return
    }

    // 최저가와 최고가 계산
    const prices = filteredData.map(item => item.close)
    const minPrice = Math.min(...prices)
    const maxPrice = Math.max(...prices)
    const priceDiff = maxPrice - minPrice
    
    // y축 범위 설정 (여유 공간 10% 추가)
    const yAxisMin = Math.floor(minPrice - (priceDiff * 0.1))
    const yAxisMax = Math.ceil(maxPrice + (priceDiff * 0.1))

    const option = {
      grid: {
        left: '5%',
        right: '5%',
        bottom: '15%',
        top: '5%',
        containLabel: true
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          animation: true,
          label: {
            backgroundColor: '#6a7985'
          }
        },
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e5e7eb',
        borderWidth: 1,
        textStyle: {
          color: '#374151'
        },
        padding: [8, 12],
        formatter: (params) => {
          const date = new Date(params[0].data[0]).toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          })
          const price = params[0].data[1].toLocaleString()
          const color = selectedAsset.value === 'gold' ? '#F59E0B' : '#94A3B8'
          
          return `
            <div class="font-medium">
              <span style="color: #6B7280">${date}</span><br/>
              <span style="color: ${color}; font-size: 1.1em">
                ${selectedAsset.value === 'gold' ? '금' : '은'} 시세: 
                <span style="font-weight: 600">${price}원/g</span>
              </span>
            </div>
          `
        }
      },
      xAxis: {
        type: 'time',
        boundaryGap: false,
        min: startDateTime.getTime(),
        max: endDateTime.getTime(),
        axisLabel: {
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
          },
          color: '#6B7280'
        },
        axisLine: {
          lineStyle: {
            color: '#e5e7eb'
          }
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f3f4f6',
            type: 'dashed'
          }
        }
      },
      yAxis: {
        type: 'value',
        name: '가격 (원/g)',
        nameLocation: 'middle',
        nameGap: 50,
        nameTextStyle: {
          color: '#6B7280',
          padding: [0, 0, 20, 0]
        },
        min: yAxisMin,
        max: yAxisMax,
        axisLabel: {
          formatter: (value) => `${value.toLocaleString()}`,
          color: '#6B7280'
        },
        axisLine: {
          lineStyle: {
            color: '#e5e7eb'
          }
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f3f4f6',
            type: 'dashed'
          }
        }
      },
      series: [
        {
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          showSymbol: false,
          emphasis: {
            scale: true,
            showSymbol: true
          },
          data: filteredData.map(item => [
            new Date(item.date).getTime(),
            item.close
          ]),
          itemStyle: {
            color: selectedAsset.value === 'gold' ? '#F59E0B' : '#94A3B8',
            borderWidth: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: selectedAsset.value === 'gold' 
                  ? 'rgba(245, 158, 11, 0.3)' 
                  : 'rgba(148, 163, 184, 0.3)'
              },
              {
                offset: 1,
                color: 'rgba(255, 255, 255, 0.1)'
              }
            ])
          }
        }
      ]
    }

    chart.value.setOption(option, true)
  } catch (error) {
    console.error('Error updating chart:', error)
  }
}

// 데이터 로드
const loadData = async (type) => {
  try {
    const response = await fetch(`/src/assets/data/${type === 'gold' ? 'Gold' : 'Silver'}_prices.xlsx`)
    const arrayBuffer = await response.arrayBuffer()
    const workbook = read(arrayBuffer)
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    const data = utils.sheet_to_json(worksheet, { 
      raw: false
    })
    
    console.log(`Raw ${type} data:`, data[0]); // 데이터 확인용 로그

    priceData.value[type] = data.map(row => {
      // 날짜 파싱 (M/D/YY 형식)
      const [month, day, year] = row.Date.split('/')
      const parsedDate = new Date(
        2000 + parseInt(year), // 2000년대 가정
        parseInt(month) - 1,   // 월 (0-based)
        parseInt(day)          // 일
      )

      // 숫자 데이터 파싱 (쉼표 제거 후 숫자로 변환)
      const parseNumber = (value) => {
        if (typeof value === 'string') {
          return parseFloat(value.replace(/,/g, ''))
        }
        return parseFloat(value)
      }

      return {
        date: parsedDate,
        close: parseNumber(row['Close/Last']),
        volume: parseNumber(row.Volume),
        open: parseNumber(row.Open),
        high: parseNumber(row.High),
        low: parseNumber(row.Low)
      }
    }).sort((a, b) => a.date - b.date)

    // 데이터 로드 후 시작일과 종료일 설정
    if (priceData.value[type].length > 0) {
      const dates = priceData.value[type].map(item => item.date)
      const minDate = new Date(Math.min(...dates))
      const maxDate = new Date(Math.max(...dates))
      
      // 날짜를 YYYY-MM-DD 형식으로 변환
      const formatDate = (date) => {
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        return `${year}-${month}-${day}`
      }

      startDate.value = formatDate(minDate)
      endDate.value = formatDate(maxDate)
    }

    console.log(`Processed ${type} data:`, {
      firstDate: priceData.value[type][0]?.date,
      lastDate: priceData.value[type][priceData.value[type].length - 1]?.date,
      totalPoints: priceData.value[type].length
    });
  } catch (error) {
    console.error(`Error loading ${type} price data:`, error)
  }
}

// 이벤트 핸들러
const selectAsset = (asset) => {
  selectedAsset.value = asset
  updateChart()
}

// 날짜 변경 시 즉시 차트 업데이트
watch([startDate, endDate], () => {
  nextTick(() => {
    updateChart()
  })
})

// 자산 선택 시 차트 업데이트
watch(selectedAsset, () => {
  nextTick(() => {
    updateChart()
  })
})

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  isLoading.value = true
  try {
    // 먼저 데이터 로드
    await Promise.all([
      loadData('gold'),
      loadData('silver')
    ])
    
    // 차트 초기화 및 데이터 업데이트
    await nextTick()
    initChart()
    
    if (chart.value) {
      window.addEventListener('resize', handleResize)
      await nextTick()
      updateChart()
    }
  } catch (error) {
    console.error('Error initializing chart:', error)
  } finally {
    isLoading.value = false
  }
})

// 컴포넌트 언마운트 시 정리
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chart.value) {
    chart.value.dispose()
    chart.value = null
  }
})
</script>

<style scoped>
.candlestick-chart {
  width: 100%;
  height: 100%;
}

/* 차트 컨테이너 스타일 */
#chartContainer {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.date-input-container {
  position: relative;
}

/* 날짜 선택 input의 기본 스타일 제거 및 커스텀 스타일 적용 */
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

/* 호버 효과 */
.date-input-container:hover input {
  border-color: #9ca3af;
}

/* 라벨 스타일 */
.date-input-container label {
  z-index: 1;
  transition: all 0.2s ease;
}

.date-input-container input:focus + label {
  color: #3b82f6;
}
</style> 