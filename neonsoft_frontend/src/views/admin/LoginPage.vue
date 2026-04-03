<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import ThemeToggle from '@/components/public/ThemeToggle.vue'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const loading = ref(false)
const form = reactive({ email: '', password: '' })

async function login() {
  loading.value = true
  try {
    await auth.login(form.email, form.password)
    await router.push('/admin/dashboard')
  } catch {
    toast.error("Email yoki parol noto'g'ri")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-secondary flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent/5 rounded-full blur-3xl" />
    </div>

    <!-- Theme toggle -->
    <div class="absolute top-4 right-4">
      <ThemeToggle />
    </div>

    <div class="w-full max-w-md z-10">
      <div class="bg-white dark:bg-surface rounded-2xl shadow-2xl p-8 border border-gray-100 dark:border-gray-800">
        <!-- Logo -->
        <div class="text-center mb-8">
          <div class="w-14 h-14 rounded-2xl bg-primary-500 flex items-center justify-center mx-auto mb-4">
            <span class="font-display font-bold text-2xl text-secondary">N</span>
          </div>
          <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Admin Panel</h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">NeonSoft boshqaruv paneli</p>
        </div>

        <form @submit.prevent="login" class="space-y-4">
          <AppInput v-model="form.email" type="email" label="Email" placeholder="admin@neonsoft.uz" required />
          <AppInput v-model="form.password" type="password" label="Parol" placeholder="••••••••" required />
          <AppButton type="submit" :loading="loading" class="w-full" size="lg">
            Kirish
          </AppButton>
        </form>
      </div>
    </div>
  </div>
</template>
