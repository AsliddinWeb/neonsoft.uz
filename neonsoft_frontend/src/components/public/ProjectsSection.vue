<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ArrowRight, ExternalLink, Github } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'
import { projectsApi } from '@/api/projects'
import { mediaUrl } from '@/utils/media'
import type { Project } from '@/types'

const projects = ref<Project[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await projectsApi.list({ featured: true, limit: 4 })
    projects.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="py-24 bg-gray-50 dark:bg-surface">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-14">
        <div>
          <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest mb-3">
            <span class="w-8 h-px bg-primary-500" /> Portfolio
          </span>
          <h2 class="section-title">Ishimiz o'zi gapiradi</h2>
        </div>
        <RouterLink to="/projects" class="btn-outline shrink-0 inline-flex self-start md:self-auto">
          Barchasi <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 4" :key="i" class="rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800">
          <div class="skeleton h-56" />
          <div class="p-5 space-y-2">
            <div class="skeleton h-5 w-3/4" />
            <div class="skeleton h-4 w-full" />
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="(project, i) in projects"
          :key="project.id"
          :class="[
            'group relative rounded-3xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface shadow-sm hover:shadow-2xl hover:shadow-primary-500/10 transition-all duration-500',
            i === 0 ? 'md:row-span-2' : '',
          ]"
        >
          <!-- Image -->
          <div :class="['relative overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900', i === 0 ? 'h-72 md:h-[420px]' : 'h-52']">
            <img
              v-if="project.image_url"
              :src="mediaUrl(project.image_url)"
              :alt="project.title"
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <div class="w-16 h-16 rounded-2xl bg-primary-500/10 flex items-center justify-center">
                <ExternalLink class="w-8 h-8 text-primary-500/40" />
              </div>
            </div>

            <!-- Overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-secondary/90 via-secondary/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-400 flex flex-col justify-end p-6">
              <div class="flex gap-3 mb-4">
                <a v-if="project.project_url" :href="project.project_url" target="_blank"
                  @click.stop
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary-500 text-secondary text-sm font-medium hover:bg-primary-400 transition-colors">
                  <ExternalLink class="w-4 h-4" /> Ko'rish
                </a>
                <a v-if="project.github_url" :href="project.github_url" target="_blank"
                  @click.stop
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/10 text-white text-sm font-medium hover:bg-white/20 transition-colors">
                  <Github class="w-4 h-4" /> GitHub
                </a>
              </div>
            </div>

            <!-- Client badge -->
            <div v-if="project.client_name" class="absolute top-4 left-4 px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm text-white text-xs font-medium">
              {{ project.client_name }}
            </div>
          </div>

          <!-- Content -->
          <div class="p-5">
            <h3 class="font-display font-semibold text-gray-900 dark:text-white group-hover:text-primary-500 transition-colors mb-2">
              {{ project.title }}
            </h3>
            <div v-if="project.tech_stack?.length" class="flex flex-wrap gap-1.5">
              <span
                v-for="tech in project.tech_stack.slice(0, 4)"
                :key="tech"
                class="px-2 py-0.5 text-xs font-mono bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-md"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
