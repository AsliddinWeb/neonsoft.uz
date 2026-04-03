<script setup lang="ts">
import Navbar from '@/components/public/Navbar.vue'
import Footer from '@/components/public/Footer.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-1">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>
