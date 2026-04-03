<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Hamkorlar</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ partners.length }} ta hamkor</p>
      </div>
      <button @click="openCreate" class="btn-primary flex items-center gap-2">
        <Plus class="w-4 h-4" />Qo'shish
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-16"><AppLoader /></div>

    <div v-else-if="partners.length === 0"
      class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-16 text-center">
      <Handshake class="w-12 h-12 mx-auto text-gray-300 mb-3" />
      <p class="text-gray-500">Hali hamkorlar qo'shilmagan</p>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div v-for="p in partners" :key="p.id"
        class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 flex flex-col items-center gap-3 group">
        <div class="w-20 h-20 rounded-xl overflow-hidden bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
          <img v-if="p.logo_url" :src="mediaUrl(p.logo_url)" :alt="p.name" class="w-full h-full object-contain p-2" />
          <Building2 v-else class="w-8 h-8 text-gray-400" />
        </div>
        <p class="text-sm font-medium text-gray-800 dark:text-gray-200 text-center">{{ p.name }}</p>
        <div class="flex items-center gap-1">
          <span :class="p.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'"
            class="text-xs px-2 py-0.5 rounded-full">
            {{ p.is_active ? 'Aktiv' : 'Noaktiv' }}
          </span>
        </div>
        <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button @click="openEdit(p)" class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
            <Pencil class="w-4 h-4 text-primary-500" />
          </button>
          <button @click="confirmDelete(p.id)" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20">
            <Trash2 class="w-4 h-4 text-red-500" />
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <AppModal :open="showModal" :title="editing ? 'Tahrirlash' : 'Yangi hamkor'" @close="showModal = false">
      <form @submit.prevent="save" class="space-y-4">
        <div>
          <label class="label">Nomi <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" class="input-field" required />
        </div>

        <div>
          <label class="label">Veb-sayt URL</label>
          <input v-model="form.website_url" type="url" class="input-field" placeholder="https://example.com" />
        </div>

        <div>
          <label class="label">Logo</label>
          <div v-if="form.logo_url" class="relative inline-block mb-2">
            <img :src="mediaUrl(form.logo_url)" alt="logo" class="h-20 rounded-xl object-contain border border-gray-200 dark:border-gray-600 p-2 bg-white" />
            <button type="button" @click="form.logo_url = ''"
              class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-0.5">
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
          <div v-else class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-6 text-center cursor-pointer hover:border-primary-500 transition-colors"
            @click="logoInput?.click()">
            <ImageIcon class="w-8 h-8 mx-auto text-gray-400 mb-1" />
            <p class="text-xs text-gray-500">Logo yuklash</p>
          </div>
          <input ref="logoInput" type="file" accept="image/*" class="hidden" @change="uploadLogo" />
          <div v-if="uploading" class="flex items-center gap-2 text-sm text-primary-500 mt-1">
            <AppLoader size="sm" /> Yuklanmoqda...
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Tartib</label>
            <input v-model.number="form.order" type="number" min="0" class="input-field" />
          </div>
          <div class="flex items-end pb-1">
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="form.is_active" type="checkbox" class="w-4 h-4 accent-primary-500" />
              <span class="text-sm text-gray-700 dark:text-gray-300">Aktiv</span>
            </label>
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button type="button" @click="showModal = false" class="btn-outline">Bekor</button>
          <button type="submit" :disabled="saving" class="btn-primary">
            {{ saving ? 'Saqlanmoqda...' : 'Saqlash' }}
          </button>
        </div>
      </form>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { Plus, Pencil, Trash2, X, Image as ImageIcon, Handshake, Building2 } from 'lucide-vue-next'
import { partnersApi, type Partner } from '@/api/partners'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import AppModal from '@/components/ui/AppModal.vue'
import AppLoader from '@/components/ui/AppLoader.vue'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const showModal = ref(false)
const editing = ref<Partner | null>(null)
const partners = ref<Partner[]>([])
const logoInput = ref<HTMLInputElement>()

const emptyForm = () => ({ name: '', logo_url: '', website_url: '', order: 0, is_active: true })
const form = ref(emptyForm())

onMounted(load)

async function load() {
  loading.value = true
  try { partners.value = await partnersApi.adminList() }
  finally { loading.value = false }
}

function openCreate() {
  editing.value = null
  form.value = emptyForm()
  showModal.value = true
}

function openEdit(p: Partner) {
  editing.value = p
  form.value = { name: p.name, logo_url: p.logo_url || '', website_url: p.website_url || '', order: p.order, is_active: p.is_active }
  showModal.value = true
}

async function uploadLogo(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try { const res = await (await uploadApi.image(file)).data; form.value.logo_url = res.url }
  catch { toast.error('Logo yuklashda xato') }
  finally { uploading.value = false }
}

async function save() {
  saving.value = true
  try {
    if (editing.value) {
      await partnersApi.update(editing.value.id, form.value)
      toast.success('Yangilandi!')
    } else {
      await partnersApi.create(form.value)
      toast.success('Qo\'shildi!')
    }
    showModal.value = false
    await load()
  } catch { toast.error('Xato yuz berdi') }
  finally { saving.value = false }
}

async function confirmDelete(id: number) {
  if (!confirm('O\'chirishni tasdiqlaysizmi?')) return
  try {
    await partnersApi.remove(id)
    toast.success('O\'chirildi!')
    await load()
  } catch { toast.error('Xato yuz berdi') }
}
</script>

<style scoped>
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input-field {
  @apply w-full px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-600
    bg-white dark:bg-gray-700 text-gray-900 dark:text-white
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
    placeholder-gray-400 transition;
}
</style>