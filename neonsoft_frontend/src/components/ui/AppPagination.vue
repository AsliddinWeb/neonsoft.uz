<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps<{ page: number; limit: number; total: number }>()
const emit = defineEmits<{ 'update:page': [page: number] }>()

const totalPages = () => Math.ceil(props.total / props.limit)
const pages = () => {
  const t = totalPages()
  const p = props.page
  const range: number[] = []
  for (let i = Math.max(1, p - 2); i <= Math.min(t, p + 2); i++) range.push(i)
  return range
}
</script>

<template>
  <div v-if="total > limit" class="flex items-center justify-center gap-2 mt-6">
    <button
      :disabled="page === 1"
      @click="emit('update:page', page - 1)"
      class="p-2 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 disabled:opacity-40 transition-colors"
    >
      <ChevronLeft class="w-4 h-4" />
    </button>
    <button
      v-for="p in pages()"
      :key="p"
      @click="emit('update:page', p)"
      :class="[
        'w-9 h-9 rounded-lg text-sm font-medium transition-colors',
        p === page
          ? 'bg-primary-500 text-secondary'
          : 'border border-gray-200 dark:border-gray-700 hover:border-primary-500',
      ]"
    >
      {{ p }}
    </button>
    <button
      :disabled="page === totalPages()"
      @click="emit('update:page', page + 1)"
      class="p-2 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 disabled:opacity-40 transition-colors"
    >
      <ChevronRight class="w-4 h-4" />
    </button>
  </div>
</template>
