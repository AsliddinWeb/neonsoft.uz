<template>
  <section v-if="partners.length" class="py-16 bg-gray-50 dark:bg-gray-900/50">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-10">
        <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest mb-2 mx-auto">
          <span class="w-8 h-px bg-primary-500" /> Hamkorlar <span class="w-8 h-px bg-primary-500" />
        </span>
        <h2 class="text-2xl md:text-3xl font-display font-bold text-gray-900 dark:text-white">
          Biz bilan ishlaganlar qayta murojaat qiladi
        </h2>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-6 md:gap-10">
        <a
          v-for="p in partners"
          :key="p.id"
          :href="p.website_url || '#'"
          :target="p.website_url ? '_blank' : '_self'"
          rel="noopener noreferrer"
          class="group flex items-center justify-center h-16 px-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:shadow-md transition-all duration-300 grayscale hover:grayscale-0"
        >
          <img
            v-if="p.logo_url"
            :src="mediaUrl(p.logo_url)"
            :alt="p.name"
            class="h-8 max-w-[120px] object-contain"
          />
          <span v-else class="text-sm font-semibold text-gray-500 dark:text-gray-400 group-hover:text-primary-500 transition-colors">
            {{ p.name }}
          </span>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { partnersApi, type Partner } from '@/api/partners'
import { mediaUrl } from '@/utils/media'

const partners = ref<Partner[]>([])

onMounted(async () => {
  try { partners.value = await partnersApi.list() }
  catch {}
})
</script>