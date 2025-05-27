import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  // 상태 추가
  const lastAction = ref(null)

  // 비디오 모달
  const videoModalData = ref(null)
  const showVideoModal = ref(false)

  // 상품 상세 모달
  const productDetailData = ref(null)
  const showProductDetailModal = ref(false)

  // 게시글 작성 모달
  const articleFormModalData = ref({
    type: 'create', // 'create' | 'edit'
    article: null,
    onSubmit: null
  })
  const showArticleFormModal = ref(false)

  // 게시글 상세 모달
  const articleDetailData = ref(null)
  const showArticleDetailModal = ref(false)

  // 비디오 모달 제어
  const openVideoModal = (video) => {
    videoModalData.value = video
    showVideoModal.value = true
    document.body.style.overflow = 'hidden'
  }

  const closeVideoModal = () => {
    videoModalData.value = null
    showVideoModal.value = false
    document.body.style.overflow = ''
  }

  // 상품 상세 모달 제어
  const openProductDetailModal = (product, callbacks = {}) => {
    productDetailData.value = { ...product, callbacks }
    showProductDetailModal.value = true
    document.body.style.overflow = 'hidden'
  }

  const closeProductDetailModal = () => {
    const callbacks = productDetailData.value?.callbacks
    productDetailData.value = null
    showProductDetailModal.value = false
    document.body.style.overflow = ''
    
    // 콜백 실행
    if (callbacks?.onClose) {
      callbacks.onClose()
    }
  }

  // 북마크 상태 업데이트 처리
  const handleBookmarkUpdate = (productId, isBookmarked) => {
    lastAction.value = 'bookmark_update'
    if (productDetailData.value?.callbacks?.onBookmarkUpdated) {
      productDetailData.value.callbacks.onBookmarkUpdated({ productId, isBookmarked })
    }
  }

  // 게시글 작성 모달 제어
  const openArticleFormModal = ({ type = 'create', article = null, onSubmit = null }) => {
    articleFormModalData.value = {
      type,
      article,
      onSubmit
    }
    showArticleFormModal.value = true
    document.body.style.overflow = 'hidden'
  }

  const closeArticleFormModal = () => {
    articleFormModalData.value = {
      type: 'create',
      article: null,
      onSubmit: null
    }
    showArticleFormModal.value = false
    document.body.style.overflow = ''
  }

  // 게시글 상세 모달 제어
  const openArticleDetailModal = (article) => {
    articleDetailData.value = article
    showArticleDetailModal.value = true
    document.body.style.overflow = 'hidden'
  }

  const closeArticleDetailModal = () => {
    articleDetailData.value = null
    showArticleDetailModal.value = false
    document.body.style.overflow = ''
    lastAction.value = 'article_modal_closed'
  }

  return {
    // 비디오 모달
    videoModalData,
    showVideoModal,
    openVideoModal,
    closeVideoModal,

    // 상품 상세 모달
    productDetailData,
    showProductDetailModal,
    openProductDetailModal,
    closeProductDetailModal,

    // 게시글 작성 모달
    articleFormModalData,
    showArticleFormModal,
    openArticleFormModal,
    closeArticleFormModal,

    // 게시글 상세 모달
    articleDetailData,
    showArticleDetailModal,
    openArticleDetailModal,
    closeArticleDetailModal,

    // 북마크 관련
    lastAction,
    handleBookmarkUpdate,
  }
}) 