<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ArrowRight } from 'lucide-vue-next'
</script>

<template>
  <section class="py-16 bg-white dark:bg-secondary">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6 bg-primary-500/5 dark:bg-primary-500/10 border border-primary-500/10 dark:border-primary-500/20 rounded-3xl px-10 py-10">
        <div>
          <h3 class="font-display font-bold text-2xl text-gray-900 dark:text-white mb-2">Loyihangizni bugun boshlang</h3>
          <p class="text-gray-500 dark:text-gray-400">Bepul konsultatsiya oling va g'oyangizni hayotga tatbiq eting</p>
        </div>
        <RouterLink to="/services" class="btn-primary shrink-0 px-8 py-3.5 text-base">
          Boshlash <ArrowRight class="w-5 h-5" />
        </RouterLink>
      </div>
    </div>
  </section>
</template>
