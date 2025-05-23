<template>
  <div 
    class="article-card bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer border border-gray-100"
    @click="$emit('click')"
  >
    <h2 class="text-xl font-semibold text-gray-900 mb-3">{{ article.title }}</h2>
    <p class="text-gray-600 mb-4 line-clamp-2 text-sm">{{ article.content }}</p>
    <div class="flex justify-between items-center text-sm text-gray-500">
      <div class="flex items-center space-x-2">
        <span class="flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          {{ article.user?.nickname || '익명' }}
        </span>
      </div>
      <span class="flex items-center">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ formatDate(article.created_at) }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const formatDate = (dateString) => {
  if (!dateString) return '날짜 없음'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script> 