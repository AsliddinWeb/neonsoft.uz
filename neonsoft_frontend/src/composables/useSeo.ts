import { useHead } from '@vueuse/head'
import { useSettingsStore } from '@/stores/settings'

interface SeoOptions {
  title?: string
  description?: string
  image?: string
  keywords?: string
}

export function useSeo(options: SeoOptions = {}) {
  const store = useSettingsStore()
  const appName = import.meta.env.VITE_APP_NAME || 'NeonSoft'

  const siteTitle = store.settings?.meta_title || appName
  const siteDesc = store.settings?.meta_description || ''

  const title = options.title ? `${options.title} | ${appName}` : siteTitle
  const description = options.description || siteDesc
  const image = options.image || ''

  useHead({
    title,
    meta: [
      { name: 'description', content: description },
      { name: 'keywords', content: options.keywords || store.settings?.meta_keywords || '' },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: image },
      { property: 'og:type', content: 'website' },
    ],
  })
}
