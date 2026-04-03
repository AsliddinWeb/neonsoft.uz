<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Send, Linkedin, Github } from 'lucide-vue-next'
import { teamApi } from '@/api/team'
import { mediaUrl } from '@/utils/media'
import { useSeo } from '@/composables/useSeo'
import PageHeader from '@/components/public/PageHeader.vue'
import AppLoader from '@/components/ui/AppLoader.vue'
import type { TeamMember } from '@/types'

useSeo({ title: 'Jamoa' })
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
  <div>
    <PageHeader label="Jamoa" title="Natija ortidagi odamlar" description="Professional dasturchilar, dizaynerlar va menejerlar — birgalikda kuchli jamoamiz" />
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-16">

      <AppLoader v-if="loading" :rows="4" :cols="4" />

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="member in members" :key="member.id" class="card text-center group">
          <div class="relative w-24 h-24 mx-auto mb-5">
            <img v-if="member.photo_url" :src="mediaUrl(member.photo_url)" :alt="member.full_name"
              class="w-24 h-24 rounded-full object-cover border-2 border-transparent group-hover:border-primary-500 transition-all duration-300" />
            <div v-else class="w-24 h-24 rounded-full bg-primary-500/10 flex items-center justify-center text-4xl border-2 border-transparent group-hover:border-primary-500 transition-all">👤</div>
          </div>
          <h3 class="font-semibold text-gray-900 dark:text-white group-hover:text-primary-500 transition-colors">{{ member.full_name }}</h3>
          <p class="text-sm text-primary-500 dark:text-primary-400 font-medium mt-1">{{ member.position }}</p>
          <p v-if="member.bio" class="text-sm text-gray-500 dark:text-gray-400 mt-3 leading-relaxed">{{ member.bio }}</p>
          <div class="flex justify-center gap-2 mt-4">
            <a v-if="member.telegram_url" :href="member.telegram_url" target="_blank"
              class="p-2 rounded-lg hover:text-primary-500 hover:bg-primary-500/10 transition-colors text-gray-400">
              <Send class="w-4 h-4" />
            </a>
            <a v-if="member.linkedin_url" :href="member.linkedin_url" target="_blank"
              class="p-2 rounded-lg hover:text-primary-500 hover:bg-primary-500/10 transition-colors text-gray-400">
              <Linkedin class="w-4 h-4" />
            </a>
            <a v-if="member.github_url" :href="member.github_url" target="_blank"
              class="p-2 rounded-lg hover:text-primary-500 hover:bg-primary-500/10 transition-colors text-gray-400">
              <Github class="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
