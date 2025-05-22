<template>
  <a :href="authUrl" class="login-btn" :class="provider">
    {{ label }}
  </a>
</template>

<script setup lang="ts">
defineProps<{
  provider: 'google' | 'kakao' | 'github',
  label: string,
  authUrl: string,
}>()
</script>

<style scoped>
.login-btn {
  display: inline-block;
  width: 250px;
  padding: 0.75rem 1rem;
  text-align: center;
  font-size: 1rem;
  border-radius: 9999px;
  color: white;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.2s ease;
}

.google {
  background-color: #db4437;
}
.kakao {
  background-color: #fee500;
  color: #333;
}
.github {
  background-color: #333;
}
</style>
