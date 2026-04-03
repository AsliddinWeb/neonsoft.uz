<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  icon: string
  color?: 'primary' | 'accent' | 'blue' | 'purple'
}>()
</script>

<template>
  <div class="card flex items-center gap-5">
    <div :class="[
      'w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shrink-0',
      {
        'bg-primary-500/10': !color || color === 'primary',
        'bg-accent/10': color === 'accent',
        'bg-blue-500/10': color === 'blue',
        'bg-purple-500/10': color === 'purple',
      }
    ]">
      {{ icon }}
    </div>
    <div>
      <p class="text-sm text-gray-500 dark:text-gray-400">{{ title }}</p>
      <p class="font-display font-bold text-2xl text-gray-900 dark:text-white">{{ value }}</p>
    </div>
  </div>
</template>
