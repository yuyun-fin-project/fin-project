import { createRouter, createWebHistory } from 'vue-router'

// 동기적으로 컴포넌트 import
import HomePage from '../pages/HomePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import AIView from '../pages/AIView.vue'
import MyDataView from '../pages/MyDataView.vue'
import CommunityView from '../pages/CommunityView.vue'
import HomeView from '../views/HomeView.vue'
import StockSearchView from '../views/StockSearchView.vue'

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: () => import('../pages/HomePage.vue'),
    meta: { keepAlive: true }
  },
  { 
    path: '/login', 
    name: 'Login',
    component: () => import('../pages/LoginPage.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: () => import('../pages/AIView.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/mydata',
    name: 'MyData',
    component: () => import('../pages/MyDataView.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../pages/DashboardView.vue'),
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
    name: 'Community',
    component: () => import('../pages/CommunityView.vue'),
    meta: { keepAlive: true }
  },
  {
    path: '/stock-search',
    name: 'stock-search',
    component: StockSearchView
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
  // 페이지 전환 시작 시 처리
  if (from.name === 'Home') {
    // 홈에서 다른 페이지로 이동할 때 캐시 초기화
    const toComponent = await to.matched[0].components?.default;
    if (toComponent) {
      delete toComponent.__vccOpts;
    }
  }
  next()
})

router.afterEach((to, from) => {
  // 페이지 전환 완료 시 처리
  window.scrollTo(0, 0)
})

export default router 