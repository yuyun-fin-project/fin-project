<template>
  <div class="article-detail-modal">
    <div class="modal-overlay"></div>
    <div 
      v-motion
      :initial="{ opacity: 0, scale: 0.95 }"
      :enter="{ opacity: 1, scale: 1 }"
      :transition="{ type: 'spring', damping: 20, stiffness: 300 }"
      class="modal-content bg-white rounded-xl p-6 w-full max-w-2xl shadow-xl mx-4"
    >
      <div v-if="!isEditing">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-900">{{ props.article.title }}</h2>
          <div class="space-x-2" v-if="isAuthor">
            <button
              @click="startEditing"
              class="px-4 py-2 text-blue-600 hover:text-blue-800 transition-colors"
            >
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                수정
              </span>
            </button>
            <button
              @click="handleDelete"
              class="px-4 py-2 text-red-600 hover:text-red-800 transition-colors"
            >
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                삭제
              </span>
            </button>
          </div>
          <div v-else>
            <div class="space-x-2">
              <button
                @click="likeorUnlike"
                class="px-4 py-2 text-blue-600 hover:text-blue-800 transition-colors"
                v-if="!localIsLiked"
              >
                <span class="flex items-center">좋아요</span>
              </button>

              <button
                @click="likeorUnlike"
                class="px-4 py-2 text-blue-600 hover:text-blue-800 transition-colors"
                v-else
              >
                <span class="flex items-center">좋아요 취소</span>
              </button>
          </div>
        </div>
        </div>

        <div class="mb-6 text-sm text-gray-500 flex items-center space-x-4">
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ props.article.user?.nickname || '익명' }}
          </span>
          <span class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ formatDate(props.article.created_at) }}
          </span>
          <span v-if="props.article.updated_at && props.article.updated_at !== props.article.created_at" class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ formatDate(props.article.updated_at) }}
          </span>
        </div>
        
        <div class="prose max-w-none text-gray-700 mb-8 whitespace-pre-wrap">
          {{ props.article.content }}
        </div>
      </div>
      
      <article-form-modal
        v-else
        :article="props.article"
        @close="cancelEditing"
        @submit="handleUpdate"
      />
      
      <div class="mt-6 flex justify-end">
        <button
          @click="$emit('close')"
          class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          닫기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ArticleFormModal from './ArticleFormModal.vue'
import axios from 'axios'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  is_liked: {
    type: Boolean,
    default: false
  },
})

console.log(props)

const emit = defineEmits(['close', 'delete', 'update'])
const auth = useAuthStore()
const isEditing = ref(false)
const accessToken = ref(localStorage.getItem('access_token'))
const localIsLiked = ref(props.is_liked)

// Update local state when props change
watch(() => props.is_liked, (newVal) => {
  localIsLiked.value = newVal
})

const isAuthor = computed(() => {
  return auth.user?.id === props.article.user?.id
})

const likeorUnlike = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/articles/like/${props.article.id}/`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        }
      }
    )
    // 서버 응답에서 "liked" 필드로 받아오기!
    localIsLiked.value = response.data.liked;
    console.log('Like updated:', response.data);
  } catch (error) {
    console.error('Error updating like:', error);
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.');
    }
  }
}


const formatDate = (dateString) => {
  if (!dateString) return '날짜 없음'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const startEditing = () => {
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
}

const handleDelete = () => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    emit('delete', props.article.id)
  }
}

const handleUpdate = (articleData) => {
  emit('update', {
    id: props.article.id,
    ...articleData
  })
  isEditing.value = false
}


</script> 