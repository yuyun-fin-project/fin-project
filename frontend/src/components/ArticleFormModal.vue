<template>
  <div class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="modal-content bg-white rounded-lg p-6 w-full max-w-2xl">
      <h2 class="text-2xl font-bold mb-4">{{ isEdit ? '게시글 수정' : '새 게시글 작성' }}</h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">제목</label>
          <input
            v-model="form.title"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">내용</label>
          <textarea
            v-model="form.content"
            rows="6"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          ></textarea>
        </div>
        
        <div class="flex justify-end space-x-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            취소
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {{ isEdit ? '수정' : '작성' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const isEdit = props.article !== null

const form = ref({
  title: props.article?.title || '',
  content: props.article?.content || ''
})

const handleSubmit = () => {
  emit('submit', {
    title: form.value.title,
    content: form.value.content
  })
}
</script> 