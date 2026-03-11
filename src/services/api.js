import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Auth store reference — set via setupInterceptors() to avoid circular imports
let _getAuthStore = null

export function setupInterceptors(getAuthStore) {
  _getAuthStore = getAuthStore
}

// Request interceptor to add JWT token from memory
api.interceptors.request.use((config) => {
  if (_getAuthStore) {
    const auth = _getAuthStore()
    if (auth.token) {
      config.headers.Authorization = `Bearer ${auth.token}`
    }
  }
  return config
})

// Response interceptor: on 401, attempt refresh once, then retry
let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error)
    } else {
      resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Don't intercept login or refresh requests
    if (
      error.response?.status !== 401 ||
      originalRequest._retry ||
      originalRequest.url === '/auth/login' ||
      originalRequest.url === '/auth/refresh' ||
      !_getAuthStore
    ) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const auth = _getAuthStore()
      const refreshed = await auth.refreshToken()
      if (refreshed) {
        processQueue(null, auth.token)
        originalRequest.headers.Authorization = `Bearer ${auth.token}`
        return api(originalRequest)
      } else {
        processQueue(new Error('Refresh failed'))
        auth.logout()
        return Promise.reject(error)
      }
    } catch (refreshError) {
      processQueue(refreshError)
      try { _getAuthStore().logout() } catch { /* ignore */ }
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export default api

// Auth API
export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  refresh: () => api.post('/auth/refresh'),
  profile: () => api.get('/auth/profile'),
  changePassword: (data) => api.post('/auth/password', data),
  forgotPassword: (data) => api.post('/auth/forgot-password', data),
}

// Children API
export const childrenApi = {
  getAll: () => api.get('/children'),
  getDetail: (id) => api.get(`/children/${id}`),
  getSiblings: (id) => api.get(`/children/${id}/siblings`),
}

// Attendance API
export const attendanceApi = {
  getByStudent: (id, params) => api.get(`/attendance/${id}`, { params }),
  getSummary: (id) => api.get(`/attendance/${id}/summary`),
}

// Invoices API
export const invoicesApi = {
  getAll: (params) => api.get('/invoices', { params }),
  getDetail: (id) => api.get(`/invoices/${id}`),
}

// Payments API
export const paymentsApi = {
  getAll: (params) => api.get('/payments', { params }),
  create: (data) => api.post('/payments', data),
  getBalance: () => api.get('/payments/balance'),
  getSummary: () => api.get('/payments/summary'),
}

// Subscriptions API
export const subscriptionsApi = {
  getAll: (params) => api.get('/subscriptions', { params }),
  getDetail: (id) => api.get(`/subscriptions/${id}`),
}

// Content API
export const contentApi = {
  getCategories: () => api.get('/content/categories'),
  getItems: (params) => api.get('/content/items', { params }),
  getDetail: (id, params) => api.get(`/content/items/${id}`, { params }),
}

// Kids Area API
export const kidsAreaApi = {
  getServices: () => api.get('/kidsarea/services'),
  getSlots: (params) => api.get('/kidsarea/slots', { params }),
  getBookings: () => api.get('/kidsarea/bookings'),
  createBooking: (data) => api.post('/kidsarea/bookings', data),
  cancelBooking: (id) => api.delete(`/kidsarea/bookings/${id}/cancel`),
  getPackages: () => api.get('/kidsarea/packages'),
}

// Messages API
export const messagesApi = {
  getAll: (params) => api.get('/messages', { params }),
  send: (data) => api.post('/messages', data),
  markRead: (id) => api.post(`/messages/${id}/read`),
  getUnreadCount: () => api.get('/messages/unread-count'),
}

// Config API
export const configApi = {
  get: () => api.get('/config'),
  getDepartments: () => api.get('/config/departments'),
  getBranches: () => api.get('/config/branches'),
}

// Voice API
export const voiceApi = {
  evaluate: (data) => api.post('/voice/evaluate', data),
  getWords: (params) => api.get('/voice/words', { params }),
}
