<template>
  <div class="stock-search-view">
    <div
      v-motion
      :key="'community-content'"
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0 }"
      :delay="300"
      :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
      class="max-w-6xl mx-auto px-4 py-12"
    >
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900">
          관심 종목 검색
        </h1>

      </div>        
        <!-- 검색 입력 섹션 -->
        <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div class="flex gap-4 mb-6">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="관심 있는 종목을 검색해보세요"
              class="flex-1 px-4 py-2.5 pr-12 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700"
              @keyup.enter="searchVideos"
            />
            <button
              @click="searchVideos"
              :disabled="isLoading"
              class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300"
            >
              {{ isLoading ? '검색 중...' : '검색' }}
            </button>
          </div>
        </div>

        <!-- 로딩 상태 -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>

        <!-- 검색 결과 섹션 -->
        <template v-else>
          <div 
            v-if="videos.length > 0" 
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0 }"
            :delay="500"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            <div
              v-for="video in videos"
              :key="video.id"
              class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
              @click="openVideoModal(video)"
            >
              <div class="block">
                <img :src="video.thumbnail" :alt="video.title" class="w-full h-48 object-cover" />
                <div class="p-4">
                  <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">{{ video.title }}</h3>
                  <div class="flex items-center text-sm text-gray-600 mb-2">
                    <span>{{ video.channelTitle }}</span>
                    <span class="mx-2">•</span>
                    <span>{{ formatDate(video.publishedAt) }}</span>
                  </div>
                  <p class="text-gray-600 text-sm line-clamp-2">{{ video.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 검색 결과 없음 -->
          <div
            v-else-if="hasSearched"
            class="bg-white rounded-xl shadow-sm p-8 text-center"
          >
            <p class="text-gray-600">검색 결과가 없습니다.</p>
          </div>
        </template>

        <!-- 비디오 모달 -->
        <VideoModal
          :show="showVideoModal"
          :video="selectedVideo"
          @close="closeVideoModal"
        />

        <!-- 에러 메시지 -->
        <div
          v-if="error"
          class="bg-red-50 border border-red-200 rounded-xl p-4 mt-4 text-center text-red-600"
        >
          {{ error }}
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VideoModal from '../components/VideoModal.vue'

const searchQuery = ref('')
const videos = ref([])
const hasSearched = ref(false)
const isLoading = ref(false)
const error = ref(null)

// 모달 관련 상태
const showVideoModal = ref(false)
const selectedVideo = ref({
  id: '',
  title: '',
  channelTitle: '',
  publishedAt: '',
  description: ''
})

const openVideoModal = (video) => {
  selectedVideo.value = video
  showVideoModal.value = true
}

const closeVideoModal = () => {
  showVideoModal.value = false
  // selectedVideo를 초기 상태로 되돌림
  selectedVideo.value = {
    id: '',
    title: '',
    channelTitle: '',
    publishedAt: '',
    description: ''
  }
}

// 임시 데이터 (API 키가 없을 때 사용)
const sampleData = [
  {
    id: '1',
    title: '삼성전자 투자 전략 분석',
    description: '국내 대표 기업 삼성전자의 최신 투자 전략과 주가 분석',
    thumbnail: 'https://via.placeholder.com/480x360.png?text=Samsung+Electronics',
    channelTitle: '주식투자연구소',
    publishedAt: new Date().toISOString()
  },
  {
    id: '2',
    title: 'SK하이닉스 실적 전망',
    description: '반도체 업종 핵심 기업 SK하이닉스의 실적 분석',
    thumbnail: 'https://via.placeholder.com/480x360.png?text=SK+Hynix',
    channelTitle: '종목분석채널',
    publishedAt: new Date().toISOString()
  },
  {
    id: '3',
    title: '현대차 주가 전망',
    description: '자동차 산업 리더 현대차의 미래 전망',
    thumbnail: 'https://via.placeholder.com/480x360.png?text=Hyundai+Motor',
    channelTitle: '주식마스터',
    publishedAt: new Date().toISOString()
  }
]

const searchVideos = async () => {
  if (!searchQuery.value.trim()) return

  isLoading.value = true
  error.value = null
  
  try {
    // API 키가 없는 경우 샘플 데이터 사용
    if (!import.meta.env.VITE_YOUTUBE_API_KEY) {
      await new Promise(resolve => setTimeout(resolve, 1000)) // 가짜 로딩
      videos.value = sampleData
      hasSearched.value = true
      return
    }

    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(
        searchQuery.value + ' 주식 투자'
      )}&type=video&maxResults=9&key=${import.meta.env.VITE_YOUTUBE_API_KEY}`
    )

    if (!response.ok) {
      throw new Error('검색 중 오류가 발생했습니다.')
    }

    const data = await response.json()

    if (!data.items) {
      throw new Error('검색 결과를 가져올 수 없습니다.')
    }

    // 비디오 상세 정보를 가져오기 위한 두 번째 API 호출
    const videoIds = data.items.map(item => item.id.videoId).join(',')
    const detailsResponse = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id=${videoIds}&key=${import.meta.env.VITE_YOUTUBE_API_KEY}`
    )

    if (!detailsResponse.ok) {
      throw new Error('비디오 상세 정보를 가져올 수 없습니다.')
    }

    const detailsData = await detailsResponse.json()

    videos.value = detailsData.items.map(item => ({
      id: item.id,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.high.url,
      channelTitle: item.snippet.channelTitle,
      publishedAt: item.snippet.publishedAt
    }))

    hasSearched.value = true
  } catch (err) {
    console.error('Error fetching videos:', err)
    error.value = err.message
    videos.value = [] // 에러 시 결과 초기화
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
</script>

<style scoped>
.stock-search-view {
  @apply min-h-screen bg-gray-50;
  margin-top: -5rem;  /* 상단 여백 제거 */
  padding-top: 5rem;  /* 헤더 높이만큼 패딩 추가 */
}

.stock-search-container {
  @apply container mx-auto px-4 py-8;
}

.search-title {
  @apply text-3xl font-bold text-center mb-8;
}

.search-form {
  @apply max-w-2xl mx-auto;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 