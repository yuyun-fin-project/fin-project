<template>
  <div id="app" class="app">
    <div class="container">
      <Header />
    </div>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <suspense>
          <template #default>
            <keep-alive include="['HomePage', 'AIView', 'MyDataView', 'CommunityView', 'ProductComparisonView']">
              <transition
                name="page"
                mode="out-in"
                @before-leave="beforeLeave"
                @enter="enter"
                @after-enter="afterEnter"
              >
                <component 
                  :is="Component" 
                  :key="route.fullPath"
                  v-if="Component"
                />
              </transition>
            </keep-alive>
          </template>
          <template #fallback>
            <div class="loading">
              <div class="loading-spinner"></div>
            </div>
          </template>
        </suspense>
      </router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { onMounted, watch } from 'vue';
import { useAuthStore } from './stores/auth';
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// URL의 access 토큰 감시
watch(
  () => route.query.access,
  async (newToken) => {
    if (newToken) {
      try {
        // JWT 토큰 디코딩
        const payload = JSON.parse(atob(newToken.split('.')[1]));
        // user_id 저장
        localStorage.setItem('user_id', payload.user_id);
        // 토큰 저장 및 인증 처리
        await authStore.setAccessToken(newToken);
        // URL에서 access 파라미터 제거
        const { access, ...query } = route.query;
        await router.replace({ query });
        // 홈페이지로 리다이렉트
        if (route.path === '/login') {
          await router.push('/');
        }
      } catch (error) {
        console.error('로그인 처리 실패:', error);
        await router.push('/login');
      }
    }
  },
  { immediate: true }
);

// 초기 인증 상태 확인
onMounted(async () => {
  if (authStore.accessToken) {
    try {
      // 저장된 토큰으로 사용자 정보 가져오기
      await authStore.checkAuth();
    } catch (error) {
      console.error('인증 확인 실패:', error);
      await router.push('/login');
    }
  }
});

const beforeLeave = (el) => {
  window.scrollTo(0, 0);
};

const enter = (el, done) => {
  requestAnimationFrame(() => {
    done();
  });
};

const afterEnter = (el) => {
  window.scrollTo(0, 0);
};
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.app {
  @apply min-h-screen flex flex-col;
}

.main-content {
  @apply flex-grow;
}

.loading {
  @apply flex items-center justify-center min-h-[200px];
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}

/* 컨테이너 스타일 */
.container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
}
</style>
