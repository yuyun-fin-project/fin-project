import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 동기적으로 컴포넌트 import
import HomePage from '../pages/HomePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import AIView from '../pages/AIView.vue'
import MyDataView from '../pages/MyDataView.vue'
import CommunityView from '../pages/CommunityView.vue'
import HomeView from '../views/HomeView.vue'
import StockSearchView from '../views/StockSearchView.vue'
import CommunityPage from '@/views/CommunityPage.vue'
import MyPage from '@/views/MyPage.vue'
import DashboardView from '@/pages/DashboardView.vue'

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: HomePage,
    meta: { keepAlive: true }
  },
  { 
    path: '/login', 
    name: 'Login',
    component: LoginPage,
    meta: { keepAlive: true }
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: AIView,
    meta: { keepAlive: true }
  },
  {
    path: '/mydata',
    name: 'MyData',
    component: MyDataView,
    meta: { keepAlive: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { keepAlive: true }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('../pages/ProductComparisonView.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/community',
    name: 'community',
    component: CommunityPage,
    meta: { keepAlive: true }
  },
  {
    path: '/stock-search',
    name: 'stock-search',
    component: StockSearchView
  },
  {
    path: '/mypage',
    name: 'mypage',
    component: MyPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 전역 네비게이션 가드
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 인증이 필요한 페이지인지 확인
  if (to.meta.requiresAuth) {
    // 로그인 상태가 아니면 로그인 페이지로 리다이렉트
    if (!authStore.isAuthenticated) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
    
    // 토큰 유효성 검사
    try {
      await authStore.checkAuth()
      next()
    } catch (error) {
      console.error('인증 확인 실패:', error)
      next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  } else {
    // 페이지 전환 시작 시 처리
    if (from.name === 'Home') {
      // 홈에서 다른 페이지로 이동할 때 캐시 초기화
      const toComponent = await to.matched[0].components?.default;
      if (toComponent) {
        delete toComponent.__vccOpts;
      }
    }
    next()
  }
})

router.afterEach((to, from) => {
  // 페이지 전환 완료 시 처리
  window.scrollTo(0, 0)
})

export default router 