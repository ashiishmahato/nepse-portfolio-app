import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Stocks API
export const stocksAPI = {
  initialize: () => api.get('/stocks/initialize'),
  listAll: () => api.get('/stocks/list'),
  getStock: (symbol) => api.get(`/stocks/${symbol}`),
  searchStocks: (query) => api.get('/stocks/search', { params: { query } }),
  getHistory: (symbol, days = 60) => api.get(`/stocks/${symbol}/history`, { params: { days } }),
  getTechnicalAnalysis: (symbol) => api.get(`/stocks/${symbol}/technical-analysis`),
  updatePrices: () => api.post('/stocks/update-prices'),
}

// Portfolio API
export const portfolioAPI = {
  addStock: (data) => api.post('/portfolio/add', data),
  getList: (includeSold = false) => api.get('/portfolio/list', { params: { include_sold: includeSold } }),
  getItem: (id) => api.get(`/portfolio/${id}`),
  update: (id, data) => api.put(`/portfolio/${id}`, data),
  remove: (id) => api.delete(`/portfolio/${id}`),
  getDashboard: () => api.get('/portfolio/dashboard/summary'),
}

// Alerts API
export const alertsAPI = {
  getAll: (activeOnly = true, limit = 50) => 
    api.get('/alerts/', { params: { active_only: activeOnly, limit } }),
  getByStock: (symbol, activeOnly = true) => 
    api.get(`/alerts/by-stock/${symbol}`, { params: { active_only: activeOnly } }),
  getAlert: (id) => api.get(`/alerts/${id}`),
  markAsRead: (id) => api.put(`/alerts/${id}/mark-as-read`),
  deactivate: (id) => api.put(`/alerts/${id}/deactivate`),
  generate: () => api.post('/alerts/generate'),
}

export default api
