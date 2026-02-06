import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const getProducts = (params = {}) =>
  api.get('/api/products', { params }).then((r) => r.data);

export const getProduct = (id) =>
  api.get(`/api/products/${id}`).then((r) => r.data);

export const getCategories = () =>
  api.get('/api/categories').then((r) => r.data);

export const getRecommendations = (query, userId = 'default_user') =>
  api.post('/api/recommendations/voice', { query, user_id: userId }).then((r) => r.data);

export const purchase = (items, userId = 'default_user') =>
  api.post('/api/purchase', {
    user_id: userId,
    items: items.map((item) => ({
      product_id: item.product_id,
      sku: item.sku || item.product_id,
      quantity: item.quantity,
      size: item.size,
    })),
  }).then((r) => r.data);

export const healthCheck = () => api.get('/api/health').then((r) => r.data);
