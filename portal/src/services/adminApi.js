import api from './api'

export const adminApi = {
  getDashboard: () => api.get('/admin/dashboard'),
  getStudents: (params) => api.get('/admin/students', { params }),
  getParents: (params) => api.get('/admin/parents', { params }),
  getSubscriptions: (params) => api.get('/admin/subscriptions', { params }),
  getInvoices: (params) => api.get('/admin/invoices', { params }),
  getTeachers: (params) => api.get('/admin/teachers', { params }),
  getAttendance: (params) => api.get('/admin/attendance', { params }),
  getContent: (params) => api.get('/admin/content', { params }),
  getKidsArea: (params) => api.get('/admin/kidsarea', { params }),
  getMessages: (params) => api.get('/admin/messages', { params }),
  getOptions: () => api.get('/admin/options'),
  createStudent: (data) => api.post('/admin/students/create', data),
  createTeacher: (data) => api.post('/admin/teachers/create', data),
  createParent: (data) => api.post('/admin/parents/create', data),
  // Detail endpoints
  getStudent: (id) => api.get(`/admin/students/${id}`),
  getTeacher: (id) => api.get(`/admin/teachers/${id}`),
  getParent: (id) => api.get(`/admin/parents/${id}`),
  // Actions
  studentAction: (id, action) => api.post(`/admin/students/${id}/action`, { action }),
  teacherAction: (id, action) => api.post(`/admin/teachers/${id}/action`, { action }),
  parentAction: (id, action) => api.post(`/admin/parents/${id}/action`, { action }),
  // Detail endpoints (remaining)
  getSubscription: (id) => api.get(`/admin/subscriptions/${id}`),
  getInvoice: (id) => api.get(`/admin/invoices/${id}`),
  getAttendanceRecord: (id) => api.get(`/admin/attendance/${id}`),
  getContentItem: (id) => api.get(`/admin/content/${id}`),
  getBooking: (id) => api.get(`/admin/kidsarea/booking/${id}`),
  getMessage: (id) => api.get(`/admin/messages/${id}`),
  // Actions (remaining)
  subscriptionAction: (id, action) => api.post(`/admin/subscriptions/${id}/action`, { action }),
  attendanceAction: (id, action) => api.post(`/admin/attendance/${id}/action`, { action }),
  contentAction: (id, action) => api.post(`/admin/content/${id}/action`, { action }),
  bookingAction: (id, action) => api.post(`/admin/kidsarea/booking/${id}/action`, { action }),
  messageAction: (id, action) => api.post(`/admin/messages/${id}/action`, { action }),
  // Portal user management
  getPortalUsers: (params) => api.get('/admin/portal-accounts', { params }),
  createPortalUser: (data) => api.post('/admin/portal-user/create', data),
  togglePortalUser: (id) => api.post(`/admin/portal-user/${id}/toggle`),
  resetPortalPassword: (id, password) => api.post(`/admin/portal-user/${id}/reset-password`, { password }),
  // Subscription options (types, plans, content items for dropdowns)
  getSubscriptionOptions: () => api.get('/admin/subscription-options'),
  // Student subscriptions & content
  getStudentSubscriptions: (id) => api.get(`/admin/students/${id}/subscriptions`),
  getStudentContentAccess: (id) => api.get(`/admin/students/${id}/content-access`),
  grantContentToStudent: (id, data) => api.post(`/admin/students/${id}/grant-content`, data),
  createStudentSubscription: (id, data) => api.post(`/admin/students/${id}/create-subscription`, data),
  // Parent children data & grant
  getParentChildrenData: (id) => api.get(`/admin/parents/${id}/children-data`),
  grantContentToParentChildren: (id, data) => api.post(`/admin/parents/${id}/grant-content`, data),
  // Content access revoke
  revokeContentAccess: (id) => api.post(`/admin/content-access/${id}/revoke`),
  // Teacher portal user
  createTeacherPortalUser: (id, data) => api.post(`/admin/teachers/${id}/create-portal-user`, data),
}
