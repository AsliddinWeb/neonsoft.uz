<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { teamApi } from '@/api/team'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import { useApi } from '@/composables/useApi'
import AppTable from '@/components/ui/AppTable.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import type { TeamMember } from '@/types'

const { list, loading, fetch, create, update, remove } = useApi<TeamMember>()
const showModal = ref(false)
const showConfirm = ref(false)
const editing = ref<TeamMember | null>(null)
const deleteTarget = ref<TeamMember | null>(null)
const saving = ref(false)
const uploading = ref(false)

const form = reactive({ full_name: '', position: '', bio: '', photo_url: '', linkedin_url: '', github_url: '', telegram_url: '', order: 0, is_active: true })

const columns = [
  { key: 'photo', label: '', class: 'w-14' },
  { key: 'name', label: 'Ism' },
  { key: 'position', label: 'Lavozim' },
  { key: 'status', label: 'Holat', class: 'w-24' },
  { key: 'actions', label: '', class: 'w-20' },
]

function openCreate() {
  editing.value = null
  Object.assign(form, { full_name: '', position: '', bio: '', photo_url: '', linkedin_url: '', github_url: '', telegram_url: '', order: 0, is_active: true })
  showModal.value = true
}

function openEdit(m: TeamMember) {
  editing.value = m
  Object.assign(form, { full_name: m.full_name, position: m.position, bio: m.bio || '', photo_url: m.photo_url || '', linkedin_url: m.linkedin_url || '', github_url: m.github_url || '', telegram_url: m.telegram_url || '', order: m.order, is_active: m.is_active })
  showModal.value = true
}

async function uploadPhoto(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { data } = await uploadApi.image(file)
    form.photo_url = data.url
  } finally {
    uploading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    if (editing.value) {
      await update(() => teamApi.update(editing.value!.id, form))
    } else {
      await create(() => teamApi.create(form))
    }
    showModal.value = false
    await fetch(() => teamApi.adminList())
  } catch { /* handled */ } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  await remove(() => teamApi.delete(deleteTarget.value!.id))
  showConfirm.value = false
  await fetch(() => teamApi.adminList())
}

onMounted(() => fetch(() => teamApi.adminList()))
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Jamoa</h1>
      <AppButton @click="openCreate" size="sm"><Plus class="w-4 h-4" /> Qo'shish</AppButton>
    </div>

    <AppTable :columns="columns" :loading="loading">
      <tr v-for="m in list" :key="m.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
        <td class="px-4 py-3">
          <img v-if="m.photo_url" :src="mediaUrl(m.photo_url)" class="w-9 h-9 rounded-full object-cover" />
          <div v-else class="w-9 h-9 rounded-full bg-primary-500/10 flex items-center justify-center text-sm">👤</div>
        </td>
        <td class="px-4 py-3 font-medium text-gray-900 dark:text-white">{{ m.full_name }}</td>
        <td class="px-4 py-3 text-sm text-gray-500">{{ m.position }}</td>
        <td class="px-4 py-3"><AppBadge :variant="m.is_active ? 'success' : 'gray'">{{ m.is_active ? 'Faol' : 'Nofaol' }}</AppBadge></td>
        <td class="px-4 py-3">
          <div class="flex gap-1">
            <button @click="openEdit(m)" class="p-1.5 rounded-lg hover:bg-primary-500/10 text-gray-400 hover:text-primary-500 transition-colors"><Pencil class="w-4 h-4" /></button>
            <button @click="() => { deleteTarget.value = m; showConfirm = true }" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors"><Trash2 class="w-4 h-4" /></button>
          </div>
        </td>
      </tr>
    </AppTable>

    <AppModal :open="showModal" :title="editing ? 'Tahrirlash' : 'Yangi a\'zo'" size="lg" @close="showModal = false">
      <form id="team-form" @submit.prevent="save" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="form.full_name" label="Ism familiya" required />
          <AppInput v-model="form.position" label="Lavozim" required />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Bio</label>
          <textarea v-model="form.bio" rows="3" class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="form.linkedin_url" label="LinkedIn URL" />
          <AppInput v-model="form.github_url" label="GitHub URL" />
        </div>
        <AppInput v-model="form.telegram_url" label="Telegram URL" />

        <!-- Photo upload -->
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Foto</label>
          <div v-if="form.photo_url" class="flex items-center gap-3">
            <img :src="mediaUrl(form.photo_url)" class="w-16 h-16 rounded-full object-cover" />
            <button type="button" @click="form.photo_url = ''" class="text-xs text-red-500 hover:underline">O'chirish</button>
          </div>
          <label v-else class="flex items-center justify-center h-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl cursor-pointer hover:border-primary-500 transition-colors">
            <span class="text-sm text-gray-400">{{ uploading ? 'Yuklanmoqda...' : 'Foto yuklash' }}</span>
            <input type="file" accept="image/*" @change="uploadPhoto" class="hidden" :disabled="uploading" />
          </label>
        </div>

        <div class="flex gap-4 items-center">
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="form.is_active" id="m_active" class="w-4 h-4 accent-primary-500" />
            <label for="m_active" class="text-sm text-gray-700 dark:text-gray-300">Faol</label>
          </div>
          <AppInput v-model="form.order" type="number" label="" placeholder="Tartib" class="w-24" />
        </div>
      </form>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showModal = false">Bekor</AppButton>
          <AppButton :loading="saving" type="submit" form="team-form">Saqlash</AppButton>
        </div>
      </template>
    </AppModal>

    <AppModal :open="showConfirm" title="O'chirishni tasdiqlash" size="sm" @close="showConfirm = false">
      <p class="text-gray-600 dark:text-gray-400"><strong>{{ deleteTarget?.full_name }}</strong> ni o'chirishni tasdiqlaysizmi?</p>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" @click="showConfirm = false">Bekor</AppButton>
          <AppButton variant="danger" @click="confirmDelete">O'chirish</AppButton>
        </div>
      </template>
    </AppModal>
  </div>
</template>
