<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { Calendar, Eye, Tag } from 'lucide-vue-next'
import { blogApi } from '@/api/blog'
import { mediaUrl } from '@/utils/media'
import { useSeo } from '@/composables/useSeo'
import PageHeader from '@/components/public/PageHeader.vue'
import AppLoader from '@/components/ui/AppLoader.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import type { BlogPost } from '@/types'

useSeo({ title: 'Blog' })

const posts = ref<BlogPost[]>([])
const loading = ref(true)
const page = ref(1)
const limit = 9
const total = ref(0)
const activeTag = ref('')

function formatDate(d: string | null) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { year: 'numeric', month: 'long', day: 'numeric' })
}

async function load() {
  loading.value = true
  try {
    const { data } = await blogApi.list({ page: page.value, limit, tag: activeTag.value || undefined })
    posts.value = data
    total.value = data.length === limit ? page.value * limit + 1 : (page.value - 1) * limit + data.length
  } finally {
    loading.value = false
  }
}

watch(page, load)
watch(activeTag, () => { page.value = 1; load() })
onMounted(load)
</script>

<template>
  <div>
    <PageHeader label="Blog" title="Foydali bilimlar va yangiliklar" />
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-16">

      <!-- Tag filter -->
      <div v-if="posts.length" class="flex flex-wrap gap-2 mb-8 justify-center">
        <button @click="activeTag = ''"
          :class="['flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm transition-colors', !activeTag ? 'bg-primary-500 text-secondary' : 'border border-gray-200 dark:border-gray-700 hover:border-primary-500']">
          <Tag class="w-3.5 h-3.5" /> Hammasi
        </button>
      </div>

      <AppLoader v-if="loading" :rows="3" :cols="3" />

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RouterLink v-for="post in posts" :key="post.id" :to="`/blog/${post.slug}`"
          class="group rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface hover:shadow-lg hover:shadow-primary-500/10 transition-all duration-300 hover:-translate-y-1 flex flex-col">
          <div class="h-48 overflow-hidden bg-gray-100 dark:bg-gray-800">
            <img v-if="post.cover_image_url" :src="mediaUrl(post.cover_image_url)" :alt="post.title"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
            <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-300">📝</div>
          </div>
          <div class="p-5 flex flex-col flex-1">
            <div v-if="post.tags?.length" class="flex flex-wrap gap-1.5 mb-3">
              <button v-for="tag in post.tags.slice(0,3)" :key="tag" @click.prevent="activeTag = tag"
                class="px-2 py-0.5 text-xs bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded hover:bg-primary-500 hover:text-secondary transition-colors">{{ tag }}</button>
            </div>
            <h2 class="font-display font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors line-clamp-2">{{ post.title }}</h2>
            <p v-if="post.excerpt" class="text-sm text-gray-500 dark:text-gray-400 line-clamp-3 flex-1">{{ post.excerpt }}</p>
            <div class="flex items-center gap-4 mt-4 text-xs text-gray-400">
              <span class="flex items-center gap-1"><Calendar class="w-3 h-3" /> {{ formatDate(post.published_at) }}</span>
              <span class="flex items-center gap-1"><Eye class="w-3 h-3" /> {{ post.views }}</span>
            </div>
          </div>
        </RouterLink>
      </div>

      <AppPagination :page="page" :limit="limit" :total="total" @update:page="page = $event" />
    </div>
  </div>
</template>
