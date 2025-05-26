<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">내가 쓴 글</h2>
    <div v-if="articles.length > 0" class="space-y-4">
      <div 
        v-for="article in displayedArticles" 
        :key="article.id"
        class="p-4 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer"
        @click="openDetailModal(article)"
      >
        <h3 class="text-lg font-medium text-gray-900 mb-2">{{ article.title }}</h3>
        <p class="text-sm text-gray-600 line-clamp-2">{{ article.content }}</p>
        <div class="mt-2 text-sm text-gray-500">
          {{ formatDate(article.created_at) }}
        </div>
      </div>

      <!-- 펼치기/접기 버튼 -->
      <div v-if="articles.length > 5" class="text-center mt-4">
        <button
          @click="toggleArticles"
          class="inline-flex items-center px-4 py-2 text-blue-500 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors duration-200 font-medium"
        >
          <span>{{ isExpanded ? '접기' : '펼치기' }}</span>
          <svg
            :class="{'rotate-180': isExpanded}"
            class="w-5 h-5 ml-1 transition-transform duration-200"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
      </div>
    </div>
    <div v-else class="text-center text-gray-500 py-8">
      작성한 글이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { articleService } from '@/services/articleService'
import { useModalStore } from '@/stores/modalStore'

const modalStore = useModalStore()
const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['refresh'])
const isExpanded = ref(false)

// 새로고침 이벤트 리스너 등록
onMounted(() => {
  window.addEventListener('refresh-my-articles', handleRefresh)
})

// 컴포넌트 언마운트 시 이벤트 리스너 제거
onUnmounted(() => {
  window.removeEventListener('refresh-my-articles', handleRefresh)
})

// 새로고침 핸들러
const handleRefresh = () => {
  emit('refresh')
}

// 표시할 게시글 목록
const displayedArticles = computed(() => {
  return isExpanded.value ? props.articles : props.articles.slice(0, 5)
})

const toggleArticles = () => {
  isExpanded.value = !isExpanded.value
}

const formatDate = (dateString) => {
  if (!dateString) return '날짜 없음'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const openDetailModal = (article) => {
  modalStore.openArticleDetailModal(article)
}

const handleDelete = async (articleId) => {
  try {
    await articleService.deleteArticle(articleId)
    modalStore.closeArticleDetailModal()
    emit('refresh') // 부모 컴포넌트에 새로고침 요청
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
  }
}

const handleUpdate = async (articleData) => {
  try {
    await articleService.updateArticle(articleData.id, articleData)
    modalStore.closeArticleDetailModal()
    emit('refresh') // 부모 컴포넌트에 새로고침 요청
  } catch (error) {
    console.error('게시글 수정 실패:', error)
  }
}
</script> 