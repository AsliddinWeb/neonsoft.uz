export function mediaUrl(path: string | null | undefined): string {
  if (!path) return ''
  if (path.startsWith('http')) return path
  const base = import.meta.env.VITE_MEDIA_BASE_URL || ''
  return `${base}${path.startsWith('/') ? path : '/' + path}`
}
