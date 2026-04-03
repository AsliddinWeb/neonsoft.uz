<script setup lang="ts">
import { onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useThemeStore } from '@/stores/theme'

const settingsStore = useSettingsStore()
const themeStore = useThemeStore()

onMounted(() => {
  settingsStore.fetch()
  // Initialize dark mode
  themeStore.isDark
})
</script>

<template>
  <RouterView />
</template>
