<template>
  <div class="economic-news-list">
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="error" class="text-red-500 p-4 text-center">
      {{ error }}
    </div>

    <div v-else class="space-y-4">
      <a
        v-for="news in newsItems"
        :key="news.link"
        :href="news.link"
        target="_blank"
        rel="noopener noreferrer"
        class="block p-4 hover:bg-gray-50 rounded-lg transition-colors border-b border-gray-100 last:border-b-0"
      >
        <div class="flex gap-4">
          <div class="flex-1">
            <h4 class="font-medium text-gray-900 mb-1">{{ news.title }}</h4>
            <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ news.description }}</p>
            <div class="flex items-center text-xs text-gray-500">
              <span>{{ formatDate(news.pubDate) }}</span>
              <span class="mx-2">·</span>
              <span>{{ news.source }}</span>
            </div>
          </div>
        </div>
      </a>
    </div>

    <div v-if="!loading && !error && newsItems.length === 0" class="text-center py-8 text-gray-500">
      뉴스를 불러올 수 없습니다.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsItems = ref([])
const loading = ref(true)
const error = ref(null)

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const parseRSSFeed = (xmlText: string) => {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(xmlText, 'text/xml')
  const items = xmlDoc.querySelectorAll('item')
  
  return Array.from(items).map(item => ({
    title: item.querySelector('title')?.textContent?.replace(/<!\[CDATA\[|\]\]>/g, '') || '',
    description: item.querySelector('description')?.textContent?.replace(/<!\[CDATA\[|\]\]>/g, '').replace(/<\/?[^>]+(>|$)/g, '') || '',
    link: item.querySelector('link')?.textContent || '#',
    pubDate: new Date(item.querySelector('pubDate')?.textContent || '').toISOString(),
    source: '한국경제'
  })).slice(0, 5)
}

const fetchNews = async () => {
  loading.value = true
  error.value = null

  try {
    // CORS 우회를 위한 프록시 서버 사용
    const proxyUrl = 'https://api.allorigins.win/raw?url='
    const targetUrl = encodeURIComponent('https://www.hankyung.com/feed/economy')
    
    const response = await axios.get(`${proxyUrl}${targetUrl}`)
    
    if (response.data) {
      newsItems.value = parseRSSFeed(response.data)
    } else {
      throw new Error('뉴스 데이터를 가져오는데 실패했습니다.')
    }
  } catch (err) {
    console.error('뉴스 데이터 조회 실패:', err)
    error.value = '뉴스를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 5분마다 새로고침
const startNewsRefresh = () => {
  setInterval(() => {
    fetchNews()
  }, 300000) // 5분
}

onMounted(() => {
  fetchNews()
  startNewsRefresh()
})
</script>

<style scoped>
.economic-news-list {
  @apply bg-white rounded-lg overflow-hidden;
}
</style> 