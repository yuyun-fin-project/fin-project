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

    <!-- 전역 모달 -->
    <VideoModal
      v-if="modalStore.showVideoModal"
      :show="modalStore.showVideoModal"
      :video="modalStore.videoModalData"
      @close="modalStore.closeVideoModal"
    />
    <ProductDetailModal
      v-if="modalStore.showProductDetailModal"
      :show="modalStore.showProductDetailModal"
      :product="modalStore.productDetailData"
      :isAuthenticated="authStore.isAuthenticated"
      @close="modalStore.closeProductDetailModal"
      @bookmark-updated="handleBookmarkUpdated"
    />
    <ArticleFormModal
      v-if="modalStore.showArticleFormModal"
      :type="modalStore.articleFormModalData.type"
      :article="modalStore.articleFormModalData.article"
      @close="modalStore.closeArticleFormModal"
      @submit="handleArticleFormSubmit"
    />
    <ArticleDetailModal
      v-if="modalStore.showArticleDetailModal"
      :article="modalStore.articleDetailData"
      @close="modalStore.closeArticleDetailModal"
      @delete="handleArticleDelete"
      @update="handleArticleUpdate"
    />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { onMounted, watch } from 'vue';
import { useAuthStore } from './stores/auth';
import { useModalStore } from './stores/modalStore'
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import VideoModal from './components/VideoModal.vue'
import ProductDetailModal from './components/product/ProductDetailModal.vue'
import ArticleFormModal from './components/ArticleFormModal.vue'
import ArticleDetailModal from './components/ArticleDetailModal.vue'
import { articleService } from './services/articleService'

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const modalStore = useModalStore()

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
  // 앱 시작 시 인증 상태 체크
  await authStore.checkAuth()
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

// 북마크 업데이트 이벤트 핸들러
const handleBookmarkUpdated = () => {
  // 북마크 목록을 새로고침하는 이벤트를 발생시킵니다
  window.dispatchEvent(new CustomEvent('refresh-bookmarks'))
}

const handleArticleFormSubmit = async (formData) => {
  try {
    if (modalStore.articleFormModalData.type === 'create') {
      await articleService.createArticle(formData)
    } else {
      await articleService.updateArticle(formData.id, formData)
    }
    modalStore.closeArticleFormModal()
    window.dispatchEvent(new CustomEvent('refresh-articles'))
  } catch (error) {
    console.error('게시글 처리 실패:', error)
    alert('게시글 처리에 실패했습니다. 다시 시도해주세요.')
  }
}

const handleArticleDelete = async (articleId) => {
  try {
    await articleService.deleteArticle(articleId)
    modalStore.closeArticleDetailModal()
    // 게시글 목록 새로고침 이벤트 발생
    window.dispatchEvent(new CustomEvent('refresh-articles'))
    // 내 게시글 목록 새로고침 이벤트 발생
    window.dispatchEvent(new CustomEvent('refresh-my-articles'))
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    alert('게시글 삭제에 실패했습니다. 다시 시도해주세요.')
  }
}

const handleArticleUpdate = async (articleData) => {
  try {
    await articleService.updateArticle(articleData.id, articleData)
    modalStore.closeArticleDetailModal()
    // 게시글 목록 새로고침 이벤트 발생
    window.dispatchEvent(new CustomEvent('refresh-articles'))
    // 내 게시글 목록 새로고침 이벤트 발생
    window.dispatchEvent(new CustomEvent('refresh-my-articles'))
  } catch (error) {
    console.error('게시글 수정 실패:', error)
    alert('게시글 수정에 실패했습니다. 다시 시도해주세요.')
  }
}
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

/* 모달 z-index 설정 */
.video-modal,
.product-detail-modal,
.article-form-modal,
.article-detail-modal {
  @apply fixed inset-0 z-[1001] flex items-center justify-center;
}

/* 모달 오버레이 스타일 */
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 z-[1001];
}

/* 모달 컨텐츠 스타일 */
.modal-content {
  @apply relative z-[1002] bg-white rounded-lg shadow-xl;
}
</style>
