<script setup lang="ts">
defineProps<{ rows?: number; cols?: number }>()
</script>

<template>
  <div class="space-y-4 animate-pulse">
    <div v-for="r in (rows || 3)" :key="r" class="flex gap-4">
      <div v-for="c in (cols || 1)" :key="c" class="flex-1 space-y-2">
        <div class="skeleton h-4 w-3/4" />
        <div class="skeleton h-3 w-full" />
        <div class="skeleton h-3 w-5/6" />
      </div>
    </div>
  </div>
</template>
