import { ref } from 'vue'
import { useToast } from 'vue-toastification'

export function useApi<T>() {
  const data = ref<T | null>(null)
  const list = ref<T[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const toast = useToast()

  async function fetch(apiFn: () => Promise<{ data: T[] }>) {
    loading.value = true
    error.value = null
    try {
      const res = await apiFn()
      list.value = res.data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Xato yuz berdi'
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(apiFn: () => Promise<{ data: T }>) {
    loading.value = true
    error.value = null
    try {
      const res = await apiFn()
      data.value = res.data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Xato yuz berdi'
    } finally {
      loading.value = false
    }
  }

  async function create(apiFn: () => Promise<{ data: T }>, successMsg = "Muvaffaqiyatli qo'shildi") {
    loading.value = true
    try {
      const res = await apiFn()
      toast.success(successMsg)
      return res.data
    } catch (e: any) {
      const msg = e?.response?.data?.detail || 'Xato yuz berdi'
      toast.error(msg)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function update(apiFn: () => Promise<{ data: T }>, successMsg = 'Muvaffaqiyatli yangilandi') {
    loading.value = true
    try {
      const res = await apiFn()
      toast.success(successMsg)
      return res.data
    } catch (e: any) {
      const msg = e?.response?.data?.detail || 'Xato yuz berdi'
      toast.error(msg)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function remove(apiFn: () => Promise<any>, successMsg = "O'chirildi") {
    loading.value = true
    try {
      await apiFn()
      toast.success(successMsg)
    } catch (e: any) {
      const msg = e?.response?.data?.detail || 'Xato yuz berdi'
      toast.error(msg)
      throw e
    } finally {
      loading.value = false
    }
  }

  return { data, list, loading, error, fetch, fetchOne, create, update, remove }
}
