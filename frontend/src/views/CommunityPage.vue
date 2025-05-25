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
          @click="handleWriteClick" 
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          글쓰기
        </button>
      </div>

      <!-- 검색 바 -->
      <div class="mb-6">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="게시글 제목 검색..."
            class="w-full px-4 py-2 pr-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 placeholder-gray-500"
            @input="handleSearch"
          />
          <svg
            class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
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
          v-for="article in paginatedArticles"
          :key="article.id"
          :article="article"
          @click="openDetailModal(article)"
          class="transform hover:scale-[1.02] transition-transform duration-200"
        />
        
        <!-- 게시글이 없을 때 메시지 -->
        <div 
          v-if="articles.length === 0" 
          class="text-center py-12 bg-white rounded-lg shadow-sm"
        >
          <svg
            class="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">게시글이 없습니다</h3>
          <p class="mt-1 text-sm text-gray-500">
            {{ auth.isAuthenticated ? '첫 번째 게시글을 작성해보세요!' : '로그인하여 첫 번째 게시글을 작성해보세요!' }}
          </p>
          <div class="mt-6">
            <button
              v-if="auth.isAuthenticated"
              @click="handleWriteClick"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg
                class="-ml-1 mr-2 h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              글쓰기
            </button>
            <button
              v-else
              @click="handleWriteClick"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              로그인하여 글쓰기
            </button>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div v-if="filteredArticles.length > itemsPerPage" class="mt-8 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button
            :disabled="currentPage === 1"
            @click="handlePageChange(currentPage - 1)"
            class="px-4 py-2 rounded-lg border border-gray-300 hover:bg-blue-50 text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            이전
          </button>
          <div class="flex space-x-2">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="handlePageChange(page)"
              :class="[
                'px-4 py-2 rounded-lg transition-colors duration-200',
                currentPage === page
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'border border-gray-300 text-gray-700 hover:bg-blue-50'
              ]"
            >
              {{ page }}
            </button>
          </div>
          <button
            :disabled="currentPage === totalPages"
            @click="handlePageChange(currentPage + 1)"
            class="px-4 py-2 rounded-lg border border-gray-300 hover:bg-blue-50 text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            다음
          </button>
        </nav>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleFormModal from '@/components/ArticleFormModal.vue'
import ArticleDetailModal from '@/components/ArticleDetailModal.vue'
import { articleService } from '@/services/articleService'
import { debounce } from 'lodash'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const articles = ref([])
const isCreateModalOpen = ref(false)
const selectedArticle = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 10
const router = useRouter()

// 페이지 변경 시 스크롤 처리
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// 검색어에 따른 필터링
const filteredArticles = computed(() => {
  if (!searchQuery.value) return articles.value
  const query = searchQuery.value.toLowerCase()
  return articles.value.filter(article => 
    article.title.toLowerCase().includes(query)
  )
})

// 페이지네이션 계산
const totalPages = computed(() => 
  Math.ceil(filteredArticles.value.length / itemsPerPage)
)

// 현재 페이지의 게시글
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredArticles.value.slice(start, end)
})

// 검색어 변경 시 첫 페이지로 이동
watch(searchQuery, () => {
  currentPage.value = 1
})

// 검색 처리 (디바운스 적용)
const handleSearch = debounce(() => {
  currentPage.value = 1
}, 300)

// 게시글 목록 조회
const fetchArticles = async () => {
  try {
    const response = await articleService.getArticles()
    articles.value = response.results
  } catch (error) {
    console.error('게시글 목록 조회 실패:', error)
    articles.value = [] // 에러 발생 시 빈 배열로 초기화
  }
}

// 게시글 생성
const createArticle = async (articleData) => {
  try {
    await articleService.createArticle(articleData)
    closeCreateModal()
    // 성공적으로 게시글을 생성한 후에만 목록을 새로고침
    try {
      const response = await articleService.getArticles()
      articles.value = response.results || []
    } catch (error) {
      console.log('게시글 목록 새로고침 중 오류가 발생했습니다.')
      // 오류가 발생해도 사용자에게는 게시글이 생성되었다는 것을 알림
      articles.value = []
    }
  } catch (error) {
    console.error('게시글 생성 실패:', error)
    // 게시글 생성 실패 시 사용자에게 알림
    alert('게시글 생성에 실패했습니다. 다시 시도해주세요.')
  }
}

// 게시글 수정
const updateArticle = async (articleData) => {
  try {
    await articleService.updateArticle(selectedArticle.value.id, articleData)
    closeDetailModal()
    // 성공적으로 게시글을 수정한 후에만 목록을 새로고침
    try {
      const response = await articleService.getArticles()
      articles.value = response.results || []
    } catch (error) {
      console.log('게시글 목록 새로고침 중 오류가 발생했습니다.')
      articles.value = []
    }
  } catch (error) {
    console.error('게시글 수정 실패:', error)
    alert('게시글 수정에 실패했습니다. 다시 시도해주세요.')
  }
}

// 게시글 삭제
const deleteArticle = async (articleId) => {
  try {
    await articleService.deleteArticle(articleId)
    closeDetailModal()
    // 성공적으로 게시글을 삭제한 후에만 목록을 새로고침
    try {
      const response = await articleService.getArticles()
      articles.value = response.results || []
    } catch (error) {
      console.log('게시글 목록 새로고침 중 오류가 발생했습니다.')
      articles.value = []
    }
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    alert('게시글 삭제에 실패했습니다. 다시 시도해주세요.')
  }
}

// 모달 컨트롤
const openCreateModal = () => {
  isCreateModalOpen.value = true
}

const handleWriteClick = () => {
  if (!auth.isAuthenticated) {
    // 현재 페이지 URL을 저장하여 로그인 후 돌아올 수 있도록 함
    router.push({ 
      name: 'Login', 
      query: { redirect: router.currentRoute.value.fullPath }
    })
    return
  }
  openCreateModal()
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