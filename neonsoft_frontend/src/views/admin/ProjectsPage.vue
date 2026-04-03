<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { projectsApi } from '@/api/projects'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import { useApi } from '@/composables/useApi'
import AppTable from '@/components/ui/AppTable.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import type { Project } from '@/types'

const { list, loading, fetch, create, update, remove } = useApi<Project>()
const showModal = ref(false)
const showConfirm = ref(false)
const editing = ref<Project | null>(null)
const deleteTarget = ref<Project | null>(null)
const saving = ref(false)
const uploading = ref(false)

const form = reactive({
  title: '', description: '', client_name: '', tech_stack: '',
  image_url: '', project_url: '', github_url: '',
  is_featured: false, order: 0, is_active: true,
})

const columns = [
  { key: 'image', label: '', class: 'w-16' },
  { key: 'title', label: 'Loyiha' },
  { key: 'tech', label: 'Texnologiyalar' },
  { key: 'status', label: 'Holat', class: 'w-28' },
  { key: 'actions', label: '', class: 'w-24' },
]

function openCreate() {
  editing.value = null
  Object.assign(form, { title: '', description: '', client_name: '', tech_stack: '', image_url: '', project_url: '', github_url: '', is_featured: false, order: 0, is_active: true })
  showModal.value = true
}

function openEdit(p: Project) {
  editing.value = p
  Object.assign(form, { title: p.title, description: p.description, client_name: p.client_name || '', tech_stack: (p.tech_stack || []).join(', '), image_url: p.image_url || '', project_url: p.project_url || '', github_url: p.github_url || '', is_featured: p.is_featured, order: p.order, is_active: p.is_active })
  showModal.value = true
}

async function uploadImage(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { data } = await uploadApi.image(file)
    form.image_url = data.url
  } finally {
    uploading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form, tech_stack: form.tech_stack ? form.tech_stack.split(',').map((s) => s.trim()).filter(Boolean) : [] }
    if (editing.value) {
      await update(() => projectsApi.update(editing.value!.id, payload))
    } else {
      await create(() => projectsApi.create(payload))
    }
    showModal.value = false
    await fetch(() => projectsApi.adminList())
  } catch { /* handled */ } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  await remove(() => projectsApi.delete(deleteTarget.value!.id))
  showConfirm.value = false
  await fetch(() => projectsApi.adminList())
}

onMounted(() => fetch(() => projectsApi.adminList()))
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Loyihalar</h1>
      <AppButton @click="openCreate" size="sm"><Plus class="w-4 h-4" /> Qo'shish</AppButton>
    </div>

    <AppTable :columns="columns" :loading="loading">
      <tr v-for="p in list" :key="p.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
        <td class="px-4 py-3">
          <img v-if="p.image_url" :src="mediaUrl(p.image_url)" class="w-10 h-10 rounded-lg object-cover" />
          <div v-else class="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center text-lg">🚀</div>
        </td>
        <td class="px-4 py-3">
          <p class="font-medium text-gray-900 dark:text-white">{{ p.title }}</p>
          <p v-if="p.client_name" class="text-xs text-gray-400">{{ p.client_name }}</p>
        </td>
        <td class="px-4 py-3">
          <div class="flex flex-wrap gap-1">
            <span v-for="t in (p.tech_stack || []).slice(0,3)" :key="t"
              class="px-1.5 py-0.5 text-xs font-mono bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded">{{ t }}</span>
          </div>
        </td>
        <td class="px-4 py-3 space-y-1">
          <AppBadge :variant="p.is_active ? 'success' : 'gray'">{{ p.is_active ? 'Faol' : 'Nofaol' }}</AppBadge>
          <AppBadge v-if="p.is_featured" variant="warning">Tanlangan</AppBadge>
        </td>
        <td class="px-4 py-3">
          <div class="flex gap-1">
            <button @click="openEdit(p)" class="p-1.5 rounded-lg hover:bg-primary-500/10 text-gray-400 hover:text-primary-500 transition-colors"><Pencil class="w-4 h-4" /></button>
            <button @click="() => { deleteTarget.value = p; showConfirm = true }" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors"><Trash2 class="w-4 h-4" /></button>
          </div>
        </td>
      </tr>
    </AppTable>

    <!-- Form modal -->
    <AppModal :open="showModal" :title="editing ? 'Loyihani tahrirlash' : 'Yangi loyiha'" size="lg" @close="showModal = false">
      <form id="project-form" @submit.prevent="save" class="space-y-4">
        <AppInput v-model="form.title" label="Sarlavha" required />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Tavsif *</label>
          <textarea v-model="form.description" rows="3" required class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="form.client_name" label="Mijoz nomi" />
          <AppInput v-model="form.tech_stack" label="Texnologiyalar (vergul bilan)" placeholder="Vue, FastAPI, PostgreSQL" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="form.project_url" label="Loyiha URL" />
          <AppInput v-model="form.github_url" label="GitHub URL" />
        </div>

        <!-- Image upload -->
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Rasm</label>
          <div v-if="form.image_url" class="relative w-full h-36 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <img :src="mediaUrl(form.image_url)" class="w-full h-full object-cover" />
            <button type="button" @click="form.image_url = ''" class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-lg text-xs">✕</button>
          </div>
          <label v-else class="flex flex-col items-center justify-center h-28 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl cursor-pointer hover:border-primary-500 transition-colors">
            <span class="text-sm text-gray-400">{{ uploading ? 'Yuklanmoqda...' : 'Rasm yuklash' }}</span>
            <input type="file" accept="image/*" @change="uploadImage" class="hidden" :disabled="uploading" />
          </label>
        </div>

        <div class="flex gap-4">
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="form.is_active" id="p_active" class="w-4 h-4 accent-primary-500" />
            <label for="p_active" class="text-sm text-gray-700 dark:text-gray-300">Faol</label>
          </div>
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="form.is_featured" id="p_featured" class="w-4 h-4 accent-primary-500" />
            <label for="p_featured" class="text-sm text-gray-700 dark:text-gray-300">Tanlangan</label>
          </div>
          <AppInput v-model="form.order" type="number" label="" placeholder="Tartib" class="w-24" />
        </div>
      </form>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showModal = false">Bekor</AppButton>
          <AppButton :loading="saving" type="submit" form="project-form">Saqlash</AppButton>
        </div>
      </template>
    </AppModal>

    <AppModal :open="showConfirm" title="O'chirishni tasdiqlash" size="sm" @close="showConfirm = false">
      <p class="text-gray-600 dark:text-gray-400"><strong>{{ deleteTarget?.title }}</strong> loyihasini o'chirishni tasdiqlaysizmi?</p>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" @click="showConfirm = false">Bekor</AppButton>
          <AppButton variant="danger" @click="confirmDelete">O'chirish</AppButton>
        </div>
      </template>
    </AppModal>
  </div>
</template>
