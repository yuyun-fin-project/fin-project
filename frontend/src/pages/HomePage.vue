<template>
  <div class="home-page">
    <Suspense>
      <template #default>
        <div>
          <HeroSection />
          <!-- 앞으로 여기에 FeatureCard, 자산 분석, 추천 추가 예정 -->
        </div>
      </template>
      <template #fallback>
        <div class="loading">
          <div class="loading-spinner"></div>
        </div>
      </template>
    </Suspense>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import HeroSection from '../components/HeroSection.vue'

// Simulate async setup for consistency with other pages
await new Promise(resolve => setTimeout(resolve, 0));
</script>

<style scoped>
.home-page {
  @apply min-h-screen;
}

.loading {
  @apply flex items-center justify-center min-h-[200px];
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}
</style>
