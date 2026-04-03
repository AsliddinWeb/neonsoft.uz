import api from './axios'
import type { TeamMember } from '@/types'

export const teamApi = {
  list: () => api.get<TeamMember[]>('/api/team'),

  adminList: () => api.get<TeamMember[]>('/api/admin/team'),
  create: (data: Partial<TeamMember>) => api.post<TeamMember>('/api/admin/team', data),
  update: (id: number, data: Partial<TeamMember>) =>
    api.put<TeamMember>(`/api/admin/team/${id}`, data),
  delete: (id: number) => api.delete(`/api/admin/team/${id}`),
}
