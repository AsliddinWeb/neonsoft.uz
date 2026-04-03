import api from './axios'
import type { User } from '@/types'

export const usersApi = {
  list: () => api.get<User[]>('/api/admin/users'),
  create: (data: { email: string; full_name: string; password: string; role: string }) =>
    api.post<User>('/api/admin/users', data),
  toggleActive: (id: number) => api.patch<User>(`/api/admin/users/${id}/toggle-active`),
  delete: (id: number) => api.delete(`/api/admin/users/${id}`),
}
