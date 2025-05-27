<template>
  <div class="mydata-view">
    <div
      v-motion
      :key="'mydata-content'"
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-4xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        마이데이터 분석
      </h1>
      
      <div class="grid gap-6">
        <HeroSection />
        <CardSummarySection />
        <SpendCalandar class="inline-component" />
        <SpendCalandarGraph class="inline-component" />
        <RecommendGpt />
        <div class="notice-bar">
          공지사항 2021.03.09 18:00부터 22:00까지 시스템 업데이트가 있습니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import HeroSection from '@/components/HeroSection.vue';
import CardSummarySection from '../components/mydata/CardSummarySection.vue'
import SpendCalandar from '../components/mydata/SpendCalandar.vue'
import SpendCalandarGraph from '@/components/mydata/SpendCalandarGraph.vue';
import RecommendGpt from '@/components/mydata/RecommendGpt.vue';
</script>

<style scoped>
.mydata-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}

.dashboard-container {
  padding: 2rem;
  background-color: #f9fafb;
}

.inline-component {
  display: inline-block;
  vertical-align: top;
  margin: 1rem;
}

.notice-bar {
  margin-top: 2rem;
  background-color: #f1f3f5;
  padding: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #333;
  border-radius: 8px;
}
</style>