import { defineBoot } from '#q-app/wrappers';
import axios from 'axios';

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({
  baseURL: process.env.API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default defineBoot(({ app }) => {
  // 设置 axios 实例到全局
  app.config.globalProperties.$axios = api;
  app.config.globalProperties.$api = api;
});

export { api };