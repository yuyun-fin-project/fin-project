<template>
  <header class="header" :class="{ 'header-scrolled': isScrolled }">
    <div class="container mx-auto">
      <div class="header-content">
        <router-link to="/" class="logo custom-font">YUNU'S</router-link>
        <nav class="nav">
          <router-link to="/dashboard" active-class="active">금융</router-link>
          <router-link to="/recommend" active-class="active">추천</router-link>
          <router-link to="/community" active-class="active">커뮤니티</router-link>
          <router-link to="/mydata" active-class="active">마이데이터</router-link>
          
          <!-- 로그인 상태에 따른 조건부 렌더링 -->
          <template v-if="isAuthenticated">
            <div class="auth-buttons">
              <router-link to="/mypage" class="mypage-btn">마이페이지</router-link>
              <button @click="handleLogout" class="logout-btn">로그아웃</button>
            </div>
          </template>
          <router-link v-else to="/login" class="login-btn">로그인</router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

// 스크롤 상태 관리
const isScrolled = ref(false)

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  isScrolled.value = window.scrollY > 0
}

// 컴포넌트 마운트/언마운트 시 이벤트 리스너 관리
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

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
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 4rem;
  transition: all 0.3s ease;
  background-color: transparent;
  box-sizing: border-box;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.header-scrolled {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  @apply text-2xl font-bold;
  color: #3182f6;
  text-decoration: none;
}

.nav {
  @apply flex items-center gap-6;
}

.nav a {
  color: #4b5563;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav a:hover {
  color: #3182f6;
  text-decoration: none;
}

.nav a.active {
  color: #3182f6;
  font-weight: 600;
}

/* 홈 페이지에서만 적용될 스타일 */
.home-page .header:not(.header-scrolled) .logo {
  color: white;
}

.home-page .header:not(.header-scrolled) .nav a {
  color: rgba(255, 255, 255, 0.9);
}

.home-page .header:not(.header-scrolled) .nav a:hover,
.home-page .header:not(.header-scrolled) .nav a.active {
  color: white;
}

.home-page .header:not(.header-scrolled) .login-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.home-page .header:not(.header-scrolled) .login-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 스크롤 시 또는 다른 페이지에서의 스타일 */
.header-scrolled .logo,
.header:not(.home-page) .logo {
  color: #3182f6;
}

.auth-buttons {
  @apply flex items-center gap-4;
}

/* 기본 마이페이지 버튼 스타일 */
.mypage-btn {
  @apply px-4 py-2 rounded-lg;
  color: #3182f6;
  border: 1px solid #3182f6;
  background-color: white;
  transition: all 0.2s ease;
}

.mypage-btn:hover {
  background-color: #f0f7ff;
  text-decoration: none;
}

/* 기본 로그아웃 버튼 스타일 */
.logout-btn {
  @apply px-4 py-2 rounded-lg;
  color: white;
  background-color: #3182f6;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: #2563eb;
}

/* 홈페이지에서 스크롤하지 않았을 때의 버튼 스타일 */
.home-page .header:not(.header-scrolled) .mypage-btn {
  color: white;
  border-color: rgba(255, 255, 255, 0.5);
  background-color: transparent;
}

.home-page .header:not(.header-scrolled) .mypage-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.home-page .header:not(.header-scrolled) .logout-btn {
  background-color: rgba(255, 255, 255, 0.2);
}

.home-page .header:not(.header-scrolled) .logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.login-btn {
  @apply px-4 py-2 rounded-lg;
  background-color: #3182f6;
  color: white !important;
  transition: all 0.2s ease;
  font-weight: 500;
}

.login-btn:hover {
  background-color: #2563eb;
  text-decoration: none;
}

/* 홈 페이지에서 스크롤하지 않았을 때의 로그인 버튼 스타일 */
.home-page .header:not(.header-scrolled) .login-btn {
  background-color: rgba(255, 255, 255, 0.2);
}

.home-page .header:not(.header-scrolled) .login-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 스크롤 시 또는 다른 페이지에서의 로그인 버튼 스타일 */
.header-scrolled .login-btn,
.header:not(.home-page) .login-btn {
  background-color: #3182f6;
}

.header-scrolled .login-btn:hover,
.header:not(.home-page) .login-btn:hover {
  background-color: #2563eb;
}

.custom-font {
  font-family: "Poetsen One", sans-serif;
  font-weight: 800;
  font-size: 2.2rem;
  font-style: normal;
}

@media (max-width: 768px) {
  .header {
    padding: 0.5rem 2rem;
  }
  
  .nav {
    gap: 1rem;
  }
  
  .logo {
    font-size: 1.8rem;
  }
  
  .nav a {
    font-size: 0.9rem;
  }
}
</style>
