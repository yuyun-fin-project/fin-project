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
        <user-profile :user="user" />

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
import { articleService } from '@/services/articleService'
import UserProfile from '@/components/profile/UserProfile.vue'
import MyArticles from '@/components/profile/MyArticles.vue'
import ProfileEditPreview from '@/components/profile/ProfileEditPreview.vue'
import FavoriteProductsPreview from '@/components/profile/FavoriteProductsPreview.vue'

const auth = useAuthStore()
const user = ref(null)
const myArticles = ref([])

const fetchUserData = async () => {
  try {
    const userData = await articleService.getUserInfo(auth.user.id)
    user.value = userData
  } catch (error) {
    console.error('사용자 정보 조회 실패:', error)
  }
}

const fetchMyArticles = async () => {
  try {
    const response = await articleService.getArticles()
    myArticles.value = response.results.filter(article => article.user_id === auth.user.id)
  } catch (error) {
    console.error('내가 쓴 글 조회 실패:', error)
  }
}

onMounted(() => {
  fetchUserData()
  fetchMyArticles()
})
</script>

<style scoped>
.my-page {
  @apply min-h-screen bg-gradient-to-b from-blue-50 to-white;
}
</style> 