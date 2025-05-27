<template>
  <div class="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-900">관심 종목 정보</h2>
      <router-link
        to="/stock-search"
        class="text-sm text-blue-600 hover:text-blue-800 font-medium"
      >
        더 알아보기 →
      </router-link>
    </div>

    <div class="flex-1 flex flex-col space-y-4">
      <!-- 검색 입력 -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="관심 있는 종목을 검색해보세요"
          class="w-full px-4 py-2.5 pr-12 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-700"
          @keyup.enter="searchVideos"
        />
        <button
          @click="searchVideos"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 px-3 py-1.5 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors"
        >
          검색
        </button>
      </div>

      <!-- 최근 검색 결과 -->
      <div v-if="recentVideos.length > 0" class="flex-1 overflow-auto space-y-4">
        <div
          v-for="video in recentVideos.slice(0, 3)"
          :key="video.id"
          class="flex gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
          @click="modalStore.openVideoModal(video)"
        >
          <img
            :src="video.thumbnail"
            :alt="video.title"
            class="w-24 h-16 object-cover rounded"
          />
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">
              {{ video.title }}
            </h3>
            <p class="text-xs text-gray-600 mt-1">
              {{ video.channelTitle }}
            </p>
            <div class="flex items-center text-xs text-gray-500 mt-1">
              <span>{{ formatDate(video.publishedAt) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 검색 전 상태 -->
      <div v-if="!recentVideos.length && !isLoading" class="flex flex-col items-center justify-center h-full">
        <img 
          src="https://www.youtube.com/img/desktop/yt_1200.png"
          alt="YouTube Logo"
          class="w-32 mb-2 opacity-75"
        />
        <p class="text-gray-500 text-center text-sm">
          관심 있는 종목을 검색하면<br/>
          관련 유튜브 영상을 찾아드립니다
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useModalStore } from '../stores/modalStore'

const router = useRouter()
const modalStore = useModalStore()
const searchQuery = ref('')
const recentVideos = ref([])
const searchResults = ref([])
const isLoading = ref(false)
const error = ref(null)

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
      recentVideos.value = sampleData.slice(0, 3)
      searchResults.value = sampleData.slice(0, 3)
      return
    }

    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(
        searchQuery.value + ' 주식 투자'
      )}&type=video&maxResults=3&key=${import.meta.env.VITE_YOUTUBE_API_KEY}`
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

    const mappedResults = detailsData.items.map(item => ({
      id: item.id,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.high.url,
      channelTitle: item.snippet.channelTitle,
      publishedAt: item.snippet.publishedAt
    }))

    recentVideos.value = mappedResults
    searchResults.value = mappedResults
  } catch (err) {
    console.error('Error fetching videos:', err)
    error.value = err.message
    recentVideos.value = []
    searchResults.value = []
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
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.overflow-auto {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E1 transparent;
}

.overflow-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #CBD5E1;
  border-radius: 3px;
}

/* 커서 스타일 */
.cursor-pointer {
  cursor: pointer;
}
</style> 