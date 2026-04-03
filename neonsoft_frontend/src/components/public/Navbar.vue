<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { Menu, X, Phone } from 'lucide-vue-next'
import ThemeToggle from './ThemeToggle.vue'
import { useSettingsStore } from '@/stores/settings'
import { mediaUrl } from '@/utils/media'

const store = useSettingsStore()

const shortPhone = computed(() => {
  const phone = store.settings?.phone
  if (!phone) return ''
  // +998 (94) 202-55-11 -> (94) 202-55-11
  return phone.replace(/^\+?\d{3}\s*/, '')
})
const route = useRoute()
const mobileOpen = ref(false)
const scrolled = ref(false)

const isHome = computed(() => route.path === '/')
const transparent = computed(() => isHome.value && !scrolled.value)

const links = [
  { to: '/', label: 'Bosh sahifa' },
  { to: '/services', label: 'Xizmatlar' },
  { to: '/projects', label: 'Loyihalar' },
  { to: '/team', label: 'Jamoa' },
  { to: '/blog', label: 'Blog' },
  { to: '/contact', label: 'Aloqa' },
]

function onScroll() {
  scrolled.value = window.scrollY > 20
}
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-40 transition-all duration-300',
      transparent
        ? 'bg-transparent'
        : 'bg-white/95 dark:bg-secondary/95 backdrop-blur-md shadow-sm border-b border-gray-100 dark:border-gray-800',
    ]"
  >
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 md:h-20">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-3 group">
          <img
            v-if="store.settings?.logo_url"
            :src="mediaUrl(store.settings.logo_url)"
            alt="Logo"
            class="h-9 w-9 rounded-lg object-cover"
          />
          <div v-else class="h-9 w-9 rounded-lg bg-primary-500 flex items-center justify-center">
            <span class="text-secondary font-bold text-lg font-display">N</span>
          </div>
          <span :class="[
            'font-display font-bold text-xl group-hover:text-primary-500 transition-colors',
            transparent ? 'text-white' : 'text-gray-900 dark:text-white',
          ]">
            {{ store.settings?.company_name || 'NeonSoft' }}
          </span>
        </RouterLink>

        <!-- Desktop nav -->
        <nav class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              route.path === link.to
                ? transparent
                  ? 'text-white bg-white/15'
                  : 'text-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : transparent
                  ? 'text-white/80 hover:text-white hover:bg-white/10'
                  : 'text-gray-600 dark:text-gray-300 hover:text-primary-500 hover:bg-gray-50 dark:hover:bg-gray-800',
            ]"
          >
            {{ link.label }}
          </RouterLink>
        </nav>

        <!-- Right -->
        <div class="flex items-center gap-3">
          <ThemeToggle :transparent="transparent" />
          <a
            v-if="store.settings?.phone"
            :href="`tel:${store.settings.phone}`"
            :class="[
              'hidden md:inline-flex items-center gap-2 text-sm font-medium px-4 py-2 rounded-xl transition-all duration-200',
              transparent
                ? 'text-white border border-white/25 hover:bg-white/10 hover:border-white/40'
                : 'text-primary-600 dark:text-primary-400 bg-primary-500/10 hover:bg-primary-500/20',
            ]"
          >
            <Phone class="w-3.5 h-3.5" />
            {{ shortPhone }}
          </a>
          <button
            :class="[
              'md:hidden p-2 rounded-lg transition-colors',
              transparent
                ? 'text-white hover:bg-white/10'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800',
            ]"
            @click="mobileOpen = !mobileOpen"
          >
            <X v-if="mobileOpen" class="w-5 h-5" />
            <Menu v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition name="slide-down">
      <div
        v-if="mobileOpen"
        class="md:hidden bg-white dark:bg-secondary border-t border-gray-100 dark:border-gray-800 px-4 py-3 space-y-1"
      >
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          @click="mobileOpen = false"
          :class="[
            'block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors',
            route.path === link.to
              ? 'text-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'text-gray-700 dark:text-gray-300 hover:text-primary-500',
          ]"
        >
          {{ link.label }}
        </RouterLink>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
