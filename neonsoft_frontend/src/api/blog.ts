import api from './axios'
import type { BlogPost } from '@/types'

export const blogApi = {
  list: (params?: { page?: number; limit?: number; tag?: string }) =>
    api.get<BlogPost[]>('/api/blog', { params }),
  get: (slug: string) => api.get<BlogPost>(`/api/blog/${slug}`),

  adminList: (params?: { page?: number; limit?: number }) =>
    api.get<BlogPost[]>('/api/admin/blog', { params }),
  create: (data: Partial<BlogPost>) => api.post<BlogPost>('/api/admin/blog', data),
  update: (id: number, data: Partial<BlogPost>) =>
    api.put<BlogPost>(`/api/admin/blog/${id}`, data),
  delete: (id: number) => api.delete(`/api/admin/blog/${id}`),
}
