<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-900">금융상품 금리비교</h2>
      <router-link
        to="/products"
        class="text-sm text-blue-600 hover:text-blue-800 font-medium"
      >
        더 알아보기 →
      </router-link>
    </div>

    <div class="flex-1 flex flex-col">
      <!-- 금리 비교 테이블 -->
      <div class="flex-1 overflow-auto">
        <table class="min-w-full">
          <thead class="sticky top-0 bg-white">
            <tr class="border-b border-gray-200">
              <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">상품명</th>
              <th class="px-4 py-3 text-right text-sm font-semibold text-gray-600">금리</th>
              <th class="px-4 py-3 text-right text-sm font-semibold text-gray-600">기간</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="product in topProducts" :key="product.id">
              <td class="px-4 py-3 text-sm text-gray-900">{{ product.name }}</td>
              <td class="px-4 py-3 text-sm text-right text-blue-600 font-medium">
                {{ product.rate }}%
              </td>
              <td class="px-4 py-3 text-sm text-right text-gray-600">
                {{ product.term }}개월
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 샘플 데이터
const topProducts = ref([
  {
    id: 1,
    name: '우리은행 주택청약종합저축',
    rate: 3.5,
    term: 12
  },
  {
    id: 2,
    name: '신한은행 자유적금',
    rate: 3.3,
    term: 24
  },
  {
    id: 3,
    name: '국민은행 장기저축예금',
    rate: 3.2,
    term: 36
  },
  {
    id: 4,
    name: '하나은행 정기예금',
    rate: 3.1,
    term: 12
  }
])
</script>

<style scoped>
.overflow-auto {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E1 transparent;
}

.overflow-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 3px;
}
</style> 