<script setup lang="ts">
defineProps<{
  columns: { key: string; label: string; class?: string }[]
  loading?: boolean
  empty?: string
}>()
</script>

<template>
  <div class="overflow-x-auto rounded-xl border border-gray-100 dark:border-gray-800">
    <table class="w-full text-sm">
      <thead class="bg-gray-50 dark:bg-gray-800/50">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :class="['px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider', col.class]"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-surface">
        <!-- Skeleton loader -->
        <template v-if="loading">
          <tr v-for="i in 5" :key="i">
            <td v-for="col in columns" :key="col.key" class="px-4 py-3">
              <div class="skeleton h-4 w-full" />
            </td>
          </tr>
        </template>
        <!-- Empty state -->
        <tr v-else-if="!$slots.default">
          <td :colspan="columns.length" class="px-4 py-12 text-center text-gray-400">
            {{ empty || "Ma'lumot topilmadi" }}
          </td>
        </tr>
        <!-- Data rows -->
        <slot v-else />
      </tbody>
    </table>
  </div>
</template>
