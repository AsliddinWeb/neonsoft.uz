<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Send, Linkedin, Github } from 'lucide-vue-next'
import { teamApi } from '@/api/team'
import { mediaUrl } from '@/utils/media'
import type { TeamMember } from '@/types'

const members = ref<TeamMember[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await teamApi.list()
    members.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="py-24 bg-white dark:bg-secondary">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest mb-3 mx-auto">
          <span class="w-8 h-px bg-primary-500" /> Jamoa <span class="w-8 h-px bg-primary-500" />
        </span>
        <h2 class="section-title">Natija ortidagi odamlar</h2>
        <p class="text-gray-500 dark:text-gray-400 mt-4 max-w-xl mx-auto">
          Professional dasturchilar, dizaynerlar va menejerlar — birgalikda kuchli jamoamiz
        </p>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i" class="rounded-2xl border border-gray-100 dark:border-gray-800 p-6 space-y-3">
          <div class="skeleton w-20 h-20 rounded-2xl mx-auto" />
          <div class="skeleton h-4 w-3/4 mx-auto" />
          <div class="skeleton h-3 w-1/2 mx-auto" />
        </div>
      </div>

      <!-- Cards -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="member in members"
          :key="member.id"
          class="group relative bg-white dark:bg-surface rounded-2xl border border-gray-100 dark:border-gray-800 p-6 text-center hover:shadow-xl hover:shadow-primary-500/10 hover:-translate-y-1 hover:border-primary-500/30 transition-all duration-300 overflow-hidden"
        >
          <!-- Glow -->
          <div class="absolute inset-0 bg-gradient-to-b from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />

          <!-- Photo -->
          <div class="relative w-20 h-20 mx-auto mb-4">
            <img
              v-if="member.photo_url"
              :src="mediaUrl(member.photo_url)"
              :alt="member.full_name"
              class="w-20 h-20 rounded-2xl object-cover ring-2 ring-transparent group-hover:ring-primary-500 transition-all duration-300"
            />
            <div v-else class="w-20 h-20 rounded-2xl bg-primary-500/10 flex items-center justify-center text-2xl font-bold text-primary-500 ring-2 ring-transparent group-hover:ring-primary-500 transition-all duration-300">
              {{ member.full_name?.[0]?.toUpperCase() }}
            </div>
            <!-- Online dot -->
            <div class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-green-400 border-2 border-white dark:border-surface" />
          </div>

          <!-- Info -->
          <h3 class="relative font-display font-semibold text-gray-900 dark:text-white group-hover:text-primary-500 transition-colors">
            {{ member.full_name }}
          </h3>
          <p class="relative text-sm text-primary-500 font-medium mt-0.5">{{ member.position }}</p>
          <p v-if="member.bio" class="relative text-xs text-gray-400 dark:text-gray-500 mt-2 line-clamp-2">
            {{ member.bio }}
          </p>

          <!-- Social -->
          <div class="relative flex justify-center gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
            <a v-if="member.telegram_url" :href="member.telegram_url" target="_blank"
              class="p-2 rounded-xl bg-gray-50 dark:bg-gray-800 hover:bg-primary-500/10 hover:text-primary-500 text-gray-400 transition-colors">
              <Send class="w-3.5 h-3.5" />
            </a>
            <a v-if="member.linkedin_url" :href="member.linkedin_url" target="_blank"
              class="p-2 rounded-xl bg-gray-50 dark:bg-gray-800 hover:bg-primary-500/10 hover:text-primary-500 text-gray-400 transition-colors">
              <Linkedin class="w-3.5 h-3.5" />
            </a>
            <a v-if="member.github_url" :href="member.github_url" target="_blank"
              class="p-2 rounded-xl bg-gray-50 dark:bg-gray-800 hover:bg-primary-500/10 hover:text-primary-500 text-gray-400 transition-colors">
              <Github class="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
