<template>
  <section class="hero">
    <div class="space-y-6">
      <h1 
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="300"
        :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
        class="mb-4"
      >
        {{ isAuthenticated ? '카드를 연동하고 시작하세요' : '당신의 자산을 더 똑똑하게' }}
      </h1>
      <p 
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="500"
        :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
        class="mb-8"
      >
        {{ isAuthenticated ? '카드를 연동하면 맞춤형 금융 분석을 시작할 수 있어요' : '모든 금융 데이터를 연결해 분석하고 추천까지!' }}
      </p>
      <div class="flex flex-col items-center gap-4">
        <button
          v-motion
          :initial="{ opacity: 0, y: 40 }"
          :enter="{ opacity: 1, y: 0 }"
          :delay="700"
          :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
          class="hover:bg-blue-600 transition-all duration-300 ease-out hover:shadow-xl transform hover:-translate-y-1"
          @click="startMyData"
          :disabled="isLoading"
        >
          {{ getButtonText() }}
        </button>
        <!-- 에러 메시지 표시 -->
        <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated, user } = storeToRefs(authStore)
const isLoading = ref(false)
const error = ref(null)

const API_BASE_URL = 'http://localhost:8000'

const fetchMyData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // 사용자 정보 확인
    if (!user.value) {
      error.value = '사용자 정보를 찾을 수 없습니다. 다시 로그인해주세요.'
      return
    }

    const userEmail = user.value.useremail || user.value.email
    const userName = user.value.nickname || user.value.username

    console.log('사용자 정보:', { email: userEmail, name: userName })
    
    if (!userEmail || !userName) {
      error.value = '사용자 정보를 찾을 수 없습니다. 다시 로그인해주세요.'
      return
    }

    // 현재 로그인된 사용자 정보로 카드 연동 요청
    const connectResponse = await axios.post(`${API_BASE_URL}/mydata/`, {
      "useremail": userEmail,
      "username": userName
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('카드 연동 응답:', connectResponse.data)
    
    // 연동이 성공했다면 바로 마이데이터 분석 페이지로 이동
    if (connectResponse.data) {
      router.push('/mydata/analysis')  // 분석 페이지 경로로 수정
      return
    }

    error.value = '카드 연동에 실패했습니다. 잠시 후 다시 시도해주세요.'
  } catch (err) {
    console.error('카드 연동 실패:', err.response?.data || err)
    error.value = err.response?.data?.message || '카드 연동에 실패했습니다. 잠시 후 다시 시도해주세요.'
  } finally {
    isLoading.value = false
  }
}

const getButtonText = () => {
  if (!isAuthenticated.value) {
    return '로그인해서 시작해보세요'
  }
  if (isLoading.value) {
    return '연동 중...'
  }
  return '지금 시작하기'
}

const startMyData = async () => {
  if (!isAuthenticated.value) {
    router.push('/login')
  } else {
    await fetchMyData()
  }
}
</script>

<style scoped>
.hero {
  @apply flex items-center justify-center min-h-[70vh] text-center;
  background: linear-gradient(180deg, 
    rgba(234, 243, 255, 0.8) 0%,
    rgba(234, 243, 255, 0.4) 50%,
    rgba(255, 255, 255, 1) 100%
  );
  position: relative;
  left: 50%;
  right: 50%;
  margin-top: -100px;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;
  padding: 3rem 1rem;
}

.hero h1 {
  @apply text-4xl md:text-5xl font-bold text-gray-900 max-w-3xl mx-auto;
}

.hero p {
  @apply text-lg md:text-xl text-gray-600 max-w-2xl mx-auto;
}

.hero button {
  @apply bg-blue-500 text-white px-8 py-3 rounded-full text-lg font-medium shadow-lg;
}

button:disabled {
  @apply opacity-70 cursor-not-allowed;
}
</style>
