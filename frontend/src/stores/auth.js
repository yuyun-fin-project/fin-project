import { defineStore } from 'pinia'
import authService from '../services/authService'
import router from '../router'  // router 인스턴스 직접 import
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    isAuthenticated: false,
    user: null,
    refreshTokenTimeout: null,
    lastTokenCheck: 0,
    isRefreshing: false
  }),

  getters: {
    isTokenValid() {
      if (!this.accessToken) return false
      try {
        const decoded = jwtDecode(this.accessToken)
        const currentTime = Date.now() / 1000
        return decoded.exp > currentTime
      } catch {
        return false
      }
    }
  },

  actions: {
    async setAccessToken(token) {
      if (!token) {
        throw new Error('토큰이 제공되지 않았습니다.')
      }

      try {
        const decoded = jwtDecode(token)
        const currentTime = Date.now() / 1000
        
        if (decoded.exp <= currentTime) {
          throw new Error('만료된 토큰입니다.')
        }

        this.accessToken = token
        this.isAuthenticated = true
        localStorage.setItem('access_token', token)

        // 토큰 만료 5분 전에 갱신 시작
        const timeUntilExpiry = (decoded.exp - currentTime) * 1000
        const refreshTime = Math.max(timeUntilExpiry - 5 * 60 * 1000, 0)
        this.startRefreshTokenTimer(refreshTime)

        // 사용자 정보 가져오기
        const userData = await authService.getUserInfo()
        this.user = userData
        return userData
      } catch (error) {
        console.error('토큰 설정 실패:', error)
        this.clearAuth()
        throw error
      }
    },

    async checkAuth() {
      if (!this.accessToken) {
        this.clearAuth()
        return false
      }

      try {
        const now = Date.now()
        if (now - this.lastTokenCheck < 10000) {
          return this.isAuthenticated
        }

        if (!this.isTokenValid) {
          await this.refreshToken()
        }

        if (!this.user) {
          const userData = await authService.getUserInfo()
          this.user = userData
        }

        this.isAuthenticated = true
        this.lastTokenCheck = now
        return true
      } catch (error) {
        console.error('인증 확인 실패:', error)
        this.clearAuth()
        return false
      }
    },

    clearAuth() {
      this.accessToken = null
      this.isAuthenticated = false
      this.user = null
      this.isRefreshing = false
      localStorage.removeItem('access_token')
      this.stopRefreshTokenTimer()
      
      const cookies = ['refresh_token', 'csrftoken']
      cookies.forEach(cookieName => {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=localhost;`
      })
    },

    startRefreshTokenTimer(delay) {
      this.stopRefreshTokenTimer()
      
      if (delay <= 0) {
        this.refreshToken()
        return
      }

      this.refreshTokenTimeout = setTimeout(async () => {
        try {
          if (!this.isRefreshing) {
            await this.refreshToken()
          }
        } catch (error) {
          console.error('자동 토큰 갱신 실패:', error)
          this.clearAuth()
          router.push('/login')
        }
      }, delay)
    },

    stopRefreshTokenTimer() {
      if (this.refreshTokenTimeout) {
        clearTimeout(this.refreshTokenTimeout)
        this.refreshTokenTimeout = null
      }
    },

    async refreshToken() {
      if (this.isRefreshing) {
        return new Promise((resolve, reject) => {
          setTimeout(async () => {
            try {
              if (this.accessToken) {
                resolve(this.accessToken)
              } else {
                reject(new Error('토큰 갱신 실패'))
              }
            } catch (error) {
              reject(error)
            }
          }, 1000)
        })
      }

      this.isRefreshing = true

      try {
        if (!document.cookie.includes('refresh_token=')) {
          throw new Error('리프레시 토큰이 없습니다.')
        }

        const response = await authService.refreshToken()
        if (!response.access) {
          throw new Error('새로운 액세스 토큰을 받지 못했습니다.')
        }

        await this.setAccessToken(response.access)
        return response.access
      } catch (error) {
        console.error('토큰 갱신 실패:', error)
        this.clearAuth()
        router.push('/login')
        throw error
      } finally {
        this.isRefreshing = false
      }
    },

    async handleSocialLogin(provider, code) {
      try {
        const response = await authService.handleSocialLogin(provider, code)
        if (!response.access) {
          throw new Error('액세스 토큰을 받지 못했습니다.')
        }
        await this.setAccessToken(response.access)
        return response
      } catch (error) {
        console.error('소셜 로그인 실패:', error)
        this.clearAuth()
        throw error
      }
    },

    async logout() {
      try {
        await authService.logout()
      } catch (error) {
        console.error('로그아웃 API 호출 실패:', error)
      } finally {
        this.clearAuth()
      }
    }
  },

  persist: {
    paths: ['accessToken', 'isAuthenticated', 'user', 'lastTokenCheck']
  }
}) 