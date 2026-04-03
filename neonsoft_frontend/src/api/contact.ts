import api from './axios'
import type { ContactMessage } from '@/types'

export const contactApi = {
  send: (data: {
    full_name: string
    email: string
    phone?: string
    subject?: string
    message: string
  }) => api.post<ContactMessage>('/api/contact', data),

  adminList: (params?: { page?: number; limit?: number }) =>
    api.get<ContactMessage[]>('/api/admin/contacts', { params }),
  markRead: (id: number) =>
    api.patch<ContactMessage>(`/api/admin/contacts/${id}/read`),
  delete: (id: number) => api.delete(`/api/admin/contacts/${id}`),
}
