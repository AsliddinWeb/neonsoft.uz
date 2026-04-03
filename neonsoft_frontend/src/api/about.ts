import api from './axios'

export interface About {
  id: number
  title: string | null
  subtitle: string | null
  description: string | null
  image_url: string | null
  stat_projects: number
  stat_clients: number
  stat_years: number
  stat_team: number
}

export const aboutApi = {
  get: () => api.get<About>('/api/about').then(r => r.data),
  adminGet: () => api.get<About>('/api/admin/about').then(r => r.data),
  update: (data: Partial<About>) => api.put<About>('/api/admin/about', data).then(r => r.data),
}