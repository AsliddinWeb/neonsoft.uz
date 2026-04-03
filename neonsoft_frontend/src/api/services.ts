import api from './axios'
import type { Service } from '@/types'

export const servicesApi = {
  list: () => api.get<Service[]>('/api/services'),
  get: (slug: string) => api.get<Service>(`/api/services/${slug}`),

  adminList: () => api.get<Service[]>('/api/admin/services'),
  create: (data: Partial<Service>) => api.post<Service>('/api/admin/services', data),
  update: (id: number, data: Partial<Service>) =>
    api.put<Service>(`/api/admin/services/${id}`, data),
  delete: (id: number) => api.delete(`/api/admin/services/${id}`),
}
