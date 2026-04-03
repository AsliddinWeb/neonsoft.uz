import api from './axios'
import type { Project } from '@/types'

export const projectsApi = {
  list: (params?: { featured?: boolean; page?: number; limit?: number }) =>
    api.get<Project[]>('/api/projects', { params }),
  get: (slug: string) => api.get<Project>(`/api/projects/${slug}`),

  adminList: (params?: { page?: number; limit?: number }) =>
    api.get<Project[]>('/api/admin/projects', { params }),
  create: (data: Partial<Project>) => api.post<Project>('/api/admin/projects', data),
  update: (id: number, data: Partial<Project>) =>
    api.put<Project>(`/api/admin/projects/${id}`, data),
  delete: (id: number) => api.delete(`/api/admin/projects/${id}`),
}
