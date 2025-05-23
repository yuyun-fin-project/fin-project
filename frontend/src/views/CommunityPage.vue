<template>
  <div class="community-page">
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
          커뮤니티
        </h1>
        <button 
          @click="openCreateModal" 
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          글쓰기
        </button>
      </div>

      <!-- 게시글 목록 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="400"
        class="grid gap-4"
      >
        <article-card
          v-for="article in articles"
          :key="article.id"
          :article="article"
          @click="openDetailModal(article)"
          class="transform hover:scale-[1.02] transition-transform duration-200"
        />
      </div>

      <!-- 글쓰기 모달 -->
      <article-form-modal
        v-if="isCreateModalOpen"
        @close="closeCreateModal"
        @submit="createArticle"
      />

      <!-- 상세보기 모달 -->
      <article-detail-modal
        v-if="selectedArticle"
        :article="selectedArticle"
        @close="closeDetailModal"
        @delete="deleteArticle"
        @update="updateArticle"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleFormModal from '@/components/ArticleFormModal.vue'
import ArticleDetailModal from '@/components/ArticleDetailModal.vue'
import { articleService } from '@/services/articleService'

const auth = useAuthStore()
const articles = ref([])
const isCreateModalOpen = ref(false)
const selectedArticle = ref(null)

// 게시글 목록 조회
const fetchArticles = async () => {
  try {
    const response = await articleService.getArticles()
    articles.value = response.results
  } catch (error) {
    console.error('게시글 목록 조회 실패:', error)
  }
}

// 게시글 생성
const createArticle = async (articleData) => {
  try {
    await articleService.createArticle(articleData)
    await fetchArticles()
    closeCreateModal()
  } catch (error) {
    console.error('게시글 생성 실패:', error)
  }
}

// 게시글 수정
const updateArticle = async (articleData) => {
  try {
    await articleService.updateArticle(selectedArticle.value.id, articleData)
    await fetchArticles()
    closeDetailModal()
  } catch (error) {
    console.error('게시글 수정 실패:', error)
  }
}

// 게시글 삭제
const deleteArticle = async (articleId) => {
  try {
    await articleService.deleteArticle(articleId)
    await fetchArticles()
    closeDetailModal()
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
  }
}

// 모달 컨트롤
const openCreateModal = () => {
  isCreateModalOpen.value = true
}

const closeCreateModal = () => {
  isCreateModalOpen.value = false
}

const openDetailModal = (article) => {
  selectedArticle.value = article
}

const closeDetailModal = () => {
  selectedArticle.value = null
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.community-page {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}
</style> 