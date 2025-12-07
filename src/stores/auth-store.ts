import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export const useAuthStore = defineStore('auth', () => {
  // State - 固定的admin用户
  const user = ref<User>({
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    is_active: true,
    created_at: new Date().toISOString(),
  });

  const token = ref('admin-token');
  const loading = ref(false);

  // Getters
  const isAuthenticated = computed(() => true); // 总是已认证
  const userDisplayName = computed(() => user.value?.username || 'Admin');

  // Actions
  function initAuth() {
    // 不需要任何认证初始化
    return Promise.resolve(true);
  }

  function logout() {
    // MVP阶段不需要真正的登出
    console.log('Logout not implemented in MVP');
  }

  return {
    // State
    user,
    token,
    loading,

    // Getters
    isAuthenticated,
    userDisplayName,

    // Actions
    initAuth,
    logout,
  };
});