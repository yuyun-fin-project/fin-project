import { ref } from 'vue'

// 디바운스 함수
export function useDebounce(value, delay = 300) {
  let timeout
  return new Promise(resolve => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      resolve(value)
    }, delay)
  })
}

// 검색 히스토리 관리
export function useSearchHistory(key = 'search_history', maxItems = 5) {
  const getHistory = () => {
    const history = localStorage.getItem(key)
    return history ? JSON.parse(history) : []
  }

  const addToHistory = (term) => {
    if (!term.trim()) return
    
    const history = getHistory()
    const newHistory = [
      term,
      ...history.filter(item => item !== term)
    ].slice(0, maxItems)
    
    localStorage.setItem(key, JSON.stringify(newHistory))
  }

  const clearHistory = () => {
    localStorage.removeItem(key)
  }

  return {
    getHistory,
    addToHistory,
    clearHistory
  }
}

// URL 쿼리 파라미터 관리
export function useQueryParams(router) {
  const updateQueryParams = (params) => {
    router.push({
      query: {
        ...router.currentRoute.value.query,
        ...params
      }
    })
  }

  const getQueryParams = () => {
    return router.currentRoute.value.query
  }

  return {
    updateQueryParams,
    getQueryParams
  }
}

// 정렬 함수
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