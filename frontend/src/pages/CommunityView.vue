<template>
  <div class="community-view">
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
        <button class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
          글쓰기
        </button>
      </div>

      <!-- 검색 바 -->
      <div class="mb-6">
        <div class="relative">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="검색어를 입력하세요" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
      </div>

      <!-- 게시글 목록 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">번호</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">제목</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성자</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성일</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">조회</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="post in paginatedPosts" :key="post.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ post.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ post.title }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ post.author }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ post.createdAt }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ post.views }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 -->
      <div class="mt-6 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button 
            v-for="page in totalPages" 
            :key="page"
            @click="setPage(page)"
            :class="[
              'px-3 py-1 rounded',
              currentPage === page 
                ? 'bg-blue-500 text-white' 
                : 'text-gray-500 hover:bg-gray-100'
            ]"
          >
            {{ page }}
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import PostSearch from '../components/community/PostSearch.vue'
import PostTable from '../components/community/PostTable.vue'
import Pagination from '../components/community/Pagination.vue'

interface Post {
  id: number
  title: string
  author: string
  createdAt: string
  views: number
}

const posts = ref<Post[]>([
  { id: 1, title: '주식 투자 초보자 가이드', author: '투자왕', createdAt: '2024-03-21', views: 128 },
  { id: 2, title: '요즘 HOT한 금융 상품 추천', author: '재테크고수', createdAt: '2024-03-20', views: 256 },
  { id: 3, title: '주간 금융시장 동향', author: '애널리스트', createdAt: '2024-03-19', views: 189 },
  { id: 4, title: '연금저축 상품 비교', author: '미래대비', createdAt: '2024-03-18', views: 145 },
  { id: 5, title: '부동산 투자 전략', author: '부자되기', createdAt: '2024-03-17', views: 267 },
])

const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10

const filteredPosts = computed(() =>
  posts.value.filter(post =>
    post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    post.author.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize))
const startIndex = computed(() => (currentPage.value - 1) * pageSize)

const paginatedPosts = computed(() =>
  filteredPosts.value.slice(startIndex.value, startIndex.value + pageSize)
)

const setPage = (page: number) => {
  currentPage.value = page
}
</script>

<style scoped>
.community-view {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}
</style>
