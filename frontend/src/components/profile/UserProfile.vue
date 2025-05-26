<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">프로필</h2>
    <div v-if="user" class="space-y-4">
      <div class="flex items-center space-x-4">
        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-medium text-gray-900">
            {{ displayName }}
          </h3>
          <p class="text-sm text-gray-500">{{ user.useremail || user.email }}</p>
        </div>
      </div>
      
      <div class="border-t pt-4">
        <div class="grid grid-cols-2 gap-4 text-center">
          <div>
            <p class="text-sm text-gray-500">작성한 글</p>
            <p class="text-lg font-semibold text-gray-900">{{ articleCount }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">찜한 상품</p>
            <p class="text-lg font-semibold text-gray-900">{{ localBookmarkCount || 0 }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-gray-500">
      로딩 중...
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import eventBus from '../../utils/eventBus'

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  articleCount: {
    type: Number,
    default: 0
  },
  bookmarkCount: {
    type: Number,
    default: 0
  }
})

const localBookmarkCount = ref(props.bookmarkCount)

// props의 bookmarkCount가 변경될 때 localBookmarkCount 업데이트
watch(() => props.bookmarkCount, (newCount) => {
  localBookmarkCount.value = newCount
})

// 북마크 수 변경 이벤트 핸들러
const handleBookmarkCountUpdate = (count) => {
  localBookmarkCount.value = count
}

// 컴포넌트 마운트 시 이벤트 구독
onMounted(() => {
  eventBus.on('bookmark-count-updated', handleBookmarkCountUpdate)
})

// 컴포넌트 언마운트 시 이벤트 구독 해제
onUnmounted(() => {
  eventBus.off('bookmark-count-updated', handleBookmarkCountUpdate)
})

// 사용자 표시 이름 계산
const displayName = computed(() => {
  if (!props.user) return '사용자'
  return props.user.nickname || props.user.useremail || '사용자'
})
</script> 