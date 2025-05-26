<template>
  <div v-if="show" class="fixed inset-0 z-[1001] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- 배경 오버레이 -->
      <div class="fixed inset-0 transition-opacity" @click="handleClose">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <!-- 모달 컨텐츠 -->
      <div class="relative inline-block w-full max-w-4xl p-6 my-8 text-left align-middle bg-white rounded-lg shadow-xl transform transition-all">
        <!-- 닫기 버튼 -->
        <div class="absolute top-2 right-2 z-50">
          <button
            type="button"
            class="bg-white rounded-full p-2 text-gray-400 hover:text-gray-500 focus:outline-none hover:bg-gray-100"
            @click="handleClose"
          >
            <span class="sr-only">닫기</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 비디오 플레이어 -->
        <div class="aspect-w-16 aspect-h-9 mb-4">
          <iframe
            :src="'https://www.youtube.com/embed/' + videoId"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            class="w-full h-full rounded-lg"
          ></iframe>
        </div>

        <!-- 비디오 정보 -->
        <div class="space-y-4">
          <h3 class="text-2xl font-bold text-gray-900">{{ video.title }}</h3>
          <div class="flex items-center text-sm text-gray-600">
            <span class="font-medium">{{ video.channelTitle }}</span>
            <span class="mx-2">•</span>
            <span>{{ formatDate(video.publishedAt) }}</span>
          </div>
          <div class="max-h-[40vh] overflow-y-auto pr-2">
            <p class="text-gray-700 text-base whitespace-pre-line">
              {{ isExpanded ? video.description : truncatedDescription }}
              <button
                v-if="shouldShowToggle"
                @click="toggleDescription"
                class="text-blue-600 hover:text-blue-800 font-medium ml-2"
              >
                {{ isExpanded ? '간략히' : '더보기' }}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  video: {
    type: Object,
    required: false,
    default: () => ({
      id: '',
      title: '',
      channelTitle: '',
      publishedAt: '',
      description: ''
    })
  }
})

// 디버깅을 위한 watcher 추가
watch(() => props.video, (newVideo) => {
  console.log('Video data received:', newVideo)
  console.log('Description length:', newVideo?.description?.length)
  console.log('Full description:', newVideo?.description)
}, { immediate: true, deep: true })

// 모달이 열리고 닫힐 때 body 스크롤 제어
watch(() => props.show, (newValue) => {
  if (newValue) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const isExpanded = ref(false)
const DESCRIPTION_LIMIT = 200 // 더 긴 글자 수로 변경

const truncatedDescription = computed(() => {
  if (!props.video?.description) return ''
  if (props.video.description.length <= DESCRIPTION_LIMIT) return props.video.description
  return props.video.description.slice(0, DESCRIPTION_LIMIT) + '...'
})

const shouldShowToggle = computed(() => {
  return props.video?.description?.length > DESCRIPTION_LIMIT
})

const toggleDescription = () => {
  isExpanded.value = !isExpanded.value
}

const emit = defineEmits(['close'])
const videoId = computed(() => props.video?.id || '')

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

// 닫기 핸들러
const handleClose = () => {
  document.body.style.overflow = ''
  emit('close')
}
</script>

<style scoped>
.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
}

.aspect-w-16 iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 스크롤바 스타일링 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 모달 스타일 */
.fixed {
  position: fixed;
}

.z-[1001] {
  z-index: 1001;
}

/* 배경 오버레이 스타일 */
.bg-opacity-75 {
  --tw-bg-opacity: 0.75;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style> 

