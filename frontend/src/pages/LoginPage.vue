<template>
  <div class="login-page">
    <div class="login-container">
      <div class="text-center mb-8">
        <h1 class="login-title">환영합니다!</h1>
        <p class="login-subtitle">소셜 계정으로 간편하게 로그인하세요</p>
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
.login-page {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem;
  padding-top: 5rem;
}

.login-container {
  @apply container mx-auto px-4 py-8 flex flex-col items-center justify-center;
}

.login-title {
  @apply text-3xl font-bold text-center mb-4;
}

.login-subtitle {
  @apply text-gray-600 text-center mb-8;
}

.social-login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
