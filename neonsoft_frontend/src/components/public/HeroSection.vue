<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight, ChevronDown, Code2, Smartphone, Bot, Settings, Play } from 'lucide-vue-next'
import { useSettingsStore } from '@/stores/settings'
import { mediaUrl } from '@/utils/media'

const store = useSettingsStore()
const visible = ref(false)
onMounted(() => setTimeout(() => (visible.value = true), 100))
</script>

<template>
  <section class="relative min-h-screen flex items-center overflow-hidden bg-[#0d1424]">
    <!-- Background effects -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-[15%] left-[10%] w-[500px] h-[500px] bg-primary-500/20 rounded-full blur-[120px]" />
      <div class="absolute bottom-[10%] right-[5%] w-[400px] h-[400px] bg-accent/10 rounded-full blur-[100px]" />
      <div class="absolute top-[60%] left-[50%] w-[300px] h-[300px] bg-primary-500/8 rounded-full blur-[80px]" />
      <div class="absolute inset-0 bg-[linear-gradient(rgba(0,212,170,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,212,170,0.03)_1px,transparent_1px)] bg-[size:64px_64px]" />
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,#0d1424_75%)]" />
    </div>

    <div class="relative container mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        <!-- Left: Content -->
        <div :class="['transition-all duration-1000', visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']">
          <!-- Company badge -->
          <div class="inline-flex items-center gap-3 px-5 py-2.5 rounded-2xl border border-white/[0.08] bg-white/[0.04] backdrop-blur-sm mb-8">
            <img
              v-if="store.settings?.logo_url"
              :src="mediaUrl(store.settings.logo_url)"
              alt="Logo"
              class="w-7 h-7 rounded-lg object-cover"
            />
            <div v-else class="w-7 h-7 rounded-lg bg-primary-500/15 flex items-center justify-center">
              <span class="font-display font-bold text-xs text-primary-500">N</span>
            </div>
            <span class="text-white/70 text-sm font-medium">{{ store.settings?.company_name || 'NeonSoft' }}</span>
            <span class="h-4 w-px bg-white/10" />
            <span class="text-primary-400 text-xs font-medium uppercase tracking-wider">IT Solutions</span>
          </div>

          <!-- Headline -->
          <h1 class="font-display font-bold text-4xl sm:text-5xl lg:text-6xl xl:text-7xl text-white leading-[1.1] mb-6">
            Biznesingizni
            <br />
            <span class="relative inline-block">
              <span class="gradient-text">raqamlashtiring</span>
              <svg class="absolute -bottom-1 left-0 w-full h-2 text-primary-500/25" viewBox="0 0 200 8" preserveAspectRatio="none">
                <path d="M0 7 Q50 0 100 4 Q150 8 200 1" stroke="currentColor" stroke-width="2" fill="none" />
              </svg>
            </span>
          </h1>

          <!-- Description -->
          <p class="text-lg text-gray-400 max-w-lg leading-relaxed mb-10">
            Web platformalar, mobil ilovalar va biznes tizimlar — <span class="text-gray-300">professional jamoa bilan yarating.</span> Birinchi konsultatsiya bepul.
          </p>

          <!-- CTAs -->
          <div class="flex flex-col sm:flex-row gap-4 mb-14">
            <RouterLink
              to="/services"
              class="group inline-flex items-center gap-2.5 bg-primary-500 hover:bg-primary-400 text-secondary font-semibold px-8 py-4 rounded-2xl text-base transition-all duration-300 hover:shadow-lg hover:shadow-primary-500/25 hover:-translate-y-0.5"
            >
              Loyihani boshlash
              <ArrowRight class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </RouterLink>
            <RouterLink
              to="/projects"
              class="group inline-flex items-center gap-2.5 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 text-white font-medium px-8 py-4 rounded-2xl text-base transition-all duration-300 backdrop-blur-sm"
            >
              <Play class="w-4 h-4 text-primary-500" />
              Ishlarimiz
            </RouterLink>
          </div>

          <!-- Stats -->
          <div class="flex gap-10">
            <div v-for="stat in [
              { value: '50+', label: 'Loyiha' },
              { value: '30+', label: 'Mijoz' },
              { value: '3+', label: 'Yil' },
            ]" :key="stat.label">
              <div class="font-display font-bold text-3xl text-white">{{ stat.value }}</div>
              <div class="text-gray-500 text-sm mt-0.5">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <!-- Right: Floating cards -->
        <div
          :class="['relative hidden lg:block transition-all duration-1000 delay-300', visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12']"
        >
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-80 h-80 bg-primary-500/10 rounded-full blur-[100px]" />
          </div>

          <div class="relative w-full aspect-square max-w-lg mx-auto">
            <!-- Card 1: Web -->
            <div class="absolute top-[5%] left-[10%] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 w-52 hover:bg-white/10 hover:border-primary-500/30 transition-all duration-500 animate-float">
              <div class="w-10 h-10 rounded-xl bg-primary-500/15 flex items-center justify-center mb-3">
                <Code2 class="w-5 h-5 text-primary-500" />
              </div>
              <h4 class="text-white font-semibold text-sm mb-1">Web Dasturlash</h4>
              <p class="text-gray-500 text-xs leading-relaxed">Zamonaviy va tez ishlaydigan platformalar</p>
            </div>

            <!-- Card 2: Mobile -->
            <div class="absolute top-[8%] right-[5%] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 w-48 hover:bg-white/10 hover:border-primary-500/30 transition-all duration-500 animate-float" style="animation-delay: 1s">
              <div class="w-10 h-10 rounded-xl bg-accent/15 flex items-center justify-center mb-3">
                <Smartphone class="w-5 h-5 text-accent" />
              </div>
              <h4 class="text-white font-semibold text-sm mb-1">Mobil Ilovalar</h4>
              <p class="text-gray-500 text-xs leading-relaxed">iOS va Android uchun</p>
            </div>

            <!-- Card 3: Bot -->
            <div class="absolute bottom-[18%] left-[5%] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 w-48 hover:bg-white/10 hover:border-primary-500/30 transition-all duration-500 animate-float" style="animation-delay: 2s">
              <div class="w-10 h-10 rounded-xl bg-blue-500/15 flex items-center justify-center mb-3">
                <Bot class="w-5 h-5 text-blue-400" />
              </div>
              <h4 class="text-white font-semibold text-sm mb-1">Telegram Bot</h4>
              <p class="text-gray-500 text-xs leading-relaxed">24/7 avtomatik tizim</p>
            </div>

            <!-- Card 4: Automation -->
            <div class="absolute bottom-[12%] right-[8%] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 w-52 hover:bg-white/10 hover:border-primary-500/30 transition-all duration-500 animate-float" style="animation-delay: 0.5s">
              <div class="w-10 h-10 rounded-xl bg-purple-500/15 flex items-center justify-center mb-3">
                <Settings class="w-5 h-5 text-purple-400" />
              </div>
              <h4 class="text-white font-semibold text-sm mb-1">Avtomatizatsiya</h4>
              <p class="text-gray-500 text-xs leading-relaxed">Biznes jarayonlarni raqamlashtirish</p>
            </div>

            <!-- Center N -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 rounded-2xl bg-primary-500/10 border border-primary-500/20 flex items-center justify-center rotate-12 hover:rotate-0 transition-transform duration-500">
              <span class="font-display font-bold text-3xl text-primary-500">N</span>
            </div>

            <!-- Connecting lines -->
            <svg class="absolute inset-0 w-full h-full pointer-events-none opacity-20" viewBox="0 0 400 400">
              <line x1="200" y1="200" x2="80" y2="60" stroke="url(#hero-grad)" stroke-width="1" />
              <line x1="200" y1="200" x2="340" y2="80" stroke="url(#hero-grad)" stroke-width="1" />
              <line x1="200" y1="200" x2="60" y2="300" stroke="url(#hero-grad)" stroke-width="1" />
              <line x1="200" y1="200" x2="350" y2="320" stroke="url(#hero-grad)" stroke-width="1" />
              <defs>
                <linearGradient id="hero-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#00D4AA" stop-opacity="0.6" />
                  <stop offset="100%" stop-color="#00D4AA" stop-opacity="0" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll -->
    <a href="#services" class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1.5 text-gray-600 hover:text-primary-500 transition-colors group">
      <span class="text-[10px] uppercase tracking-[0.25em] font-medium">Scroll</span>
      <ChevronDown class="w-4 h-4 animate-bounce" />
    </a>
  </section>
</template>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}
.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>
