<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ArrowRight, MoveUpRight } from 'lucide-vue-next'
import { RouterLink, useRouter } from 'vue-router'
import { servicesApi } from '@/api/services'
import { SERVICE_ICONS } from '@/utils/serviceIcons'
import type { Service } from '@/types'

const services = ref<Service[]>([])
const loading = ref(true)
const router = useRouter()

onMounted(async () => {
  try {
    const { data } = await servicesApi.list()
    services.value = data.slice(0, 4)
  } finally {
    loading.value = false
  }
})

function openRequest(svc: Service) {
  router.push({ path: '/services/request', query: { id: svc.id } })
}

const colors = [
  'bg-primary-500/10 text-primary-500',
  'bg-blue-500/10 text-blue-500',
  'bg-purple-500/10 text-purple-500',
  'bg-accent/10 text-accent',
  'bg-emerald-500/10 text-emerald-500',
  'bg-pink-500/10 text-pink-500',
]
</script>

<template>
  <section id="services" class="py-28 bg-white dark:bg-secondary relative overflow-hidden">
    <!-- Decorative -->
    <div class="absolute top-0 right-0 w-96 h-96 bg-primary-500/[0.03] rounded-full blur-[100px] pointer-events-none" />
    <div class="absolute bottom-0 left-0 w-72 h-72 bg-accent/[0.03] rounded-full blur-[80px] pointer-events-none" />

    <div class="container mx-auto px-4 sm:px-6 lg:px-8 relative">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
        <div>
          <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest mb-3">
            <span class="w-8 h-px bg-primary-500" /> Xizmatlar
          </span>
          <h2 class="section-title">Nima qila olamiz?</h2>
          <p class="text-gray-500 dark:text-gray-400 mt-3 max-w-lg">
            G'oyadan tayyor mahsulotgacha — har bir bosqichda yoningizda bo'lamiz
          </p>
        </div>
        <RouterLink to="/services" class="btn-outline shrink-0 inline-flex self-start md:self-auto">
          Barchasi <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 6" :key="i" class="rounded-2xl border border-gray-100 dark:border-gray-800 p-7 space-y-3">
          <div class="skeleton h-12 w-12 rounded-xl" />
          <div class="skeleton h-5 w-3/4" />
          <div class="skeleton h-4 w-full" />
        </div>
      </div>

      <!-- Cards -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="(svc, i) in services"
          :key="svc.id"
          @click="openRequest(svc)"
          class="group relative bg-gray-50 dark:bg-surface rounded-2xl border border-gray-100 dark:border-gray-800 p-7 cursor-pointer hover:-translate-y-2 hover:bg-white hover:shadow-2xl hover:shadow-primary-500/[0.08] hover:border-primary-500/30 transition-all duration-300 overflow-hidden"
        >
          <!-- Glow on hover -->
          <div class="absolute inset-0 bg-gradient-to-br from-primary-500/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" />

          <!-- Icon -->
          <div :class="[
            'relative w-14 h-14 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300',
            colors[i % colors.length]
          ]">
            <component
              :is="SERVICE_ICONS[svc.icon] || SERVICE_ICONS['Zap']"
              class="w-7 h-7"
            />
          </div>

          <!-- Content -->
          <h3 class="relative font-display font-semibold text-lg text-gray-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors">
            {{ svc.title }}
          </h3>
          <p class="relative text-gray-500 dark:text-gray-400 text-sm leading-relaxed">
            {{ svc.short_description }}
          </p>

          <!-- Arrow -->
          <div class="relative flex items-center gap-1 mt-6 text-primary-500 text-sm font-medium opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
            Buyurtma berish <MoveUpRight class="w-4 h-4" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
