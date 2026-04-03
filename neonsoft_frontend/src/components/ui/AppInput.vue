<script setup lang="ts">
defineProps<{
  label?: string
  error?: string
  type?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  modelValue?: string | number | null
}>()

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <label v-if="label" class="text-sm font-medium text-gray-700 dark:text-gray-300">
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      :type="type || 'text'"
      :value="modelValue ?? ''"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :class="[
        'w-full px-4 py-2.5 rounded-xl border bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500',
        error
          ? 'border-red-500 focus:ring-red-500'
          : 'border-gray-300 dark:border-gray-700',
        disabled && 'opacity-50 cursor-not-allowed',
      ]"
    />
    <p v-if="error" class="text-xs text-red-500">{{ error }}</p>
  </div>
</template>
