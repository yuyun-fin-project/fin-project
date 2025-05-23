import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    user: null,
    refreshTokenTimeout: null
  }),

  actions: {
    async setAccessToken(token) {
      if (!token) {
        throw new Error('토큰이 제공되지 않았습니다.');
      }

      this.accessToken = token;
      this.isAuthenticated = true;
      localStorage.setItem('access_token', token);
      
      // 토큰 저장 후 사용자 정보 가져오기
      try {
        const userData = await authService.getUserInfo();
        this.user = userData;
        this.startRefreshTokenTimer();
        return userData;
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error);
        this.clearAuth();
        throw error;
      }
    },

    async checkAuth() {
      if (!this.accessToken) {
        throw new Error('저장된 토큰이 없습니다.');
      }

      try {
        const userData = await authService.getUserInfo();
        this.user = userData;
        this.isAuthenticated = true;
        this.startRefreshTokenTimer();
        return userData;
      } catch (error) {
        this.clearAuth();
        throw error;
      }
    },

    clearAuth() {
      this.accessToken = null;
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('access_token');
      this.stopRefreshTokenTimer();
    },

    startRefreshTokenTimer() {
      this.stopRefreshTokenTimer();
      
      // 토큰 만료 4분 전에 갱신 (토큰 만료시간이 5분이라고 가정)
      this.refreshTokenTimeout = setTimeout(async () => {
        try {
          await this.refreshToken();
        } catch (error) {
          console.error('토큰 갱신 실패:', error);
          this.clearAuth();
        }
      }, 4 * 60 * 1000); // 4분
    },

    stopRefreshTokenTimer() {
      if (this.refreshTokenTimeout) {
        clearTimeout(this.refreshTokenTimeout);
        this.refreshTokenTimeout = null;
      }
    },

    async refreshToken() {
      try {
        const response = await authService.refreshToken();
        if (!response.access) {
          throw new Error('새로운 액세스 토큰을 받지 못했습니다.');
        }
        await this.setAccessToken(response.access);
        return response.access;
      } catch (error) {
        console.error('토큰 갱신 실패:', error);
        this.clearAuth();
        throw error;
      }
    },

    async handleSocialLogin(provider, code) {
      try {
        const response = await authService.handleSocialLogin(provider, code);
        if (!response.access) {
          throw new Error('액세스 토큰을 받지 못했습니다.');
        }
        await this.setAccessToken(response.access);
        return response;
      } catch (error) {
        console.error('소셜 로그인 실패:', error);
        this.clearAuth();
        throw error;
      }
    },

    async logout() {
      try {
        await authService.logout();
      } catch (error) {
        console.error('로그아웃 API 호출 실패:', error);
      } finally {
        // API 호출 결과와 관계없이 로컬 상태 정리
        this.clearAuth();
        window.location.href = '/login';
      }
    }
  },

  persist: {
    paths: ['accessToken', 'isAuthenticated', 'user']
  }
}) 