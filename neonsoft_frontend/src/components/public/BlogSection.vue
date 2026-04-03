<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight, Calendar, Eye } from 'lucide-vue-next'
import { blogApi } from '@/api/blog'
import { mediaUrl } from '@/utils/media'
import type { BlogPost } from '@/types'

const posts = ref<BlogPost[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await blogApi.list({ limit: 3 })
    posts.value = data
  } finally {
    loading.value = false
  }
})

function formatDate(d: string | null) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<template>
  <section class="py-24 bg-gray-50 dark:bg-surface">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-14">
        <div>
          <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest mb-3">
            <span class="w-8 h-px bg-primary-500" /> Blog
          </span>
          <h2 class="section-title">Foydali bilimlar va yangiliklar</h2>
        </div>
        <RouterLink to="/blog" class="btn-outline shrink-0 inline-flex self-start md:self-auto">
          Barchasi <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800">
          <div class="skeleton h-44" />
          <div class="p-5 space-y-2">
            <div class="skeleton h-5 w-3/4" />
            <div class="skeleton h-4 w-full" />
          </div>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <RouterLink
          v-for="post in posts"
          :key="post.id"
          :to="`/blog/${post.slug}`"
          class="group rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface hover:shadow-lg hover:shadow-primary-500/10 transition-all duration-300 hover:-translate-y-1 flex flex-col"
        >
          <div class="h-44 overflow-hidden bg-gray-100 dark:bg-gray-800">
            <img
              v-if="post.cover_image_url"
              :src="mediaUrl(post.cover_image_url)"
              :alt="post.title"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-300">📝</div>
          </div>
          <div class="p-5 flex flex-col flex-1">
            <div v-if="post.tags?.length" class="flex flex-wrap gap-1.5 mb-3">
              <span v-for="tag in post.tags.slice(0,2)" :key="tag"
                class="px-2 py-0.5 text-xs bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded">
                {{ tag }}
              </span>
            </div>
            <h3 class="font-display font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors line-clamp-2">
              {{ post.title }}
            </h3>
            <p v-if="post.excerpt" class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 flex-1">
              {{ post.excerpt }}
            </p>
            <div class="flex items-center gap-4 mt-4 text-xs text-gray-400">
              <span class="flex items-center gap-1"><Calendar class="w-3 h-3" /> {{ formatDate(post.published_at) }}</span>
              <span class="flex items-center gap-1"><Eye class="w-3 h-3" /> {{ post.views }}</span>
            </div>
          </div>
        </RouterLink>
      </div>

      <!-- removed duplicate button -->
    </div>
  </section>
</template>
