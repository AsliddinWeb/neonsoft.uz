<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}>()
</script>

<template>
  <button
    :type="type || 'button'"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
      {
        'px-3 py-1.5 text-sm': size === 'sm',
        'px-5 py-2.5 text-sm': !size || size === 'md',
        'px-7 py-3.5 text-base': size === 'lg',
        'bg-primary-500 text-secondary hover:bg-primary-400 hover:scale-105 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2': !variant || variant === 'primary',
        'border-2 border-primary-500 text-primary-500 hover:bg-primary-500 hover:text-secondary': variant === 'outline',
        'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800': variant === 'ghost',
        'bg-red-500 text-white hover:bg-red-600': variant === 'danger',
      },
    ]"
  >
    <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <slot />
  </button>
</template>
