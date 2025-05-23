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
          <h3 class="text-lg font-medium text-gray-900">{{ user.nickname }}</h3>
          <p class="text-sm text-gray-500">{{ user.useremail }}</p>
        </div>
      </div>
      
      <div class="border-t pt-4">
        <div class="grid grid-cols-2 gap-4 text-center">
          <div>
            <p class="text-sm text-gray-500">작성한 글</p>
            <p class="text-lg font-semibold text-gray-900">{{ user.articles?.length || 0 }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">작성한 댓글</p>
            <p class="text-lg font-semibold text-gray-900">{{ user.comments?.length || 0 }}</p>
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
defineProps({
  user: {
    type: Object,
    required: true
  }
})
</script> 