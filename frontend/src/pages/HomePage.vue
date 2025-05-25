<template>
  <div class="home-page">
    <!-- 히어로 섹션 -->
    <section class="hero-section relative overflow-hidden bg-gradient-to-r from-blue-600 to-blue-800 text-white">
      <div class="max-w-6xl mx-auto px-4 py-20 relative z-10">
        <div class="grid md:grid-cols-2 gap-8 items-center">
          <div
            v-motion
            :initial="{ opacity: 0, x: -40 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="200"
          >
            <h1 class="text-4xl md:text-5xl font-bold mb-6">
              스마트한 금융 생활의 시작
            </h1>
            <p class="text-xl mb-8 text-blue-100">
              AI가 추천하는 맞춤형 금융상품으로<br>
              더 나은 수익을 경험하세요
            </p>
            <router-link
              to="/recommend"
              class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              AI 추천 받기
            </router-link>
          </div>
          <div
            v-motion
            :initial="{ opacity: 0, scale: 0.9 }"
            :enter="{ opacity: 1, scale: 1 }"
            :delay="400"
            class="hidden md:block"
          >
            <img src="@/assets/finance-hero.svg" alt="금융 이미지" class="w-full">
          </div>
        </div>
      </div>
      <!-- 배경 장식 -->
      <div class="absolute top-0 right-0 w-1/2 h-full opacity-10">
        <div class="absolute inset-0 bg-pattern transform rotate-12 scale-150"></div>
      </div>
    </section>

    <!-- 주요 기능 소개 -->
    <section class="py-20 bg-white">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12 text-black">주요 기능</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="200 + (index * 100)"
            class="bg-white p-6 text-black rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100"
          >
            <div class="text-3xl mb-4">{{ feature.icon }}</div>
            <h3 class="text-xl font-semibold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 실시간 금융 정보 -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12 text-black">실시간 금융 정보</h2>
        <div class="grid md:grid-cols-2 gap-8">
          <!-- 경제 뉴스 -->
          <div
            v-motion
            :initial="{ opacity: 0, x: -20 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="200"
            class="bg-white p-6 rounded-xl shadow-sm"
          >
            <h3 class="text-xl font-semibold mb-4 text-black">경제 뉴스</h3>
            <economic-news-list />
          </div>
          
          <!-- 시장 동향 -->
          <div
            v-motion
            :initial="{ opacity: 0, x: 20 }"
            :enter="{ opacity: 1, x: 0 }"
            :delay="300"
            class="bg-white p-6 rounded-xl shadow-sm"
          >
            <h3 class="text-xl font-semibold mb-4 text-black">시장 동향</h3>
            <market-trend-list :trends="marketTrends" />
          </div>
        </div>
      </div>
    </section>

    <!-- 커뮤니티 섹션 -->
    <section class="py-20 bg-white">
      <div class="max-w-6xl mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold mb-4 text-black">금융 커뮤니티</h2>
          <p class="text-gray-600">다른 투자자들과 정보를 공유하고 소통하세요</p>
        </div>
        <div class="grid md:grid-cols-2 gap-8">
          <!-- 인기 게시글 -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="200"
            class="space-y-4 text-black"
          >
            <article
              v-for="post in popularPosts"
              :key="post.id"
              class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 cursor-pointer"
              @click="goToPost(post.id)"
            >
              <h3 class="font-semibold text-lg mb-2">{{ post.title }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ post.content }}</p>
              <div class="flex items-center text-sm text-gray-500">
                <span>{{ post.author }}</span>
                <span class="mx-2">·</span>
                <span>조회 {{ post.views }}</span>
              </div>
            </article>
          </div>
          
          <!-- 커뮤니티 통계 -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="300"
            class="bg-white p-6 rounded-xl shadow-sm text-black border border-gray-100"
          >
            <h3 class="text-xl font-semibold mb-6">커뮤니티 통계</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center p-4 bg-gray-50 rounded-lg">
                <div class="text-3xl font-bold text-blue-600 mb-2">{{ communityStats.totalPosts }}</div>
                <div class="text-gray-600">총 게시글</div>
              </div>
              <div class="text-center p-4 bg-gray-50 rounded-lg">
                <div class="text-3xl font-bold text-blue-600 mb-2">{{ communityStats.totalUsers }}</div>
                <div class="text-gray-600">활성 사용자</div>
              </div>
              <div class="text-center p-4 bg-gray-50 rounded-lg">
                <div class="text-3xl font-bold text-blue-600 mb-2">{{ communityStats.todayPosts }}</div>
                <div class="text-gray-600">오늘 작성글</div>
              </div>
              <div class="text-center p-4 bg-gray-50 rounded-lg">
                <div class="text-3xl font-bold text-blue-600 mb-2">{{ communityStats.totalComments }}</div>
                <div class="text-gray-600">총 댓글</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA 섹션 -->
    <section class="py-20 bg-gradient-to-r from-blue-600 to-blue-800 text-white">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-6">지금 시작하세요</h2>
        <p class="text-xl mb-8 text-blue-100">
          AI 기반 금융 상품 추천으로 더 나은 투자를 경험하세요
        </p>
        <div class="space-x-4">
          <router-link
            to="/register"
            class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            회원가입
          </router-link>
          <router-link
            to="/ai"
            class="inline-block bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
          >
            AI 추천 받기
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MarketTrendList from '@/components/MarketTrendList.vue'
import EconomicNewsList from '@/components/EconomicNewsList.vue'

const router = useRouter()

// Simulate async setup for consistency with other pages
await new Promise(resolve => setTimeout(resolve, 0));

// 주요 기능 데이터
const features = [
  {
    icon: '🤖',
    title: 'AI 맞춤 추천',
    description: '인공지능이 분석한 최적의 금융상품을 추천해드립니다.'
  },
  {
    icon: '📊',
    title: '실시간 시장 분석',
    description: '금리, 주식, 펀드 등 실시간 금융 정보를 제공합니다.'
  },
  {
    icon: '👥',
    title: '커뮤니티',
    description: '다른 투자자들과 정보를 공유하고 소통할 수 있습니다.'
  }
]

// 시장 동향 데이터
const marketTrends = ref([
  {
    title: '기준금리 동결',
    description: '한국은행, 기준금리 3.50% 동결 결정',
    date: '2024.03.21'
  },
  {
    title: '예금금리 상승세',
    description: '시중은행 예금금리 평균 4.5% 기록',
    date: '2024.03.20'
  },
  {
    title: '펀드시장 동향',
    description: '채권형 펀드 수익률 상승세 지속',
    date: '2024.03.19'
  }
])

// 인기 게시글 데이터
const popularPosts = ref([
  {
    id: 1,
    title: '2024년 금리 전망과 투자 전략',
    content: '올해 금리는 어떻게 될까요? 전문가들의 의견을 종합해보았습니다...',
    author: '금융전문가',
    views: 1234
  },
  {
    id: 2,
    title: '적금 vs 예금, 어떤 것이 유리할까?',
    content: '목적과 기간에 따른 적금과 예금의 장단점을 비교해보았습니다...',
    author: '재테크고수',
    views: 982
  }
])

// 커뮤니티 통계 데이터
const communityStats = ref({
  totalPosts: '1,234',
  totalUsers: '567',
  todayPosts: '89',
  totalComments: '4,321'
})

// 게시글 상세 페이지로 이동
const goToPost = (postId) => {
  router.push(`/community/article/${postId}`)
}
</script>

<style scoped>
.home-page {
  @apply min-h-screen;
}

.loading {
  @apply flex items-center justify-center min-h-[200px];
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}

.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
</style>
