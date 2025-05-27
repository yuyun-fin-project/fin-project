<template>
  <div class="home-page">
    <!-- 히어로 섹션 -->
    <div
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="w-full"
    >
      <section class="hero-section relative overflow-hidden bg-gradient-to-br from-blue-500/80 via-blue-600/70 to-transparent">
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-blue-600/40 to-white/90"></div>
        <div class="max-w-6xl mx-auto px-4 py-20 relative z-10">
          <div class="grid md:grid-cols-2 gap-8 items-center">
            <div
              v-motion
              :initial="{ opacity: 0, x: -40 }"
              :enter="{ opacity: 1, x: 0 }"
              :delay="400"
            >
              <h1 class="text-4xl md:text-5xl font-bold mb-6 text-white/90">
                스마트한 금융 생활의 시작
              </h1>
              <p class="text-xl mb-8 text-blue-50/90">
                AI가 추천하는 맞춤형 금융상품으로<br>
                더 나은 수익을 경험하세요
              </p>
              <router-link
                to="/recommend"
                class="inline-block bg-white/90 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-white transition-colors"
              >
                AI 추천 받기
              </router-link>
            </div>
            <div
              v-motion
              :initial="{ opacity: 0, scale: 0.9 }"
              :enter="{ opacity: 1, scale: 1 }"
              :delay="500"
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

      <div class="max-w-6xl mx-auto px-4">
        <!-- 주요 기능 소개 -->
        <section class="mb-12 mt-12">
          <h2 class="text-3xl font-bold text-center mb-12 text-gray-900">주요 기능</h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div
              v-for="(feature, index) in features"
              :key="index"
              v-motion
              :initial="{ opacity: 0, y: 20 }"
              :enter="{ opacity: 1, y: 0 }"
              :delay="600 + (index * 100)"
              class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100"
            >
              <div class="text-3xl mb-4">{{ feature.icon }}</div>
              <h3 class="text-xl font-semibold mb-2 text-gray-900">{{ feature.title }}</h3>
              <p class="text-gray-600">{{ feature.description }}</p>
            </div>
          </div>
        </section>

        <!-- 실시간 금융 정보 -->
        <section class="mb-12">
          <h2 class="text-3xl font-bold text-center mb-12 text-gray-900">경제 뉴스</h2>
          <!-- 경제 뉴스 -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 40 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="800"
            class="bg-white p-6 rounded-xl shadow-sm w-full"
          >
            <economic-news-list />
          </div>
        </section>

        <!-- 커뮤니티 섹션 -->
        <section class="mb-12">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-bold mb-4 text-gray-900">금융 커뮤니티</h2>
            <p class="text-gray-600">다른 투자자들과 정보를 공유하고 소통하세요</p>
          </div>
          <div class="grid md:grid-cols-2 gap-8">
            <!-- 인기 게시글 -->
          <div
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="1000"
            class="space-y-4"
          >
            <div v-if="popularPosts.length === 0" class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <p class="text-gray-600 text-center py-4">첫 번째 글을 작성해 보세요!</p>
            </div>
            <article
              v-else
              v-for="post in popularPosts"
              :key="post.id"
              class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 cursor-pointer"
              @click="goToPost(post.id)"
            >
              <h3 class="font-semibold text-lg mb-2 text-gray-900">{{ post.title }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ post.content }}</p>
              <div class="flex items-center text-sm text-gray-500">
                <span>{{ post.author }}</span>
                <span class="mx-2">·</span>
                <span>좋아요 {{ post.likeCount }}</span>
              </div>
            </article>
          </div>
                      
            <!-- 커뮤니티 통계 -->
            <div
              v-motion
              :initial="{ opacity: 0, y: 20 }"
              :enter="{ opacity: 1, y: 0 }"
              :delay="1100"
              class="bg-white p-6 rounded-xl shadow-sm border border-gray-100"
            >
              <h3 class="text-xl font-semibold mb-6 text-gray-900">커뮤니티 통계</h3>
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
        </section>

        <!-- CTA 섹션 -->
        <section class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-2xl text-white">
          <div class="max-w-4xl mx-auto px-8 py-16 text-center">
            <h2 class="text-3xl font-bold mb-6">지금 시작하세요</h2>
            <p class="text-xl mb-8 text-blue-100">
              AI 기반 금융 상품 추천으로 더 나은 투자를 경험하세요
            </p>
            <div class="space-x-4">
              <router-link
                to="/mydata"
                class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                소비습관 분석하기
              </router-link>
              <router-link
                to="/recommend"
                class="inline-block bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                AI 추천 받기
              </router-link>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onActivated } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MarketTrendList from '@/components/MarketTrendList.vue'
import EconomicNewsList from '@/components/EconomicNewsList.vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

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

// 인기 게시글 데이터
const popularPosts = ref([
  // {
  //   id: 1,
  //   title: '2024년 금리 전망과 투자 전략',
  //   content: '올해 금리는 어떻게 될까요? 전문가들의 의견을 종합해보았습니다...',
  //   author: '금융전문가',
  //   views: 1234
  // },
  // {
  //   id: 2,
  //   title: '적금 vs 예금, 어떤 것이 유리할까?',
  //   content: '목적과 기간에 따른 적금과 예금의 장단점을 비교해보았습니다...',
  //   author: '재테크고수',
  //   views: 982
  // }
])

// 커뮤니티 통계 데이터
const communityStats = ref({
  totalPosts: '0',
  totalUsers: '0',
  todayPosts: '0',
  totalComments: '0'
})

// 게시글 상세 페이지로 이동
const goToPost = (postId) => {
  router.push(`/community/`)
}

// 커뮤니티 통계 가져오기
const fetchCommunityStats = async () => {
  try {
    const response = await axios.get(
      'http://127.0.0.1:8000/articles/community/stats/'
    )
    
    if (response.data) {
      communityStats.value = {
        totalPosts: response.data.total_posts?.toString() || '0',
        totalUsers: response.data.total_users?.toString() || '0',
        todayPosts: response.data.today_posts?.toString() || '0',
        totalComments: response.data.total_comments?.toString() || '0'
      }
      console.log('Updated community stats:', communityStats.value)
    }
  } catch (error) {
    console.error('커뮤니티 통계를 불러오는데 실패했습니다:', error)
    if (error.response) {
      console.error('Response status:', error.response.status);
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Error:', error.message);
    }
  }
}

const fetchCommunityarticles = async () => {
  try {
    const response = await axios.get(
      'http://127.0.0.1:8000/articles/community/recentpost/'
    );
    if (response.data && response.data.recent_articles) {
      console.log(response.data.recent_articles);

      // 앞 2개만 추출해서 매핑 후 popularPosts에 할당
      popularPosts.value = response.data.recent_articles
        .slice(0, 2) // 앞 2개만!
        .map(article => ({
          id: article.id,
          title: article.title,
          content: article.content,
          author: article.nickname,
          likeCount: article.like_count
        }));
    }
  } catch (error) {
    console.error(error);
  }
};

// 컴포넌트 마운트 시 통계 데이터 가져오기
onMounted(() => {
  console.log('Component mounted, fetching stats...')
  fetchCommunityStats()
  fetchCommunityarticles()
})

</script>

<style scoped>
.home-page {
  @apply min-h-screen;
}

.hero-section {
  position: relative;
  width: 100%;
  min-height: 600px;  /* 전체 화면 높이에서 적절한 높이로 변경 */
  background: linear-gradient(135deg, #4285f4 0%, #3b82f6 100%);
  overflow: hidden;
  margin-top: -5rem;
  padding-top: 8rem;
}

.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
</style>
