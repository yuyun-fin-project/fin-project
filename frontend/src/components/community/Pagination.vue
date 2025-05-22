<template>
  <div class="flex justify-center mt-6 space-x-2">
    <button
      v-for="page in totalPages"
      :key="page"
      @click="$emit('page-change', page)"
      :class="[
        'px-3 py-1 rounded-lg text-sm font-medium',
        page === currentPage ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      ]"
    >
      {{ page }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  currentPage: number
  totalPages: number
}>()

defineEmits(['page-change'])
</script>
