<template>
  <header class="header">
    <router-link to="/" class="logo">Bank</router-link>
    <nav class="nav">
      <router-link to="/dashboard" active-class="active">금융</router-link>
      <router-link to="/recommend" active-class="active">추천</router-link>
      <router-link to="/community" active-class="active">커뮤니티</router-link>
      <router-link to="/mydata" active-class="active">마이데이터</router-link>
      
      <!-- 로그인 상태에 따른 조건부 렌더링 -->
      <template v-if="isAuthenticated">
        <router-link to="/mypage" class="mypage-btn">마이페이지</router-link>
        <button @click="handleLogout" class="logout-btn">로그아웃</button>
      </template>
      <router-link v-else to="/login" class="login-btn">로그인</router-link>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const handleLogout = async () => {
  try {
    await authStore.logout()
    // 로그아웃 후 현재 페이지가 인증이 필요한 페이지라면 홈으로 이동
    if (router.currentRoute.value.meta.requiresAuth) {
      router.push('/')
    }
  } catch (error) {
    console.error('로그아웃 실패:', error)
  }
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0rem;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3182f6;
  cursor: pointer;
  text-decoration: none;
}

.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav a {
  color: #333;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
  font-weight: 500;
  font-size: 1rem;
}

.nav a:hover {
  color: #3182f6;
}

.nav a.active {
  color: #3182f6;
  font-weight: 600;
}

.login-btn, .logout-btn {
  background-color: #3182f6;
  color: white !important;
  padding: 0.5rem 1.5rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 600 !important;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.login-btn:hover, .logout-btn:hover {
  background-color: #1e6ee9;
}

.mypage-btn {
  background-color: transparent;
  color: #3182f6 !important;
  padding: 0.5rem 1.5rem;
  border-radius: 0.75rem;
  border: 2px solid #3182f6;
  font-weight: 600 !important;
  transition: all 0.2s ease-in-out;
}

.mypage-btn:hover {
  background-color: #3182f6;
  color: white !important;
}
</style>
