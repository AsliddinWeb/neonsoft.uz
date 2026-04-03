import api from './axios'
import type { User, TokenResponse } from '@/types'

export const authApi = {
  login: (email: string, password: string) =>
    api.post<TokenResponse>('/api/auth/login', { email, password }),

  refresh: (refresh_token: string) =>
    api.post<TokenResponse>('/api/auth/refresh', { refresh_token }),

  me: () => api.get<User>('/api/auth/me'),
}
