<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps<{ open?: boolean; title?: string; size?: 'sm' | 'md' | 'lg' | 'xl' }>()
const emit = defineEmits<{ close: [] }>()

function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}
onMounted(() => document.addEventListener('keydown', onKey))
onUnmounted(() => {
  document.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <div v-if="open !== false" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Overlay -->
      <div
        class="absolute inset-0 bg-black/60 backdrop-blur-sm"
        @click="emit('close')"
      />
      <!-- Modal -->
      <div
        :class="[
          'relative z-10 w-full bg-white dark:bg-surface rounded-2xl shadow-2xl flex flex-col max-h-[90vh]',
          { 'max-w-sm': size === 'sm', 'max-w-lg': !size || size === 'md', 'max-w-2xl': size === 'lg', 'max-w-4xl': size === 'xl' },
        ]"
      >
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100 dark:border-gray-800">
          <h3 class="text-lg font-semibold font-display text-gray-900 dark:text-white">
            {{ title }}
          </h3>
          <button
            @click="emit('close')"
            class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>
        <!-- Body -->
        <div class="overflow-y-auto flex-1 p-6">
          <slot />
        </div>
        <!-- Footer -->
        <div v-if="$slots.footer" class="p-6 border-t border-gray-100 dark:border-gray-800">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>
