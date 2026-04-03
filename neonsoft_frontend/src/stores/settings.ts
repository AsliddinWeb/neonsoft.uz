import { defineStore } from 'pinia'
import { ref } from 'vue'
import { settingsApi } from '@/api/settings'
import type { SiteSetting } from '@/types'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<SiteSetting | null>(null)
  const loading = ref(false)

  async function fetch() {
    if (settings.value) return
    loading.value = true
    try {
      const { data } = await settingsApi.get()
      settings.value = data
    } finally {
      loading.value = false
    }
  }

  return { settings, loading, fetch }
})
