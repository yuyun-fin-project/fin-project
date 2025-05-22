<template>
  <div class="ai-view">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-4xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        AI 투자 추천
      </h1>

      <div v-if="!isReady" class="loading">
        <div class="loading-spinner"></div>
      </div>

      <div v-else>
        <!-- 투자 성향 분석 섹션 -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 class="text-2xl font-semibold mb-4">나의 투자 성향</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-blue-50 p-4 rounded-lg">
              <p class="text-sm text-gray-600">위험 선호도</p>
              <p class="text-xl font-bold text-blue-600">{{ store.userProfile.riskLevel }}</p>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
              <p class="text-sm text-gray-600">투자 기간</p>
              <p class="text-xl font-bold text-blue-600">{{ store.userProfile.period }}</p>
            </div>
            <div class="bg-blue-50 p-4 rounded-lg">
              <p class="text-sm text-gray-600">월 투자 금액</p>
              <p class="text-xl font-bold text-blue-600">{{ store.userProfile.monthlyInvestment }}</p>
            </div>
          </div>
        </div>

        <!-- AI 추천 포트폴리오 -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 class="text-2xl font-semibold mb-6">맞춤 포트폴리오 추천</h2>
          <div class="space-y-4">
            <div v-for="(item, index) in store.portfolio" :key="index" 
              class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
              <div>
                <h3 class="font-medium text-gray-900">{{ item.name }}</h3>
                <p class="text-sm text-gray-500">{{ item.description }}</p>
              </div>
              <div class="text-right">
                <p class="font-bold text-blue-600">{{ item.percentage }}%</p>
                <p class="text-sm text-gray-500">추천 비중</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 투자 전략 추천 -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-2xl font-semibold mb-4">투자 전략 제안</h2>
          <div class="prose prose-blue">
            <p class="text-gray-600">
              현재 시장 상황과 고객님의 투자 성향을 분석한 결과, 안정적인 수익을 추구하는 
              포트폴리오를 추천드립니다. 정기적인 분할 투자를 통해 시장 변동성 리스크를 
              줄이는 것이 좋겠습니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useInvestmentStore } from '../stores/investment.js';

const store = useInvestmentStore();
const isReady = ref(false);

// async setup
await store.loadData();
isReady.value = true;
</script>

<style scoped>
.ai-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}

.prose {
  @apply max-w-none;
}

.loading {
  @apply flex items-center justify-center min-h-[200px];
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}
</style>
