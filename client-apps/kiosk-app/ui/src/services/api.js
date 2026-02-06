import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const kioskAPI = {
  // Generate QR code session
  generateQRSession: async () => {
    const response = await api.post('/api/kiosk/session/qr');
    return response.data;
  },

  // Get session status
  getSessionStatus: async (sessionId) => {
    const response = await api.get(`/api/kiosk/session/${sessionId}/status`);
    return response.data;
  },

  // Link session (called from user's device)
  linkSession: async (sessionId, userId, deviceInfo = {}) => {
    const response = await api.post('/api/kiosk/session/link', {
      session_id: sessionId,
      user_id: userId,
      device_info: deviceInfo,
    });
    return response.data;
  },

  // Get all kiosk data (session + cart + history)
  getKioskData: async (sessionId) => {
    const response = await api.get(`/api/kiosk/data/${sessionId}`);
    return response.data;
  },

  // Get shopping cart
  getShoppingCart: async (userId) => {
    const response = await api.get(`/api/kiosk/cart/${userId}`);
    return response.data;
  },

  // Get purchase history
  getPurchaseHistory: async (userId) => {
    const response = await api.get(`/api/kiosk/history/${userId}`);
    return response.data;
  },
};

export default api;

