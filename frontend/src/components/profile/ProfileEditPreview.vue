<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">회원 정보 수정</h2>
    <div class="space-y-6">
      <!-- 닉네임 수정 폼 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">닉네임</label>
        <div class="flex space-x-2">
          <input
            v-model="nickname"
            type="text"
            placeholder="새로운 닉네임을 입력하세요"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            @click="updateNickname"
            :disabled="isLoading || !nickname"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
          >
            {{ isLoading ? '변경 중...' : '변경하기' }}
          </button>
        </div>
        <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
        <p v-if="success" class="mt-2 text-sm text-green-600">{{ success }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const nickname = ref('')
const isLoading = ref(false)
const error = ref('')
const success = ref('')

const updateNickname = async () => {
  if (!nickname.value) return
  
  isLoading.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await axios.put(
      `http://127.0.0.1:8000/accounts/profile/${auth.user.id}/`,
      { nickname: nickname.value },
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    )

    success.value = '닉네임이 성공적으로 변경되었습니다.'
    // 전역 상태의 사용자 정보 업데이트
    auth.updateUserInfo({ ...auth.user, nickname: nickname.value })
    
    // 3초 후 성공 메시지 제거 및 페이지 새로고침
    setTimeout(() => {
      success.value = ''
      window.location.reload()
    }, 1000)

  } catch (err) {
    if (err.response?.status === 401) {
      error.value = '로그인이 필요합니다.'
    } else if (err.response?.status === 405) {
      error.value = '닉네임 변경이 허용되지 않습니다.'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = '닉네임 변경 중 오류가 발생했습니다.'
    }
  } finally {
    isLoading.value = false
  }
}
</script> 



