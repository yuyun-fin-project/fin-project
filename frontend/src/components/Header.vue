<template>
  <header class="header">
    <router-link to="/" class="logo">Bank</router-link>
    <nav class="nav">
      <router-link to="/products" active-class="active">금융</router-link>
      <router-link to="/recommend" active-class="active">추천</router-link>
      <router-link to="/community" active-class="active">커뮤니티</router-link>
      <router-link to="/mydata" active-class="active">마이데이터</router-link>
      <router-link to="/login" class="login-btn">로그인</router-link>
    </nav>
  </header>
</template>

<script setup lang="ts">
// 불필요한 라우터 메서드 제거
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0rem;
  /* background-color: #ffffff; */
  /* box-shadow: 0 2px 10px rgba(0,0,0,0.05); */
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3182f6;
  cursor: pointer;
  text-decoration: none;
}

.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav a {
  color: #333;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
  font-weight: 500;
  font-size: 1rem;
}

.nav a:hover {
  color: #3182f6;
}

.nav a.active {
  color: #3182f6;
  font-weight: 600;
}

.login-btn {
  background-color: #3182f6;
  color: white !important;
  padding: 0.5rem 1.5rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 600 !important;
}

.login-btn:hover {
  background-color: #1e6ee9;
}
</style>
