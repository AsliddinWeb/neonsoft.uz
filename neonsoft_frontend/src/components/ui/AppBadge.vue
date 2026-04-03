<script setup lang="ts">
defineProps<{ variant?: 'primary' | 'success' | 'warning' | 'danger' | 'gray' }>()
</script>

<template>
  <span
    :class="[
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      {
        'bg-primary-100 text-primary-800 dark:bg-primary-900/30 dark:text-primary-400': !variant || variant === 'primary',
        'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400': variant === 'success',
        'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400': variant === 'warning',
        'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400': variant === 'danger',
        'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300': variant === 'gray',
      },
    ]"
  >
    <slot />
  </span>
</template>
