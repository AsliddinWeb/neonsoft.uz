<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { MoveUpRight } from 'lucide-vue-next'
import { servicesApi } from '@/api/services'
import { useSeo } from '@/composables/useSeo'
import { SERVICE_ICONS } from '@/utils/serviceIcons'
import PageHeader from '@/components/public/PageHeader.vue'
import type { Service } from '@/types'

useSeo({ title: 'Xizmatlar' })
const router = useRouter()
const services = ref<Service[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await servicesApi.list()
    services.value = data
  } finally {
    loading.value = false
  }
})

function openRequest(svc: Service) {
  router.push({ path: '/services/request', query: { id: svc.id, title: svc.title } })
}
</script>

<template>
  <div>
    <PageHeader label="Xizmatlar" title="Biznesingizga kerakli yechim bor" description="Xizmatni tanlang va loyihangiz uchun bepul konsultatsiya oling" />
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-16">

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="rounded-2xl border border-gray-100 dark:border-gray-800 p-6 space-y-3">
          <div class="skeleton h-14 w-14 rounded-2xl" />
          <div class="skeleton h-5 w-3/4" />
          <div class="skeleton h-4 w-full" />
          <div class="skeleton h-4 w-5/6" />
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="svc in services"
          :key="svc.id"
          @click="openRequest(svc)"
          class="group relative bg-gray-50 dark:bg-surface rounded-2xl border border-gray-100 dark:border-gray-800 p-6 cursor-pointer hover:-translate-y-2 hover:bg-white hover:shadow-xl hover:shadow-primary-500/10 hover:border-primary-500/30 transition-all duration-300 overflow-hidden"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" />

          <div class="relative w-14 h-14 rounded-2xl bg-primary-500/10 flex items-center justify-center mb-5 group-hover:bg-primary-500/20 group-hover:scale-110 transition-all duration-300">
            <component
              :is="SERVICE_ICONS[svc.icon ?? ''] || SERVICE_ICONS['Zap']"
              class="w-7 h-7 text-primary-500"
            />
          </div>

          <h3 class="relative font-display font-semibold text-xl text-gray-900 dark:text-white mb-3 group-hover:text-primary-500 transition-colors">
            {{ svc.title }}
          </h3>
          <p class="relative text-gray-500 dark:text-gray-400 text-sm leading-relaxed mb-2">
            {{ svc.short_description }}
          </p>
          <p class="relative text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
            {{ svc.description }}
          </p>

          <div class="relative flex items-center gap-1 mt-5 text-primary-500 text-sm font-medium opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
            So'rov qoldirish <MoveUpRight class="w-4 h-4" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
