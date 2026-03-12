import api from './api'

export const adminApi = {
  getDashboard: () => api.get('/admin/dashboard'),
  getStudents: (params) => api.get('/admin/students', { params }),
  getParents: (params) => api.get('/admin/parents', { params }),
  getSubscriptions: (params) => api.get('/admin/subscriptions', { params }),
  getInvoices: (params) => api.get('/admin/invoices', { params }),
}
