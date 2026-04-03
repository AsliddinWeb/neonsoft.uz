<script setup lang="ts">
import { Menu, LogOut, Globe } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThemeToggle from '@/components/public/ThemeToggle.vue'

defineEmits<{ toggleSidebar: [] }>()

const router = useRouter()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push('/admin/login')
}
</script>

<template>
  <header class="h-16 bg-white dark:bg-surface border-b border-gray-100 dark:border-gray-800 flex items-center justify-between px-4 lg:px-6 sticky top-0 z-20">
    <button
      @click="$emit('toggleSidebar')"
      class="lg:hidden p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
    >
      <Menu class="w-5 h-5" />
    </button>

    <div class="flex-1 lg:flex-none">
      <span class="text-sm text-gray-500 dark:text-gray-400 font-medium hidden lg:block">Admin Panel</span>
    </div>

    <div class="flex items-center gap-2">
      <ThemeToggle />
      <a href="/" target="_blank"
        class="p-2 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:text-primary-500 transition-all duration-200"
        title="Saytni ko'rish">
        <Globe class="w-5 h-5" />
      </a>
      <button
        @click="logout"
        class="flex items-center gap-2 px-3 py-2 rounded-xl text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
      >
        <LogOut class="w-4 h-4" />
        <span class="hidden sm:inline">Chiqish</span>
      </button>
    </div>
  </header>
</template>
