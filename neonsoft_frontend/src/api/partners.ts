import api from './axios'

export interface Partner {
  id: number
  name: string
  logo_url: string | null
  website_url: string | null
  order: number
  is_active: boolean
}

export const partnersApi = {
  list: () => api.get<Partner[]>('/api/partners').then(r => r.data),
  adminList: () => api.get<Partner[]>('/api/admin/partners').then(r => r.data),
  create: (data: Partial<Partner>) => api.post<Partner>('/api/admin/partners', data).then(r => r.data),
  update: (id: number, data: Partial<Partner>) => api.put<Partner>(`/api/admin/partners/${id}`, data).then(r => r.data),
  remove: (id: number) => api.delete(`/api/admin/partners/${id}`),
}