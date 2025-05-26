<template>
<div class="recommend-gpt">
    <input 
    type="number" 
    v-model.number="income" 
    placeholder="월 소득을 입력해주세요."
    :disabled="isLoading"
    class="input-field"
    >
    <button 
    @click="analyzeAndRecommend" 
    :disabled="isLoading || !income"
    class="submit-btn"
    >
    {{ isLoading ? '분석 중...' : '분석하기' }}
    </button>
    
    <div v-if="error" class="error-message">
        {{ error }}
    </div>
    
    <!-- Loading Steps -->
    <div v-if="isLoading" class="loading-steps space-y-4 p-6 bg-white rounded-lg shadow-md">
        <div class="flex items-start" :class="{ 'opacity-50': currentStep > 1 }">
            <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mr-3" 
                 :class="currentStep > 1 ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'">
                <span v-if="currentStep > 1">✓</span>
                <span v-else>1</span>
            </div>
            <div>
                <p class="font-medium text-gray-800">월 소비액 확인 중...</p>
                <p class="text-sm text-gray-500">귀하의 월별 소비 내역을 분석하고 있습니다.</p>
            </div>
        </div>
        
        <div class="flex items-start" :class="{ 'opacity-50': currentStep > 2 }">
            <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mr-3"
                 :class="currentStep > 2 ? 'bg-green-100 text-green-600' : currentStep === 2 ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-400'">
                <span v-if="currentStep > 2">✓</span>
                <span v-else>2</span>
            </div>
            <div>
                <p class="font-medium text-gray-800">불필요한 소비 분석 중...</p>
                <p class="text-sm text-gray-500">절약이 가능한 항목을 찾고 있습니다.</p>
            </div>
        </div>
        
        <div class="flex items-start">
            <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mr-3"
                 :class="currentStep === 3 ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-400'">
                <span v-if="currentStep > 3">✓</span>
                <span v-else>3</span>
            </div>
            <div>
                <p class="font-medium text-gray-800">추천 소비 전략 분석 중...</p>
                <p class="text-sm text-gray-500">최적의 소비 전략을 수립하고 있습니다.</p>
            </div>
        </div>
    </div>
    
    <div v-if="recommendation && !isLoading" class="recommendation-result">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">📊 소비 분석 리포트</h3>
    <!-- Current Spending Summary -->
    <div class="summary-card bg-blue-50 p-4 rounded-lg mb-4">
        <div class="flex justify-between items-center">
            <span class="text-gray-600">현재 월 소비액</span>
            <span class="text-xl font-bold text-blue-700">{{ recommendation.recommendation.current_spending }}</span>
        </div>
        <div class="mt-2 text-sm text-gray-600">
            {{ recommendation.recommendation.income_spending_ratio }}
        </div>
    </div>

    <!-- Unnecessary Spending -->
    <div class="bg-red-50 p-4 rounded-lg mb-4">
        <div class="flex items-center text-red-700 mb-2">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <span class="font-medium">절약 가능 항목</span>
        </div>
        <div class="flex flex-wrap gap-2 mb-2">
            <span v-for="(item, index) in recommendation.recommendation.unnecessary_items" 
                :key="index" 
                class="bg-white text-red-600 px-3 py-1 rounded-full text-sm font-medium shadow-sm">
            {{ item }}
            </span>
        </div>
        <div class="text-sm text-gray-600">
            <span>약 {{ recommendation.recommendation.possible_reduction }} 절약 가능</span>
        </div>
    </div>

    <!-- Key Insights -->
    <div class="key-insights space-y-3 mb-4">
        <div v-if="recommendation.recommendation.card_spending_focus" class="flex items-start">
            <span class="text-yellow-500 mr-2">💳</span>
            <span class="text-sm">{{ recommendation.recommendation.card_spending_focus }}</span>
        </div>
        <div v-if="recommendation.recommendation.spending_trend" class="flex items-start">
            <span class="text-blue-500 mr-2">📈</span>
            <span class="text-sm">{{ recommendation.recommendation.spending_trend }}</span>
        </div>
        <div v-if="recommendation.recommendation.subscription_check" class="flex items-start">
            <span class="text-purple-500 mr-2">🔍</span>
            <span class="text-sm">{{ recommendation.recommendation.subscription_check }}</span>
        </div>
    </div>

    <!-- Emergency Saving Advice -->
    <div v-if="recommendation.recommendation.emergency_saving_advice" class="bg-green-50 p-4 rounded-lg mb-4">
        <div class="flex items-center text-green-700 mb-1">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="font-medium">비상금 저축 제안</span>
        </div>
        <p class="text-sm text-gray-700">{{ recommendation.recommendation.emergency_saving_advice }}</p>
    </div>

    <!-- Main Recommendation -->
    <div class="bg-indigo-50 p-4 rounded-lg">
        <div class="flex items-center text-indigo-700 mb-2">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <span class="font-medium">AI 추천 전략</span>
        </div>
        <p class="text-sm text-gray-800">{{ recommendation.recommendation.recommendation }}</p>
    </div>
    </div>
</div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import axios from 'axios'

const income = ref(0)
const isLoading = ref(false)
const error = ref(null)
const recommendation = ref(null)
const currentStep = ref(1)
const analysisTimer = ref(null)

const startAnalysisSteps = () => {
  currentStep.value = 1
  
  // Step 1 to 2 after 1.3 seconds
  setTimeout(() => {
    if (isLoading.value) currentStep.value = 2
  }, 1300)
  
  // Step 2 to 3 after 2.6 seconds
  setTimeout(() => {
    if (isLoading.value) currentStep.value = 3
  }, 2600)
}

const clearTimers = () => {
  if (analysisTimer.value) {
    clearTimeout(analysisTimer.value)
    analysisTimer.value = null
  }
}

// Create an axios instance with default config
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

// Add request interceptor to include auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config
        
        // If error is not 401 or we've already tried to refresh, reject
        if (error.response?.status !== 401 || originalRequest._retry) {
            return Promise.reject(error)
        }
    
        originalRequest._retry = true
    
        try {
            // Try to refresh the token
            const refreshToken = localStorage.getItem('refresh_token')
            if (!refreshToken) throw new Error('No refresh token available')
      
            const response = await axios.post('http://127.0.0.1:8000/accounts/token/refresh/', {
                refresh: refreshToken
            })
      
            // Save the new tokens
            localStorage.setItem('access_token', response.data.access)
            if (response.data.refresh) {
                localStorage.setItem('refresh_token', response.data.refresh)
            }
      
            // Update the Authorization header
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`
      
            // Retry the original request
            return api(originalRequest)
        } catch (refreshError) {
            // If refresh fails, redirect to login
            console.error('Token refresh failed:', refreshError)
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            window.location.href = '/login'
            return Promise.reject(refreshError)
        }
    }
)

const analyzeAndRecommend = async () => {
  if (!income.value) {
    error.value = '월 소득을 입력해주세요.'
    return
  }
  
  // Reset states
  isLoading.value = true
  error.value = null
  recommendation.value = null
  clearTimers()
  
  // Start the step-by-step loading UI
  startAnalysisSteps()
  
  try {
    // Simulate minimum 4 second loading
    const startTime = Date.now()
    
    // Make the API call
    const response = await api.post('/mydata/ai/', {
      income: income.value
    })
    
    // Calculate remaining time to ensure minimum 4 second loading
    const endTime = Date.now()
    const timeElapsed = endTime - startTime
    const minLoadingTime = 4000 // 4 seconds
    const remainingTime = Math.max(0, minLoadingTime - timeElapsed)
    
    // Wait for remaining time if needed
    if (remainingTime > 0) {
      await new Promise(resolve => setTimeout(resolve, remainingTime))
    }
    
    // Update with actual data
    recommendation.value = response.data
    
  } catch (err) {
    console.error('Error during analysis:', err)
    
    if (err.response) {
      if (err.response.status === 401) {
        error.value = '로그인이 필요합니다. 로그인 페이지로 이동합니다.'
        setTimeout(() => {
          window.location.href = '/login'
        }, 2000)
      } else if (err.response.data?.detail) {
        error.value = err.response.data.detail
      } else {
        error.value = `서버 오류가 발생했습니다. (${err.response.status})`
      }
    } else if (err.request) {
      error.value = '서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.'
    } else {
      error.value = '요청을 처리하는 중 오류가 발생했습니다.'
    }
  } finally {
    isLoading.value = false
    clearTimers()
  }
}

// Clean up timers when component is unmounted
onUnmounted(() => {
  clearTimers()
})
</script>

<style scoped>
.recommend-gpt {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
}

.input-field {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    color: #334155;
    background-color: #f9fafb;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
}

.input-field:focus {
    font-color: #334155;
    outline: none;
    border-color: #4f46e5;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

.submit-btn {
    width: 100%;
    padding: 0.75rem;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover {
    background-color: #4338ca;
}

.submit-btn:disabled {
    background-color: #c7d2fe;
    cursor: not-allowed;
}

.error-message {
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #fee2e2;
    color: #b91c1c;
    border-radius: 8px;
    font-size: 0.875rem;
}

.loading-steps .flex {
  transition: opacity 0.3s ease;
}

.recommendation-result {
    margin-top: 1.5rem;
    padding: 1rem;
    background-color: #f8fafc;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}

.recommendation-result h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
    color: #1e293b;
    font-size: 1.125rem;
    font-weight: 600;
}

.recommendation-result pre {
    margin: 0;
    white-space: pre-wrap;
    font-family: inherit;
    color: #334155;
    line-height: 1.5;
}

.key-insights span {
    margin-top: 1rem;
    color: #334155;
}
</style>