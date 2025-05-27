import { ref } from 'vue'

// 디바운스 훅
export const useDebounce = (callback, delay = 300) => {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => callback(...args), delay)
  }
}

// 검색 기록 관리
export const useSearchHistory = () => {
  const MAX_HISTORY = 10

  const getHistory = () => {
    try {
      return JSON.parse(localStorage.getItem('search_history')) || []
    } catch {
      return []
    }
  }

  const addToHistory = (term) => {
    if (!term.trim()) return

    const history = getHistory()
    const newHistory = [
      term,
      ...history.filter(item => item !== term)
    ].slice(0, MAX_HISTORY)

    localStorage.setItem('search_history', JSON.stringify(newHistory))
  }

  const clearHistory = () => {
    localStorage.removeItem('search_history')
  }

  return {
    getHistory,
    addToHistory,
    clearHistory
  }
}

// URL 쿼리 파라미터 관리
export const useQueryParams = (router) => {
  const updateQueryParams = (params) => {
    const query = { ...router.currentRoute.value.query }
    Object.entries(params).forEach(([key, value]) => {
      if (value) {
        query[key] = value
      } else {
        delete query[key]
      }
    })
    router.push({ query })
  }

  const getQueryParams = () => {
    return router.currentRoute.value.query
  }

  return {
    updateQueryParams,
    getQueryParams
  }
}

// 정렬 함수들
export const sortFunctions = {
  interestRate: (a, b) => b.interest_rate - a.interest_rate,
  bankName: (a, b) => a.bank_name.localeCompare(b.bank_name),
  period: (a, b) => a.period - b.period,
  amount: (a, b) => a.min_amount - b.min_amount
}

// 필터 함수
export function filterProducts(products, filters) {
  return products.filter(product => {
    const nameMatch = !filters.searchTerm || 
      product.name.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      product.bank_name.toLowerCase().includes(filters.searchTerm.toLowerCase())
    
    const bankMatch = !filters.bank || 
      product.bank_code === filters.bank
    
    const periodMatch = !filters.period || 
      product.period === parseInt(filters.period)
    
    const minAmountMatch = !filters.minAmount || 
      product.min_amount >= filters.minAmount
    
    const maxAmountMatch = !filters.maxAmount || 
      product.min_amount <= filters.maxAmount
    
    const typeMatch = !filters.productType || 
      product.type === filters.productType

    return nameMatch && bankMatch && periodMatch && 
           minAmountMatch && maxAmountMatch && typeMatch
  })
} 