<template>
  <div class="my-page">
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      class="max-w-6xl mx-auto px-4 py-12"
    >
      <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
        마이페이지
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 프로필 섹션 -->
        <user-profile 
          :user="user"
          :article-count="myArticles.length"
          :bookmark-count="bookmarkCount"
        />

        <!-- 내가 쓴 글 섹션 -->
        <my-articles 
          :articles="myArticles" 
          @refresh="fetchMyArticles"
        />

        <!-- 회원 정보 수정 섹션 -->
        <profile-edit-preview />

        <!-- 찜한 금융상품 섹션 -->
        <favorite-products-preview />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { articleService, api } from '@/services/articleService'
import UserProfile from '@/components/profile/UserProfile.vue'
import MyArticles from '@/components/profile/MyArticles.vue'
import ProfileEditPreview from '@/components/profile/ProfileEditPreview.vue'
import FavoriteProductsPreview from '@/components/profile/FavoriteProductsPreview.vue'
import { useModalStore } from '../stores/modalStore'
import eventBus from '../utils/eventBus'

const auth = useAuthStore()
const modalStore = useModalStore()
const user = ref({})
const myArticles = ref([])
const bookmarkCount = ref(0)

const fetchUserData = async () => {
  try {
    if (!auth.user?.id) {
      return
    }
    const response = await api.get(`/accounts/profile/${auth.user.id}/`)
    user.value = response.data
  } catch (error) {
    // 오류 발생 시 기본 사용자 정보 설정
    user.value = { 
      id: auth.user?.id, 
      nickname: auth.user?.nickname || '사용자',
      username: auth.user?.useremail,
      email: auth.user?.email
    }
  }
}

const fetchMyArticles = async () => {
  try {
    const response = await articleService.getArticles()
    myArticles.value = response.results.filter(article => article.user_id === auth.user.id)
  } catch (error) {
    myArticles.value = []
  }
}

const fetchBookmarkCount = async () => {
  try {
    if (!auth.user?.id) {
      return
    }
    const response = await api.get(`/finrecom/bookmark/product/`)
    bookmarkCount.value = response.data.length
    // 초기 북마크 수 이벤트 발생
    eventBus.emit('bookmark-count-updated', bookmarkCount.value)
  } catch (error) {
    bookmarkCount.value = 0
    eventBus.emit('bookmark-count-updated', 0)
  }
}

onMounted(async () => {
  if (!auth.user?.id) {
    return
  }
  
  await Promise.all([
    fetchUserData(),
    fetchMyArticles(),
    fetchBookmarkCount()
  ])
  
  // 모달 스토어 구독
  modalStore.$subscribe((mutation, state) => {
    if (mutation.type === 'closeModal') {
      fetchMyArticles()
      fetchBookmarkCount()
    }
  })
})
</script>

<style scoped>
.my-page {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem;
  padding-top: 5rem;
}

.mypage-container {
  @apply container mx-auto px-4 py-8;
}

.profile-section {
  @apply bg-white rounded-lg shadow-md p-6 mb-8;
}
</style> 