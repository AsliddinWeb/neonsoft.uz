<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { servicesApi } from '@/api/services'
import { projectsApi } from '@/api/projects'
import { teamApi } from '@/api/team'
import { contactApi } from '@/api/contact'
import { blogApi } from '@/api/blog'
import StatsCard from '@/components/admin/StatsCard.vue'
import type { ContactMessage, BlogPost } from '@/types'

const stats = ref({ services: 0, projects: 0, team: 0, unread: 0 })
const recentContacts = ref<ContactMessage[]>([])
const recentPosts = ref<BlogPost[]>([])
const loading = ref(true)

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('uz-UZ', { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(async () => {
  try {
    const [svc, prj, tm, cnt, blg] = await Promise.all([
      servicesApi.adminList(),
      projectsApi.adminList(),
      teamApi.adminList(),
      contactApi.adminList({ limit: 5 }),
      blogApi.adminList({ limit: 5 }),
    ])
    stats.value.services = svc.data.length
    stats.value.projects = prj.data.length
    stats.value.team = tm.data.length
    stats.value.unread = cnt.data.filter((c) => !c.is_read).length
    recentContacts.value = cnt.data.slice(0, 5)
    recentPosts.value = blg.data.slice(0, 5)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="space-y-6">
    <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Dashboard</h1>

    <!-- Stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatsCard title="Xizmatlar" :value="stats.services" icon="⚡" color="primary" />
      <StatsCard title="Loyihalar" :value="stats.projects" icon="🚀" color="accent" />
      <StatsCard title="Jamoa" :value="stats.team" icon="👥" color="blue" />
      <StatsCard title="O'qilmagan" :value="stats.unread" icon="✉️" color="purple" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent contacts -->
      <div class="card">
        <div class="flex items-center justify-between mb-5">
          <h2 class="font-display font-semibold text-gray-900 dark:text-white">So'nggi xabarlar</h2>
          <RouterLink to="/admin/contacts" class="text-sm text-primary-500 hover:underline">Barchasi</RouterLink>
        </div>
        <div class="space-y-3">
          <div v-for="c in recentContacts" :key="c.id"
            class="flex items-start gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
            <div :class="['w-2 h-2 rounded-full mt-2 shrink-0', c.is_read ? 'bg-gray-300' : 'bg-primary-500']" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ c.full_name }}</p>
              <p class="text-xs text-gray-400 truncate">{{ c.subject || c.message }}</p>
            </div>
            <span class="text-xs text-gray-400 shrink-0">{{ formatDate(c.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Recent blog -->
      <div class="card">
        <div class="flex items-center justify-between mb-5">
          <h2 class="font-display font-semibold text-gray-900 dark:text-white">So'nggi maqolalar</h2>
          <RouterLink to="/admin/blog" class="text-sm text-primary-500 hover:underline">Barchasi</RouterLink>
        </div>
        <div class="space-y-3">
          <div v-for="post in recentPosts" :key="post.id"
            class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
            <div :class="['w-2 h-2 rounded-full shrink-0', post.is_published ? 'bg-green-500' : 'bg-yellow-500']" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ post.title }}</p>
              <p class="text-xs text-gray-400">{{ post.views }} ko'rishlar</p>
            </div>
            <span class="text-xs text-gray-400 shrink-0">{{ formatDate(post.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
