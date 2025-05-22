<template>
  <div class="dashboard-view">
    <div
      v-motion
      :key="'community-content'"
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-6xl mx-auto px-4 py-12"
    >
    <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900">
          금융 커뮤니티
        </h1>
      </div>        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <!-- 금융상품 금리비교 컴포넌트 -->
          <div 
            v-motion
            :initial="{ opacity: 0, x: -40 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="400"
            class="bg-white rounded-xl shadow-sm"
          >
            <InterestRateComparison />
          </div>
          
          <!-- 관심종목 검색 위젯 -->
          <div 
            v-motion
            :initial="{ opacity: 0, x: 40 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="500"
            class="bg-white rounded-xl shadow-sm"
          >
            <StockSearchWidget />
          </div>
        </div>

        <!-- 귀금속 시세 차트 -->
        <div 
          v-motion
          :initial="{ opacity: 0, y: 40 }"
          :enter="{ opacity: 1, y: 0 }"
          :delay="600"
          class="bg-white rounded-xl shadow-sm"
        >
          <PreciousMetalChart />
        </div>
      </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import InterestRateComparison from '../components/InterestRateComparison.vue'
import StockSearchWidget from '../components/StockSearchWidget.vue'
import PreciousMetalChart from '../components/PreciousMetalChart.vue'

const route = useRoute()

const navItems = [
  { name: '금융', path: '/dashboard' },
  { name: '추천', path: '/recommend' },
  { name: '커뮤니티', path: '/community' },
  { name: '마이데이터', path: '/mydata' }
]

const isCurrentPath = (path) => {
  return route.path === path
}
</script>

<style scoped>
.dashboard-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}

.shadow-sm {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
</style> 