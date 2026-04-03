<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { ExternalLink, Github } from 'lucide-vue-next'
import { projectsApi } from '@/api/projects'
import { mediaUrl } from '@/utils/media'
import { useSeo } from '@/composables/useSeo'
import PageHeader from '@/components/public/PageHeader.vue'
import AppLoader from '@/components/ui/AppLoader.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import type { Project } from '@/types'

useSeo({ title: 'Loyihalar' })

const projects = ref<Project[]>([])
const loading = ref(true)
const page = ref(1)
const limit = 9
const total = ref(0)
const featured = ref<boolean | undefined>(undefined)

async function load() {
  loading.value = true
  try {
    const { data } = await projectsApi.list({ page: page.value, limit, featured: featured.value })
    projects.value = data
    total.value = data.length === limit ? page.value * limit + 1 : (page.value - 1) * limit + data.length
  } finally {
    loading.value = false
  }
}

watch(page, load)
watch(featured, () => { page.value = 1; load() })
onMounted(load)
</script>

<template>
  <div>
    <PageHeader label="Loyihalar" title="Ishimiz o'zi gapiradi" />
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="flex justify-end mb-8">
        <div class="flex gap-2">
          <button @click="featured = undefined" :class="['px-4 py-2 rounded-xl text-sm font-medium transition-colors', featured === undefined ? 'bg-primary-500 text-secondary' : 'border border-gray-200 dark:border-gray-700 hover:border-primary-500']">Hammasi</button>
          <button @click="featured = true" :class="['px-4 py-2 rounded-xl text-sm font-medium transition-colors', featured === true ? 'bg-primary-500 text-secondary' : 'border border-gray-200 dark:border-gray-700 hover:border-primary-500']">Tanlangan</button>
        </div>
      </div>

      <AppLoader v-if="loading" :rows="3" :cols="3" />

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="project in projects" :key="project.id"
          class="group rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface hover:shadow-xl hover:shadow-primary-500/10 transition-all duration-300 hover:-translate-y-1">
          <div class="relative h-52 overflow-hidden bg-gray-100 dark:bg-gray-800">
            <img v-if="project.image_url" :src="mediaUrl(project.image_url)" :alt="project.title"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
            <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-300">🚀</div>
            <div class="absolute inset-0 bg-secondary/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4">
              <a v-if="project.project_url" :href="project.project_url" target="_blank"
                class="p-3 rounded-xl bg-white/10 hover:bg-primary-500 transition-colors">
                <ExternalLink class="w-5 h-5 text-white" />
              </a>
              <a v-if="project.github_url" :href="project.github_url" target="_blank"
                class="p-3 rounded-xl bg-white/10 hover:bg-primary-500 transition-colors">
                <Github class="w-5 h-5 text-white" />
              </a>
            </div>
          </div>
          <div class="p-5">
            <h3 class="font-display font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors">{{ project.title }}</h3>
            <p v-if="project.client_name" class="text-xs text-gray-400 mb-3">{{ project.client_name }}</p>
            <div v-if="project.tech_stack?.length" class="flex flex-wrap gap-1.5">
              <span v-for="tech in project.tech_stack" :key="tech"
                class="px-2 py-0.5 text-xs font-mono bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded">{{ tech }}</span>
            </div>
          </div>
        </div>
      </div>

      <AppPagination :page="page" :limit="limit" :total="total" @update:page="page = $event" />
    </div>
  </div>
</template>
