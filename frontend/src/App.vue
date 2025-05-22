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
import { useRoute } from 'vue-router';
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

const route = useRoute();

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
