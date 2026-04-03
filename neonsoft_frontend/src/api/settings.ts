import api from './axios'
import type { SiteSetting } from '@/types'

export const settingsApi = {
  get: () => api.get<SiteSetting>('/api/settings'),
  adminGet: () => api.get<SiteSetting>('/api/admin/settings'),
  update: (data: Partial<SiteSetting>) => api.put<SiteSetting>('/api/admin/settings', data),
}
