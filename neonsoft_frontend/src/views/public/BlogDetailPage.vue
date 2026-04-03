<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { Calendar, Eye, ArrowLeft, Tag } from 'lucide-vue-next'
import { blogApi } from '@/api/blog'
import { mediaUrl } from '@/utils/media'
import { useSeo } from '@/composables/useSeo'
import AppLoader from '@/components/ui/AppLoader.vue'
import type { BlogPost } from '@/types'

const route = useRoute()
const post = ref<BlogPost | null>(null)
const related = ref<BlogPost[]>([])
const loading = ref(true)

function formatDate(d: string | null) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { year: 'numeric', month: 'long', day: 'numeric' })
}

async function load(slug: string) {
  loading.value = true
  post.value = null
  try {
    const [{ data: p }, { data: rel }] = await Promise.all([
      blogApi.get(slug),
      blogApi.list({ limit: 3 }),
    ])
    post.value = p
    related.value = rel.filter((r) => r.slug !== slug).slice(0, 3)
    useSeo({ title: p.title, description: p.excerpt || undefined, image: mediaUrl(p.cover_image_url) })
  } finally {
    loading.value = false
  }
}

watch(() => route.params.slug as string, load)
onMounted(() => load(route.params.slug as string))
</script>

<template>
  <div class="pt-24 pb-16">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
      <RouterLink to="/blog" class="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-500 transition-colors mb-8">
        <ArrowLeft class="w-4 h-4" /> Blogga qaytish
      </RouterLink>

      <AppLoader v-if="loading" :rows="8" />

      <article v-else-if="post">
        <!-- Cover -->
        <div v-if="post.cover_image_url" class="rounded-2xl overflow-hidden h-64 md:h-96 mb-8">
          <img :src="mediaUrl(post.cover_image_url)" :alt="post.title" class="w-full h-full object-cover" />
        </div>

        <!-- Tags -->
        <div v-if="post.tags?.length" class="flex flex-wrap gap-2 mb-5">
          <span v-for="tag in post.tags" :key="tag"
            class="flex items-center gap-1 px-3 py-1 text-sm bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-full">
            <Tag class="w-3 h-3" />{{ tag }}
          </span>
        </div>

        <!-- Title -->
        <h1 class="font-display font-bold text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
          {{ post.title }}
        </h1>

        <!-- Meta -->
        <div class="flex items-center gap-5 text-sm text-gray-400 mb-8 pb-8 border-b border-gray-100 dark:border-gray-800">
          <span class="font-medium text-gray-700 dark:text-gray-300">{{ post.author.full_name }}</span>
          <span class="flex items-center gap-1.5"><Calendar class="w-4 h-4" />{{ formatDate(post.published_at) }}</span>
          <span class="flex items-center gap-1.5"><Eye class="w-4 h-4" />{{ post.views }} ko'rishlar</span>
        </div>

        <!-- Content -->
        <div class="prose prose-lg dark:prose-invert max-w-none prose-headings:font-display prose-a:text-primary-500"
          v-html="post.content" />
      </article>

      <!-- Related -->
      <div v-if="related.length" class="mt-16 pt-12 border-t border-gray-100 dark:border-gray-800">
        <h2 class="font-display font-bold text-2xl text-gray-900 dark:text-white mb-8">Boshqa maqolalar</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <RouterLink v-for="r in related" :key="r.id" :to="`/blog/${r.slug}`"
            class="group rounded-xl overflow-hidden border border-gray-100 dark:border-gray-800 hover:border-primary-500 transition-colors">
            <div class="h-36 bg-gray-100 dark:bg-gray-800 overflow-hidden">
              <img v-if="r.cover_image_url" :src="mediaUrl(r.cover_image_url)" :alt="r.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform" />
            </div>
            <div class="p-4">
              <h3 class="font-semibold text-sm text-gray-900 dark:text-white group-hover:text-primary-500 transition-colors line-clamp-2">{{ r.title }}</h3>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
