<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Send, Instagram, Linkedin, Github, Mail, Phone, MapPin } from 'lucide-vue-next'
import { useSettingsStore } from '@/stores/settings'

const store = useSettingsStore()
</script>

<template>
  <footer class="bg-secondary text-gray-300 pt-16 pb-8">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        <!-- Brand -->
        <div class="lg:col-span-2">
          <span class="font-display font-bold text-2xl text-white">
            {{ store.settings?.company_name || 'NeonSoft' }}
          </span>
          <p class="mt-3 text-gray-400 leading-relaxed max-w-sm">
            G'oyangiz bor — biz uni hayotga tatbiq etamiz. Raqamli yechimlar bo'yicha ishonchli hamkoringiz.
          </p>
          <div class="flex gap-3 mt-5">
            <a v-if="store.settings?.telegram" :href="store.settings.telegram" target="_blank"
              class="p-2.5 rounded-xl bg-gray-800 hover:bg-primary-500 hover:text-secondary transition-all duration-200">
              <Send class="w-4 h-4" />
            </a>
            <a v-if="store.settings?.instagram" :href="store.settings.instagram" target="_blank"
              class="p-2.5 rounded-xl bg-gray-800 hover:bg-primary-500 hover:text-secondary transition-all duration-200">
              <Instagram class="w-4 h-4" />
            </a>
            <a v-if="store.settings?.linkedin" :href="store.settings.linkedin" target="_blank"
              class="p-2.5 rounded-xl bg-gray-800 hover:bg-primary-500 hover:text-secondary transition-all duration-200">
              <Linkedin class="w-4 h-4" />
            </a>
            <a v-if="store.settings?.github" :href="store.settings.github" target="_blank"
              class="p-2.5 rounded-xl bg-gray-800 hover:bg-primary-500 hover:text-secondary transition-all duration-200">
              <Github class="w-4 h-4" />
            </a>
          </div>
        </div>

        <!-- Links -->
        <div>
          <h4 class="font-display font-semibold text-white mb-4">Sahifalar</h4>
          <ul class="space-y-2.5">
            <li v-for="link in [['/', 'Bosh sahifa'], ['/services', 'Xizmatlar'], ['/projects', 'Loyihalar'], ['/team', 'Jamoa'], ['/blog', 'Blog']]" :key="link[0]">
              <RouterLink :to="link[0]" class="hover:text-primary-500 transition-colors text-sm">
                {{ link[1] }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="font-display font-semibold text-white mb-4">Aloqa</h4>
          <ul class="space-y-3 text-sm">
            <li v-if="store.settings?.email" class="flex items-center gap-2">
              <Mail class="w-4 h-4 text-primary-500 shrink-0" />
              <a :href="`mailto:${store.settings.email}`" class="hover:text-primary-500 transition-colors">
                {{ store.settings.email }}
              </a>
            </li>
            <li v-if="store.settings?.phone" class="flex items-center gap-2">
              <Phone class="w-4 h-4 text-primary-500 shrink-0" />
              <a :href="`tel:${store.settings.phone}`" class="hover:text-primary-500 transition-colors">
                {{ store.settings.phone }}
              </a>
            </li>
            <li v-if="store.settings?.address" class="flex items-start gap-2">
              <MapPin class="w-4 h-4 text-primary-500 shrink-0 mt-0.5" />
              <span>{{ store.settings.address }}</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-500">
        © {{ new Date().getFullYear() }} {{ store.settings?.company_name || 'NeonSoft' }}. Barcha huquqlar himoyalangan.
      </div>
    </div>
  </footer>
</template>
