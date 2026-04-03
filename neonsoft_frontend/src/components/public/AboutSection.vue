<template>
  <section class="py-24 bg-gray-50 dark:bg-surface overflow-hidden">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        <!-- Image side -->
        <div class="relative order-2 lg:order-1">
          <div class="relative rounded-3xl overflow-hidden aspect-[4/3] shadow-2xl shadow-primary-500/20">
            <img
              v-if="about?.image_url"
              :src="mediaUrl(about.image_url)"
              alt="About"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-primary-500/20 to-accent/20 flex items-center justify-center">
              <div class="text-center space-y-2">
                <div class="w-20 h-20 rounded-2xl bg-primary-500/20 flex items-center justify-center mx-auto">
                  <Award class="w-10 h-10 text-primary-500" />
                </div>
              </div>
            </div>
            <div class="absolute -bottom-4 -right-4 w-32 h-32 bg-primary-500/10 rounded-full blur-2xl" />
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-4 gap-3 mt-6">
            <div
              v-for="stat in stats"
              :key="stat.label"
              class="bg-white dark:bg-surface rounded-2xl p-3 text-center shadow-sm border border-gray-100 dark:border-gray-800 hover:shadow-md hover:border-primary-500/30 transition-all"
            >
              <component :is="stat.icon" class="w-4 h-4 text-primary-500 mx-auto mb-1" />
              <p class="font-display font-bold text-lg text-gray-900 dark:text-white">{{ stat.value }}+</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 leading-tight">{{ stat.label }}</p>
            </div>
          </div>
        </div>

        <!-- Text side -->
        <div class="order-1 lg:order-2 space-y-6">
          <span class="inline-flex items-center gap-2 text-primary-500 text-sm font-semibold uppercase tracking-widest">
            <span class="w-8 h-px bg-primary-500" /> Biz haqimizda
          </span>
          <h2 class="font-display font-bold text-4xl lg:text-5xl text-gray-900 dark:text-white leading-tight">
            {{ about?.title || settingsStore.settings?.company_name || 'NeonSoft' }} —
            <span class="gradient-text">{{ about?.subtitle || 'texnologiya orqali o\'sish' }}</span>
          </h2>
          <p class="text-gray-500 dark:text-gray-400 text-lg leading-relaxed">
            {{ about?.description || "Biz shunchaki kod yozmaymiz — biznesingiz uchun ishlaydigon mahsulot yaratamiz. Har bir loyihani chuqur tahlil qilamiz, mijoz maqsadini tushunamiz va natijaga yo'naltirilgan yechim taklif etamiz." }}
          </p>

          <ul class="space-y-3">
            <li
              v-for="f in features"
              :key="f"
              class="flex items-center gap-3 text-gray-600 dark:text-gray-300"
            >
              <CheckCircle2 class="w-5 h-5 text-primary-500 shrink-0" />
              {{ f }}
            </li>
          </ul>

          <div class="flex flex-wrap gap-4 pt-2">
            <a href="#services" class="btn-primary">Xizmatlarni ko'rish</a>
            <a href="#contact" class="btn-outline">Bepul konsultatsiya</a>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { CheckCircle2, Award, FolderOpen, Users2, Clock, Users } from 'lucide-vue-next'
import { aboutApi, type About } from '@/api/about'
import { useSettingsStore } from '@/stores/settings'
import { mediaUrl } from '@/utils/media'

const settingsStore = useSettingsStore()
const about = ref<About | null>(null)

onMounted(async () => {
  try { about.value = await aboutApi.get() } catch {}
})

const stats = computed(() => [
  { icon: FolderOpen, value: about.value?.stat_projects ?? 50,  label: 'Loyihalar' },
  { icon: Users2,     value: about.value?.stat_clients  ?? 30,  label: 'Mijozlar' },
  { icon: Clock,      value: about.value?.stat_years    ?? 5,   label: 'Yil tajriba' },
  { icon: Users,      value: about.value?.stat_team     ?? 15,  label: 'Jamoa' },
])

const features = [
  "Vue, React, Django, FastAPI — eng so'nggi texnologiyalar",
  "Kelishilgan muddatda 100% topshirish kafolati",
  "Loyihadan keyin 3 oy bepul texnik qo'llab-quvvatlash",
  "Sizning biznesingizga moslashtirilgan individual yechim",
]
</script>