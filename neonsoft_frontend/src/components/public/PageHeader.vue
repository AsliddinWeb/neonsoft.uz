<script setup lang="ts">
defineProps<{
  label: string
  title: string
  description?: string
}>()
</script>

<template>
  <div class="bg-gray-50 dark:bg-surface border-b border-gray-100 dark:border-gray-800">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-12 text-center">
      <span class="text-primary-500 text-xs font-semibold uppercase tracking-[0.2em]">
        {{ label }}
      </span>
      <h1 class="font-display font-bold text-3xl md:text-4xl text-gray-900 dark:text-white mt-3">
        {{ title }}
      </h1>
      <p v-if="description" class="text-gray-500 dark:text-gray-400 mt-3 max-w-lg mx-auto">
        {{ description }}
      </p>
    </div>
  </div>
</template>
