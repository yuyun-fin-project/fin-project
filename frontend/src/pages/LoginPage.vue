<template>
  <div class="login-container">
    <h2>소셜 로그인</h2>
    <SocialLoginButton
      provider="google"
      label="구글로 로그인"
      :authUrl="GOOGLE_AUTH_URL"
    />
    <SocialLoginButton
      provider="kakao"
      label="카카오로 로그인"
      :authUrl="KAKAO_AUTH_URL"
    />
    <SocialLoginButton
      provider="github"
      label="깃허브로 로그인"
      :authUrl="GITHUB_AUTH_URL"
    />
  </div>
</template>

<script setup lang="ts">
import SocialLoginButton from '../components/SocialLoginButton.vue'

const GOOGLE_AUTH_URL = 'http://localhost:8000/auth/google/login/'
const KAKAO_AUTH_URL = 'http://localhost:8000/auth/kakao/login/'
const GITHUB_AUTH_URL = 'http://localhost:8000/auth/github/login/'
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem;
}
</style>
