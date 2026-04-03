<script setup lang="ts">
import { Sun, Moon } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
const theme = useThemeStore()
defineProps<{ transparent?: boolean }>()
</script>

<template>
  <button
    @click="theme.toggleDark()"
    :class="[
      'p-2 rounded-xl transition-all duration-200',
      transparent
        ? 'border border-white/30 text-white hover:border-white hover:bg-white/10'
        : 'border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:text-primary-500',
    ]"
    :title="theme.isDark ? 'Light mode' : 'Dark mode'"
  >
    <Sun v-if="theme.isDark" class="w-5 h-5" />
    <Moon v-else class="w-5 h-5" />
  </button>
</template>
