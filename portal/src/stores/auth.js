import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // Token stored in memory only (not localStorage) to prevent XSS
  const token = ref(null)
  const parent = ref(null)
  const children = ref([])
  const loading = ref(false)
  const error = ref(null)
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const parentName = computed(() => parent.value?.name || '')
  const parentId = computed(() => parent.value?.id || null)

  function decodePayload(jwt) {
    try {
      const base64 = jwt.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
      return JSON.parse(atob(base64))
    } catch {
      return null
    }
  }

  function checkTokenExpiry() {
    if (!token.value) return false
    const payload = decodePayload(token.value)
    if (!payload?.exp) return false
    // Consider expired if less than 60s remaining
    return (payload.exp * 1000) > (Date.now() + 60000)
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.login(credentials)
      if (data.success) {
        token.value = data.token
        parent.value = data.parent
        children.value = data.children || []
        localStorage.setItem('logged_in', 'true')
        return true
      }
      error.value = data.message || 'فشل تسجيل الدخول'
      return false
    } catch (err) {
      error.value = err.response?.data?.message || 'خطأ في الاتصال'
      return false
    } finally {
      loading.value = false
    }
  }

  async function refreshToken() {
    try {
      const { data } = await authApi.refresh()
      if (data.success && data.token) {
        token.value = data.token
        if (data.parent) parent.value = data.parent
        if (data.children) children.value = data.children
        localStorage.setItem('logged_in', 'true')
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function fetchProfile() {
    try {
      const { data } = await authApi.profile()
      if (data.parent) parent.value = data.parent
      if (data.children) children.value = data.children
    } catch {
      // Profile fetch failed, non-critical
    }
  }

  async function initAuth() {
    const wasLoggedIn = localStorage.getItem('logged_in') === 'true'
    if (!wasLoggedIn) {
      initialized.value = true
      return false
    }

    const refreshed = await refreshToken()
    if (refreshed) {
      await fetchProfile()
      initialized.value = true
      return true
    }

    // Refresh failed — clear state
    localStorage.removeItem('logged_in')
    token.value = null
    parent.value = null
    children.value = []
    initialized.value = true
    return false
  }

  function logout() {
    token.value = null
    parent.value = null
    children.value = []
    localStorage.removeItem('logged_in')
    router.push('/login')
  }

  return {
    token, parent, children, loading, error, initialized,
    isAuthenticated, parentName, parentId,
    login, logout, refreshToken, checkTokenExpiry, initAuth, fetchProfile,
  }
})
