<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Home, ArrowLeft } from 'lucide-vue-next'
import { useSeo } from '@/composables/useSeo'
useSeo({ title: '404 - Sahifa topilmadi' })
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-white dark:bg-secondary px-4">
    <div class="text-center">
      <div class="font-display font-bold text-9xl text-primary-500 mb-4 animate-pulse">404</div>
      <h1 class="font-display font-bold text-3xl text-gray-900 dark:text-white mb-3">
        Sahifa topilmadi
      </h1>
      <p class="text-gray-500 dark:text-gray-400 mb-8 max-w-sm mx-auto">
        Bu sahifa mavjud emas yoki boshqa manzilga ko'chirilgan bo'lishi mumkin.
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <RouterLink to="/" class="btn-primary">
          <Home class="w-4 h-4" /> Bosh sahifa
        </RouterLink>
        <button @click="$router.back()" class="btn-outline">
          <ArrowLeft class="w-4 h-4" /> Orqaga
        </button>
      </div>
    </div>
  </div>
</template>
