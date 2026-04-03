<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { servicesApi } from '@/api/services'
import { useApi } from '@/composables/useApi'
import { SERVICE_ICONS, SERVICE_ICON_OPTIONS } from '@/utils/serviceIcons'
import AppTable from '@/components/ui/AppTable.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import type { Service } from '@/types'

const { list, loading, fetch, create, update, remove } = useApi<Service>()
const showModal = ref(false)
const showConfirm = ref(false)
const editing = ref<Service | null>(null)
const deleteTarget = ref<Service | null>(null)
const saving = ref(false)

const form = reactive({ title: '', short_description: '', description: '', icon: '', order: 0, is_active: true })

const columns = [
  { key: 'icon', label: 'Icon', class: 'w-16' },
  { key: 'title', label: 'Sarlavha' },
  { key: 'order', label: 'Tartib', class: 'w-24' },
  { key: 'status', label: 'Holat', class: 'w-28' },
  { key: 'actions', label: '', class: 'w-24' },
]

function openCreate() {
  editing.value = null
  Object.assign(form, { title: '', short_description: '', description: '', icon: '', order: 0, is_active: true })
  showModal.value = true
}

function openEdit(svc: Service) {
  editing.value = svc
  Object.assign(form, { title: svc.title, short_description: svc.short_description, description: svc.description, icon: svc.icon || '', order: svc.order, is_active: svc.is_active })
  showModal.value = true
}

async function save() {
  saving.value = true
  try {
    if (editing.value) {
      await update(() => servicesApi.update(editing.value!.id, form))
    } else {
      await create(() => servicesApi.create(form))
    }
    showModal.value = false
    await fetch(() => servicesApi.adminList())
  } catch { /* handled */ } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  await remove(() => servicesApi.delete(deleteTarget.value!.id))
  showConfirm.value = false
  await fetch(() => servicesApi.adminList())
}

onMounted(() => fetch(() => servicesApi.adminList()))
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Xizmatlar</h1>
      <AppButton @click="openCreate" size="sm">
        <Plus class="w-4 h-4" /> Qo'shish
      </AppButton>
    </div>

    <AppTable :columns="columns" :loading="loading">
      <tr v-for="svc in list" :key="svc.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
        <td class="px-4 py-3">
          <div class="w-8 h-8 rounded-lg bg-primary-500/10 flex items-center justify-center">
            <component :is="SERVICE_ICONS[svc.icon] || SERVICE_ICONS['Zap']" class="w-4 h-4 text-primary-500" />
          </div>
        </td>
        <td class="px-4 py-3">
          <p class="font-medium text-gray-900 dark:text-white">{{ svc.title }}</p>
          <p class="text-xs text-gray-400 truncate max-w-xs">{{ svc.short_description }}</p>
        </td>
        <td class="px-4 py-3 text-sm text-gray-500">{{ svc.order }}</td>
        <td class="px-4 py-3">
          <AppBadge :variant="svc.is_active ? 'success' : 'gray'">{{ svc.is_active ? 'Faol' : 'Nofaol' }}</AppBadge>
        </td>
        <td class="px-4 py-3">
          <div class="flex gap-1">
            <button @click="openEdit(svc)" class="p-1.5 rounded-lg hover:bg-primary-500/10 text-gray-400 hover:text-primary-500 transition-colors">
              <Pencil class="w-4 h-4" />
            </button>
            <button @click="() => { deleteTarget.value = svc; showConfirm = true }" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors">
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </td>
      </tr>
    </AppTable>

    <!-- Form modal -->
    <AppModal :open="showModal" :title="editing ? 'Xizmatni tahrirlash' : 'Yangi xizmat'" @close="showModal = false">
      <form id="service-form" @submit.prevent="save" class="space-y-4">
        <AppInput v-model="form.title" label="Sarlavha" required />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Icon</label>
          <div class="grid grid-cols-4 gap-2">
            <button
              v-for="opt in SERVICE_ICON_OPTIONS"
              :key="opt.value"
              type="button"
              @click="form.icon = opt.value"
              :class="[
                'flex flex-col items-center gap-1 p-2 rounded-xl border-2 transition-all text-xs',
                form.icon === opt.value
                  ? 'border-primary-500 bg-primary-500/10 text-primary-500'
                  : 'border-gray-200 dark:border-gray-700 hover:border-primary-500/50 text-gray-500',
              ]"
            >
              <component :is="SERVICE_ICONS[opt.value]" class="w-5 h-5" />
              {{ opt.label }}
            </button>
          </div>
        </div>
        <AppInput v-model="form.short_description" label="Qisqa tavsif" required />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">To'liq tavsif</label>
          <textarea v-model="form.description" rows="4" class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="form.order" type="number" label="Tartib" />
          <div class="flex items-center gap-3 pt-6">
            <input type="checkbox" v-model="form.is_active" id="is_active" class="w-4 h-4 accent-primary-500 rounded" />
            <label for="is_active" class="text-sm font-medium text-gray-700 dark:text-gray-300">Faol</label>
          </div>
        </div>
      </form>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showModal = false">Bekor</AppButton>
          <AppButton :loading="saving" type="submit" form="service-form">Saqlash</AppButton>
        </div>
      </template>
    </AppModal>

    <!-- Confirm delete -->
    <AppModal :open="showConfirm" title="O'chirishni tasdiqlash" size="sm" @close="showConfirm = false">
      <p class="text-gray-600 dark:text-gray-400">
        <strong>{{ deleteTarget?.title }}</strong> xizmatini o'chirishni tasdiqlaysizmi?
      </p>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showConfirm = false">Bekor</AppButton>
          <AppButton variant="danger" type="button" @click="confirmDelete">O'chirish</AppButton>
        </div>
      </template>
    </AppModal>
  </div>
</template>
