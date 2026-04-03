<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { Plus, Pencil, Trash2, Eye } from 'lucide-vue-next'
import { blogApi } from '@/api/blog'
import { uploadApi } from '@/api/upload'
import { mediaUrl } from '@/utils/media'
import { useApi } from '@/composables/useApi'
import AppTable from '@/components/ui/AppTable.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import type { BlogPost } from '@/types'

const { list, loading, fetch, create, update, remove } = useApi<BlogPost>()
const showModal = ref(false)
const showConfirm = ref(false)
const editing = ref<BlogPost | null>(null)
const deleteTarget = ref<BlogPost | null>(null)
const saving = ref(false)
const uploading = ref(false)
const content = ref('')

const form = reactive({ title: '', excerpt: '', cover_image_url: '', tags: '', is_published: false })

const columns = [
  { key: 'cover', label: '', class: 'w-14' },
  { key: 'title', label: 'Sarlavha' },
  { key: 'views', label: 'Ko\'rishlar', class: 'w-28' },
  { key: 'status', label: 'Holat', class: 'w-28' },
  { key: 'actions', label: '', class: 'w-20' },
]

function openCreate() {
  editing.value = null
  content.value = ''
  Object.assign(form, { title: '', excerpt: '', cover_image_url: '', tags: '', is_published: false })
  showModal.value = true
}

function openEdit(p: BlogPost) {
  editing.value = p
  content.value = p.content
  Object.assign(form, { title: p.title, excerpt: p.excerpt || '', cover_image_url: p.cover_image_url || '', tags: (p.tags || []).join(', '), is_published: p.is_published })
  showModal.value = true
}

async function uploadCover(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { data } = await uploadApi.image(file)
    form.cover_image_url = data.url
  } finally {
    uploading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form, content: content.value, tags: form.tags ? form.tags.split(',').map((t) => t.trim()).filter(Boolean) : [] }
    if (editing.value) {
      await update(() => blogApi.update(editing.value!.id, payload))
    } else {
      await create(() => blogApi.create(payload))
    }
    showModal.value = false
    await fetch(() => blogApi.adminList())
  } catch { /* handled */ } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  await remove(() => blogApi.delete(deleteTarget.value!.id))
  showConfirm.value = false
  await fetch(() => blogApi.adminList())
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('uz-UZ', { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(() => fetch(() => blogApi.adminList()))
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Blog</h1>
      <AppButton @click="openCreate" size="sm"><Plus class="w-4 h-4" /> Yangi maqola</AppButton>
    </div>

    <AppTable :columns="columns" :loading="loading">
      <tr v-for="p in list" :key="p.id" class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
        <td class="px-4 py-3">
          <img v-if="p.cover_image_url" :src="mediaUrl(p.cover_image_url)" class="w-10 h-10 rounded-lg object-cover" />
          <div v-else class="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">📝</div>
        </td>
        <td class="px-4 py-3">
          <p class="font-medium text-gray-900 dark:text-white line-clamp-1">{{ p.title }}</p>
          <p class="text-xs text-gray-400">{{ formatDate(p.created_at) }}</p>
        </td>
        <td class="px-4 py-3">
          <span class="flex items-center gap-1 text-sm text-gray-500"><Eye class="w-3 h-3" />{{ p.views }}</span>
        </td>
        <td class="px-4 py-3"><AppBadge :variant="p.is_published ? 'success' : 'warning'">{{ p.is_published ? 'Nashr' : 'Qoralama' }}</AppBadge></td>
        <td class="px-4 py-3">
          <div class="flex gap-1">
            <button @click="openEdit(p)" class="p-1.5 rounded-lg hover:bg-primary-500/10 text-gray-400 hover:text-primary-500 transition-colors"><Pencil class="w-4 h-4" /></button>
            <button @click="() => { deleteTarget.value = p; showConfirm = true }" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors"><Trash2 class="w-4 h-4" /></button>
          </div>
        </td>
      </tr>
    </AppTable>

    <AppModal :open="showModal" :title="editing ? 'Maqolani tahrirlash' : 'Yangi maqola'" size="xl" @close="showModal = false">
      <div class="space-y-4">
        <AppInput v-model="form.title" label="Sarlavha" required />
        <AppInput v-model="form.excerpt" label="Qisqa mazmun" />
        <AppInput v-model="form.tags" label="Teglar (vergul bilan)" placeholder="Vue, FastAPI, Python" />

        <!-- Cover image -->
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Cover rasm</label>
          <div v-if="form.cover_image_url" class="relative h-40 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <img :src="mediaUrl(form.cover_image_url)" class="w-full h-full object-cover" />
            <button type="button" @click="form.cover_image_url = ''" class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded text-xs">✕</button>
          </div>
          <label v-else class="flex items-center justify-center h-24 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl cursor-pointer hover:border-primary-500 transition-colors">
            <span class="text-sm text-gray-400">{{ uploading ? 'Yuklanmoqda...' : 'Cover yuklash' }}</span>
            <input type="file" accept="image/*" @change="uploadCover" class="hidden" :disabled="uploading" />
          </label>
        </div>

        <!-- Quill editor -->
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Mazmun *</label>
          <QuillEditor v-model:content="content" content-type="html" theme="snow"
            :toolbar="['bold', 'italic', 'underline', { list: 'ordered' }, { list: 'bullet' }, 'link', 'image', 'blockquote', 'code-block', { header: [1, 2, 3, false] }]"
            style="min-height: 200px;" />
        </div>

        <div class="flex items-center gap-2">
          <input type="checkbox" v-model="form.is_published" id="b_pub" class="w-4 h-4 accent-primary-500" />
          <label for="b_pub" class="text-sm text-gray-700 dark:text-gray-300">Nashr qilish</label>
        </div>
      </div>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showModal = false">Bekor</AppButton>
          <AppButton :loading="saving" type="button" @click="save">Saqlash</AppButton>
        </div>
      </template>
    </AppModal>

    <AppModal :open="showConfirm" title="O'chirishni tasdiqlash" size="sm" @close="showConfirm = false">
      <p class="text-gray-600 dark:text-gray-400"><strong>{{ deleteTarget?.title }}</strong> maqolasini o'chirishni tasdiqlaysizmi?</p>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" @click="showConfirm = false">Bekor</AppButton>
          <AppButton variant="danger" @click="confirmDelete">O'chirish</AppButton>
        </div>
      </template>
    </AppModal>
  </div>
</template>
