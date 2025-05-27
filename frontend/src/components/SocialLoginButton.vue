<template>
  <a :href="authUrl" class="login-btn" :class="provider">
    <img :src="getProviderIcon" :alt="`${provider} icon`" class="provider-icon" />
    {{ label }}
  </a>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  provider: 'google' | 'kakao',
  label: string,
  authUrl: string,
}>()

const getProviderIcon = computed(() => {
  const icons = {
    google: 'https://www.google.com/favicon.ico',
    kakao: 'https://developers.kakao.com/assets/img/about/logos/kakaolink/kakaolink_btn_small.png'
  }
  return icons[props.provider]
})
</script>

<style scoped>
.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  position: relative;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.12);
}

.provider-icon {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  object-fit: contain;
}

.google {
  background-color: white;
  color: #444;
}

.google:hover {
  background-color: #f8f9fa;
}

.kakao {
  background-color: #FEE500;
  color: #000000;
}

.kakao:hover {
  background-color: #FEE000;
}
</style>
