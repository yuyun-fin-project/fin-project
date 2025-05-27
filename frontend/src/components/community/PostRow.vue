<template>
  <tr class="hover:bg-gray-50 transition">
    <td class="px-6 py-4">{{ rowIndex }}</td>
    <td class="px-6 py-4">
      <RouterLink :to="`/community/${post.id}`" class="text-blue-600 hover:underline">
        {{ post.title }}
      </RouterLink>
    </td>
    <td class="px-6 py-4">{{ post.author }}</td>
    <td class="px-6 py-4">{{ formatDate(post.createdAt) }}</td>
    <td class="px-6 py-4">{{ post.views }}</td>
  </tr>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps<{
  post: {
    id: number
    title: string
    author: string
    createdAt: string
    views: number
  }
  rowIndex: number
}>()

function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>
