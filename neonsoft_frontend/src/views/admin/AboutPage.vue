<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Biz haqimizda</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">About sahifasini boshqarish</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-16">
      <AppLoader />
    </div>

    <form v-else @submit.prevent="save" class="space-y-6">
      <!-- Matnlar -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 space-y-5">
        <h2 class="font-semibold text-gray-900 dark:text-white">Asosiy ma'lumotlar</h2>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sarlavha</label>
          <input v-model="form.title" type="text" class="input-field" placeholder="Biz haqimizda" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tagline</label>
          <input v-model="form.subtitle" type="text" class="input-field" placeholder="NeonSoft — raqamli kelajakni birga quramiz" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tavsif</label>
          <textarea v-model="form.description" rows="5" class="input-field" placeholder="Kompaniya haqida to'liq ma'lumot..." />
        </div>
      </div>

      <!-- Rasm -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 space-y-4">
        <h2 class="font-semibold text-gray-900 dark:text-white">Asosiy rasm</h2>

        <div v-if="form.image_url" class="relative inline-block">
          <img :src="mediaUrl(form.image_url)" alt="About" class="h-48 w-full object-cover rounded-xl" />
          <button type="button" @click="form.image_url = ''"
            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600">
            <X class="w-4 h-4" />
          </button>
        </div>

        <div v-else
          class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8 text-center cursor-pointer hover:border-primary-500 transition-colors"
          @click="imageInput?.click()">
          <ImageIcon class="w-10 h-10 mx-auto text-gray-400 mb-2" />
          <p class="text-sm text-gray-500">Rasm yuklash uchun bosing</p>
        </div>

        <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="uploadImage" />
        <div v-if="uploading" class="flex items-center gap-2 text-sm text-primary-500">
          <AppLoader size="sm" /> Yuklanmoqda...
        </div>
      </div>

      <!-- Statistika -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 class="font-semibold text-gray-900 dark:text-white mb-5">Statistika raqamlari</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Loyihalar</label>
            <input v-model.number="form.stat_projects" type="number" min="0" class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Mijozlar</label>
            <input v-model.number="form.stat_clients" type="number" min="0" class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Yillar</label>
            <input v-model.number="form.stat_years" type="number" min="0" class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Jamoa</label>
            <input v-model.number="form.stat_team" type="number" min="0" class="input-field" />
          </div>
        </div>
      </div>

      <div class="flex justify-end">
        <button type="submit" :disabled="saving" class="btn-primary px-8">
          <span v-if="saving">Saqlanmoqda...</span>
          <span v-else>Saqlash</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { X, Image as ImageIcon } from 'lucide-vue-next'
import { aboutApi } from '@/api/about'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import AppLoader from '@/components/ui/AppLoader.vue'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const imageInput = ref<HTMLInputElement>()

const form = ref({
  title: '',
  subtitle: '',
  description: '',
  image_url: '',
  stat_projects: 0,
  stat_clients: 0,
  stat_years: 0,
  stat_team: 0,
})

onMounted(async () => {
  try {
    const data = await aboutApi.adminGet()
    form.value = {
      title: data.title || '',
      subtitle: data.subtitle || '',
      description: data.description || '',
      image_url: data.image_url || '',
      stat_projects: data.stat_projects,
      stat_clients: data.stat_clients,
      stat_years: data.stat_years,
      stat_team: data.stat_team,
    }
  } finally {
    loading.value = false
  }
})

async function uploadImage(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const res = await uploadApi.image(file)
    form.value.image_url = res.data.url
  } catch {
    toast.error('Rasm yuklashda xato')
  } finally {
    uploading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    await aboutApi.update(form.value)
    toast.success('Saqlandi!')
  } catch {
    toast.error('Xato yuz berdi')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.input-field {
  @apply w-full px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-600
    bg-white dark:bg-gray-700 text-gray-900 dark:text-white
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
    placeholder-gray-400 dark:placeholder-gray-500 transition;
}
</style>