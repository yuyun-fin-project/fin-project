<template>
  <div class="overflow-x-auto shadow-md rounded-xl">
    <table class="min-w-full divide-y divide-gray-200 bg-white">
      <thead class="bg-gray-100 text-gray-700 text-left text-sm uppercase">
        <tr>
          <th class="px-6 py-3">번호</th>
          <th class="px-6 py-3">제목</th>
          <th class="px-6 py-3">작성자</th>
          <th class="px-6 py-3">날짜</th>
          <th class="px-6 py-3">조회수</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 text-gray-700">
        <PostRow
          v-for="(post, i) in posts"
          :key="post.id"
          :post="post"
          :row-index="startIndex + i + 1"
        />
        <tr v-if="posts.length === 0">
          <td colspan="5" class="text-center px-6 py-4 text-gray-400">게시글이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import PostRow from './PostRow.vue'

defineProps<{
  posts: {
    id: number
    title: string
    author: string
    createdAt: string
    views: number
  }[]
  startIndex: number
}>()
</script>
