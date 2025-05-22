<template>
  <section class="hero">
    <div class="space-y-6">
      <h1 
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="300"
        :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
        class="mb-4"
      >
        당신의 자산을 더 똑똑하게
      </h1>
      <p 
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="500"
        :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
        class="mb-8"
      >
        모든 금융 데이터를 연결해 분석하고 추천까지!
      </p>
      <button
        v-motion
        :initial="{ opacity: 0, y: 40 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="700"
        :transition="{ type: 'spring', damping: 25, stiffness: 100 }"
        class="hover:bg-blue-600 transition-all duration-300 ease-out hover:shadow-xl transform hover:-translate-y-1"
      >
        지금 시작하기
      </button>
    </div>
  </section>
</template>

<script setup lang="ts"></script>

<style scoped>
.hero {
  @apply flex items-center justify-center min-h-[70vh] text-center p-8;
  background: linear-gradient(180deg, #eaf3ff 0%, white 100%);
}

.hero h1 {
  @apply text-4xl md:text-5xl font-bold text-gray-900;
}

.hero p {
  @apply text-lg md:text-xl text-gray-600;
}

.hero button {
  @apply bg-blue-500 text-white px-8 py-3 rounded-full text-lg font-medium shadow-lg;
}
</style>
