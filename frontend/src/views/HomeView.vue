<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">금융 대시보드</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- 금융상품 금리비교 컴포넌트 -->
      <div class="aspect-square">
        <InterestRateComparison class="h-full" />
      </div>
      
      <!-- 관심종목 검색 위젯 -->
      <div class="aspect-square">
        <StockSearchWidget class="h-full" />
      </div>
    </div>
  </div>
</template>

<script setup>
import InterestRateComparison from '../components/InterestRateComparison.vue'
import StockSearchWidget from '../components/StockSearchWidget.vue'
</script>

<style scoped>
.aspect-square {
  position: relative;
  width: 100%;
}

.aspect-square > * {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style> 