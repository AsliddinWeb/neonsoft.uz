<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { settingsApi } from '@/api/settings'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import { useToast } from 'vue-toastification'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)

const form = reactive({
  company_name: '', tagline: '', description: '', email: '', phone: '', address: '', logo_url: '',
  telegram: '', instagram: '', linkedin: '', github: '',
  meta_title: '', meta_description: '', meta_keywords: '',
})

onMounted(async () => {
  try {
    const { data } = await settingsApi.adminGet()
    Object.assign(form, { company_name: data.company_name, tagline: data.tagline || '', description: data.description || '', email: data.email || '', phone: data.phone || '', address: data.address || '', logo_url: data.logo_url || '', telegram: data.telegram || '', instagram: data.instagram || '', linkedin: data.linkedin || '', github: data.github || '', meta_title: data.meta_title || '', meta_description: data.meta_description || '', meta_keywords: data.meta_keywords || '' })
  } finally {
    loading.value = false
  }
})

async function uploadLogo(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { data } = await uploadApi.image(file)
    form.logo_url = data.url
  } finally {
    uploading.value = false
  }
}


async function save() {
  saving.value = true
  try {
    await settingsApi.update(form)
    toast.success('Sozlamalar saqlandi')
  } catch { /* handled */ } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl space-y-8">
    <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Sayt sozlamalari</h1>

    <div v-if="loading" class="animate-pulse space-y-4">
      <div v-for="i in 6" :key="i" class="skeleton h-10 rounded-xl" />
    </div>

    <form v-else @submit.prevent="save" class="space-y-8">
      <!-- General -->
      <section class="card space-y-4">
        <h2 class="font-display font-semibold text-gray-900 dark:text-white">Umumiy ma'lumotlar</h2>

        <!-- Logo -->
        <div class="flex items-center gap-5">
          <div class="w-16 h-16 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 flex items-center justify-center">
            <img v-if="form.logo_url" :src="mediaUrl(form.logo_url)" class="w-full h-full object-cover" />
            <span v-else class="text-2xl">🖼️</span>
          </div>
          <label class="btn-outline text-sm cursor-pointer">
            {{ uploading ? 'Yuklanmoqda...' : 'Logo yuklash' }}
            <input type="file" accept="image/*" @change="uploadLogo" class="hidden" :disabled="uploading" />
          </label>
          <button v-if="form.logo_url" type="button" @click="form.logo_url = ''" class="text-xs text-red-500 hover:underline">O'chirish</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <AppInput v-model="form.company_name" label="Kompaniya nomi" required />
          <AppInput v-model="form.tagline" label="Tagline" />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Tavsif</label>
          <textarea v-model="form.description" rows="3" class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <AppInput v-model="form.email" type="email" label="Email" />
          <AppInput v-model="form.phone" label="Telefon" />
        </div>
        <AppInput v-model="form.address" label="Manzil" />

        <!-- About image -->
      </section>

      <!-- Social -->
      <section class="card space-y-4">
        <h2 class="font-display font-semibold text-gray-900 dark:text-white">Ijtimoiy tarmoqlar</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <AppInput v-model="form.telegram" label="Telegram" placeholder="https://t.me/..." />
          <AppInput v-model="form.instagram" label="Instagram" placeholder="https://instagram.com/..." />
          <AppInput v-model="form.linkedin" label="LinkedIn" placeholder="https://linkedin.com/..." />
          <AppInput v-model="form.github" label="GitHub" placeholder="https://github.com/..." />
        </div>
      </section>

      <!-- SEO -->
      <section class="card space-y-4">
        <h2 class="font-display font-semibold text-gray-900 dark:text-white">SEO</h2>
        <AppInput v-model="form.meta_title" label="Meta title" />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Meta description</label>
          <textarea v-model="form.meta_description" rows="3" class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
        </div>
        <AppInput v-model="form.meta_keywords" label="Meta keywords (vergul bilan)" />
      </section>

      <AppButton type="submit" :loading="saving" size="lg">Saqlash</AppButton>
    </form>
  </div>
</template>
