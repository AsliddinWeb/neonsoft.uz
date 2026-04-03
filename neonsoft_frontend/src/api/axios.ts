import axios from 'axios'
import { useToast } from 'vue-toastification'

const api = axios.create({
  baseURL: '',
})

// ─── Request interceptor — attach token ───────────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ─── Response interceptor ─────────────────────────────────────────────────────
let isRefreshing = false
let failedQueue: Array<{ resolve: (v: string) => void; reject: (e: unknown) => void }> = []

function processQueue(error: unknown, token: string | null = null) {
  failedQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token!)))
  failedQueue = []
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const toast = useToast()
    const original = error.config

    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise<string>((resolve, reject) => failedQueue.push({ resolve, reject }))
          .then((token) => {
            original.headers.Authorization = `Bearer ${token}`
            return api(original)
          })
          .catch((e) => Promise.reject(e))
      }

      original._retry = true
      isRefreshing = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (!refreshToken) {
        isRefreshing = false
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/admin/login'
        return Promise.reject(error)
      }

      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/api/auth/refresh`,
          { refresh_token: refreshToken },
        )
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        processQueue(null, data.access_token)
        original.headers.Authorization = `Bearer ${data.access_token}`
        return api(original)
      } catch (err) {
        processQueue(err, null)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/admin/login'
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    const status = error.response?.status
    if (status === 403) {
      toast.error("Ruxsat yo'q")
    } else if (status === 422) {
      const detail = error.response?.data?.detail
      toast.error(typeof detail === 'string' ? detail : 'Validation xatosi')
    } else if (status === 500) {
      toast.error("Server xatosi. Keyinroq urinib ko'ring.")
    }

    return Promise.reject(error)
  },
)

export default api
