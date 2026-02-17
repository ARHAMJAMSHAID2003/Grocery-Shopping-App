import axios from 'axios';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const BASE_URL = Platform.OS === 'web'
  ? 'http://localhost:8000/api'
  : 'http://localhost:8000/api';  // Change to your computer's IP if needed

const api = axios.create({ baseURL: BASE_URL });

// Attach JWT token to every request
api.interceptors.request.use(async (config) => {
  try {
    const token = await AsyncStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  } catch (e) {}
  return config;
});

// Auth
export const register = (data) => api.post('/register/', data);
export const login = (data) => api.post('/login/', data);
export const sendOtp = (data) => api.post('/send-otp/', data);
export const verifyOtp = (data) => api.post('/verify-otp/', data);
export const resendOtp = (data) => api.post('/resend-otp/', data);

// Products
export const getProducts = () => api.get('/products/');
export const getProduct = (id) => api.get(`/products/${id}/`);

// Cart
export const getCart = (userId) => api.get(`/cart/?user_id=${userId}`);
export const addToCart = (data) => api.post('/cart/', data);
export const removeFromCart = (id) => api.delete(`/cart/${id}/`);

// Orders
export const createOrder = (data) => api.post('/orders/', data);
export const getOrders = (userId) => api.get(`/orders/?user_id=${userId}`);
export const getOrderItems = (orderId) => api.get(`/order-items/?order_id=${orderId}`);

// Shopping List Parser
export const parseShoppingList = (data) => api.post('/parse-shopping-list/', data);
export const bulkAddToCart = (data) => api.post('/bulk-add-to-cart/', data);

export default api;
