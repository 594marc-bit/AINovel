// import { api } from 'boot/axios'; // 暂时注释掉，MVP阶段不需要

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    username: string;
    email: string;
    is_active: boolean;
  };
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // TODO: 实现实际的登录 API
    // const response = await api.post('/auth/login', credentials);
    // return response.data;

    // 模拟登录（MVP阶段）
    await new Promise(resolve => setTimeout(resolve, 500));
    return {
      access_token: 'mock-token-' + Date.now(),
      token_type: 'bearer',
      user: {
        id: 1,
        username: credentials.username,
        email: `${credentials.username}@example.com`,
        is_active: true,
      }
    };
  },

  async register(): Promise<void> {
    // TODO: 实现实际的注册 API
    // await api.post('/auth/register', data);

    // 模拟注册（MVP阶段）
    await new Promise(resolve => setTimeout(resolve, 500));
  },

  async logout(): Promise<void> {
    // TODO: 实现实际的注销 API
    // await api.post('/auth/logout');

    // 模拟注销（MVP阶段）
    await new Promise(resolve => setTimeout(resolve, 300));
  },

  async getCurrentUser() {
    // TODO: 获取当前用户信息
    // const response = await api.get('/auth/me');
    // return response.data;

    // 模拟用户信息（MVP阶段）
    await new Promise(resolve => setTimeout(resolve, 300));
    return {
      id: 1,
      username: 'admin',
      email: 'admin@example.com',
      is_active: true,
      created_at: new Date().toISOString(),
    };
  }
};