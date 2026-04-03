<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/admin/Sidebar.vue'
import Topbar from '@/components/admin/Topbar.vue'

const sidebarOpen = ref(false)
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-secondary flex">
    <Sidebar :open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 flex flex-col min-w-0 lg:ml-64">
      <Topbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="flex-1 p-4 lg:p-6 overflow-x-hidden">
        <RouterView />
      </main>
    </div>
  </div>
</template>
