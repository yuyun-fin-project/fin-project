<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">환영합니다!</h1>
        <p class="text-gray-600">소셜 계정으로 간편하게 로그인하세요</p>
      </div>

      <div class="space-y-4">
        <SocialLoginButton
          provider="google"
          label="Google로 계속하기"
          :authUrl="GOOGLE_AUTH_URL"
        />
        <SocialLoginButton
          provider="kakao"
          label="Kakao로 계속하기"
          :authUrl="KAKAO_AUTH_URL"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import SocialLoginButton from '../components/SocialLoginButton.vue'

const GOOGLE_AUTH_URL = 'http://localhost:8000/accounts/google/login/'
const KAKAO_AUTH_URL = import.meta.env.VITE_KAKAO_LOGIN_URL || 'http://localhost:8000/accounts/kakao/login/'
</script>

<style scoped>
.social-login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.login-title {
  text-align: center;
  margin-bottom: 2rem;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
