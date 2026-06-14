import axios from 'axios'

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
// In production set VITE_API_URL to your hosted backend URL.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
})

// ---------- customers ----------
export const getCustomers = (params = {}) =>
  api.get('/api/customers/', { params }).then((r) => r.data)

export const getCustomer = (id) =>
  api.get(`/api/customers/${id}`).then((r) => r.data)

// ---------- segments ----------
export const getSegments = () => api.get('/api/segments/').then((r) => r.data)

export const createSegment = (payload) =>
  api.post('/api/segments/', payload).then((r) => r.data)

export const previewSegment = (rules) =>
  api.post('/api/segments/preview', rules).then((r) => r.data)

export const deleteSegment = (id) =>
  api.delete(`/api/segments/${id}`).then((r) => r.data)

// ---------- campaigns ----------
export const getCampaigns = () => api.get('/api/campaigns/').then((r) => r.data)

export const getCampaign = (id) =>
  api.get(`/api/campaigns/${id}`).then((r) => r.data)

export const createCampaign = (payload) =>
  api.post('/api/campaigns/', payload).then((r) => r.data)

export const launchCampaign = (id) =>
  api.post(`/api/campaigns/${id}/launch`).then((r) => r.data)

export const getCampaignStats = (id) =>
  api.get(`/api/campaigns/${id}/stats`).then((r) => r.data)

// ---------- analytics ----------
export const getOverview = () =>
  api.get('/api/analytics/overview').then((r) => r.data)

export const getAnalyticsCampaigns = () =>
  api.get('/api/analytics/campaigns').then((r) => r.data)

// ---------- ai ----------
export const aiBuildSegment = (prompt) =>
  api.post('/api/ai/build-segment', { prompt }).then((r) => r.data)

export const aiWriteMessage = (payload) =>
  api.post('/api/ai/write-message', payload).then((r) => r.data)

export const aiInsights = (campaignId) =>
  api.get(`/api/ai/insights/${campaignId}`).then((r) => r.data)

export const aiCreateCampaign = (intent) =>
  api.post('/api/ai/create-campaign', { intent }).then((r) => r.data)

export default api
