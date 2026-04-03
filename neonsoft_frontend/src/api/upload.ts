import api from './axios'

export const uploadApi = {
  image: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.post<{ url: string }>('/api/upload/image', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
