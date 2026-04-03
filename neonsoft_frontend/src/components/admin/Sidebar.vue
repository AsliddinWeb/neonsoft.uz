<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import {
  LayoutDashboard, Layers, FolderOpen, Users2, BookOpen,
  MessageSquare, Settings, Users, X, ChevronRight, Info, Handshake,
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useSettingsStore } from '@/stores/settings'

defineProps<{ open: boolean }>()
defineEmits<{ close: [] }>()

const route = useRoute()
const auth = useAuthStore()
const settings = useSettingsStore()

const links = [
  { to: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/admin/services', label: 'Xizmatlar', icon: Layers },
  { to: '/admin/projects', label: 'Loyihalar', icon: FolderOpen },
  { to: '/admin/team', label: 'Jamoa', icon: Users2 },
  { to: '/admin/blog', label: 'Blog', icon: BookOpen },
  { to: '/admin/contacts', label: 'Xabarlar', icon: MessageSquare },
  { to: '/admin/about', label: 'Biz haqimizda', icon: Info },
  { to: '/admin/partners', label: 'Hamkorlar', icon: Handshake },
  { to: '/admin/settings', label: 'Sozlamalar', icon: Settings },
]

const isActive = (to: string) => route.path === to || route.path.startsWith(to + '/')
</script>

<template>
  <!-- Mobile overlay -->
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 bg-black/50 z-30 lg:hidden" @click="$emit('close')" />
  </Teleport>

  <aside :class="[
    'fixed top-0 left-0 h-full w-64 bg-white dark:bg-surface border-r border-gray-100 dark:border-gray-800 z-40 flex flex-col transition-transform duration-300',
    open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
  ]">
    <!-- Logo -->
    <div class="flex items-center justify-between p-5 border-b border-gray-100 dark:border-gray-800">
      <RouterLink to="/admin/dashboard" class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-primary-500 flex items-center justify-center">
          <span class="text-secondary font-bold text-sm font-display">N</span>
        </div>
        <span class="font-display font-bold text-gray-900 dark:text-white">
          {{ settings.settings?.company_name || 'NeonSoft' }}
        </span>
      </RouterLink>
      <button @click="$emit('close')" class="lg:hidden p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-800">
        <X class="w-4 h-4" />
      </button>
    </div>

    <!-- Nav -->
    <nav class="flex-1 overflow-y-auto p-3 space-y-0.5">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        @click="$emit('close')"
        :class="[
          'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all group',
          isActive(link.to)
            ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white',
        ]"
      >
        <component :is="link.icon" class="w-4.5 h-4.5 shrink-0" />
        {{ link.label }}
        <ChevronRight v-if="isActive(link.to)" class="w-4 h-4 ml-auto" />
      </RouterLink>

      <!-- Superadmin only -->
      <RouterLink
        v-if="auth.isSuperadmin"
        to="/admin/users"
        @click="$emit('close')"
        :class="[
          'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all',
          isActive('/admin/users')
            ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white',
        ]"
      >
        <Users class="w-4.5 h-4.5 shrink-0" />
        Foydalanuvchilar
        <ChevronRight v-if="isActive('/admin/users')" class="w-4 h-4 ml-auto" />
      </RouterLink>
    </nav>

    <!-- User info -->
    <div class="p-4 border-t border-gray-100 dark:border-gray-800">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full bg-primary-500/10 flex items-center justify-center text-primary-500 font-bold text-sm">
          {{ auth.user?.full_name?.[0]?.toUpperCase() || 'A' }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ auth.user?.full_name }}</p>
          <p class="text-xs text-gray-400 truncate">{{ auth.user?.role }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>
