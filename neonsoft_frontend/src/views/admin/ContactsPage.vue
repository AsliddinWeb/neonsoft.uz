<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { Check, Trash2, Phone, MessageSquare, Layers } from 'lucide-vue-next'
import { contactApi } from '@/api/contact'
import { useApi } from '@/composables/useApi'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import type { ContactMessage } from '@/types'

const { list, loading, fetch, remove } = useApi<ContactMessage>()
const showDetail = ref(false)
const showConfirm = ref(false)
const selected = ref<ContactMessage | null>(null)
const marking = ref(false)

// Xizmat so'rovi: email bo'sh yoki yo'q, subject bor
function isServiceRequest(msg: ContactMessage) {
  return msg.source === 'service'
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('uz-UZ', { year: 'numeric', month: 'short', day: 'numeric' })
}

function open(msg: ContactMessage) {
  selected.value = msg
  showDetail.value = true
  if (!msg.is_read) markRead(msg)
}

async function markRead(msg: ContactMessage) {
  if (msg.is_read) return
  marking.value = true
  try {
    await contactApi.markRead(msg.id)
    msg.is_read = true
  } finally {
    marking.value = false
  }
}

async function confirmDelete() {
  if (!selected.value) return
  await remove(() => contactApi.delete(selected.value!.id))
  showConfirm.value = false
  showDetail.value = false
  await fetch(() => contactApi.adminList({ limit: 50 }))
}

onMounted(() => fetch(() => contactApi.adminList({ limit: 50 })))
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Xabarlar</h1>
      <div class="flex items-center gap-3 text-sm text-gray-500">
        <span class="flex items-center gap-1.5">
          <div class="w-2 h-2 rounded-full bg-primary-500" />
          O'qilmagan
        </span>
        <span class="flex items-center gap-1.5">
          <Layers class="w-3.5 h-3.5 text-accent" /> Xizmat so'rovi
        </span>
        <span class="flex items-center gap-1.5">
          <MessageSquare class="w-3.5 h-3.5 text-blue-500" /> Oddiy xabar
        </span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="animate-pulse space-y-2">
      <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-xl" />
    </div>

    <!-- Table -->
    <div v-else class="card overflow-hidden p-0">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
          <tr>
            <th class="w-3 px-4 py-3" />
            <th class="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400">Tur</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400">Ism</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400">Telefon</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400">Mavzu / Xabar</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400 w-28">Sana</th>
            <th class="w-20 px-4 py-3" />
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr
            v-for="msg in list"
            :key="msg.id"
            @click="open(msg)"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/30 cursor-pointer transition-colors"
            :class="{ 'bg-primary-500/3': !msg.is_read }"
          >
            <!-- Unread dot -->
            <td class="px-4 py-3.5">
              <div :class="['w-2 h-2 rounded-full', !msg.is_read ? 'bg-primary-500' : 'bg-transparent']" />
            </td>

            <!-- Type badge -->
            <td class="px-4 py-3.5">
              <div v-if="isServiceRequest(msg)" class="flex items-center gap-1.5 text-accent text-xs font-medium">
                <Layers class="w-3.5 h-3.5" />
                Xizmat
              </div>
              <div v-else class="flex items-center gap-1.5 text-blue-500 text-xs font-medium">
                <MessageSquare class="w-3.5 h-3.5" />
                Xabar
              </div>
            </td>

            <!-- Name -->
            <td class="px-4 py-3.5">
              <p :class="['text-gray-900 dark:text-white', !msg.is_read ? 'font-semibold' : 'font-medium']">
                {{ msg.full_name }}
              </p>
            </td>

            <!-- Phone -->
            <td class="px-4 py-3.5">
              <a v-if="msg.phone" :href="`tel:${msg.phone}`" @click.stop
                class="flex items-center gap-1.5 text-gray-500 hover:text-primary-500 transition-colors">
                <Phone class="w-3.5 h-3.5" />
                {{ msg.phone }}
              </a>
              <span v-else class="text-gray-300 dark:text-gray-600">—</span>
            </td>

            <!-- Subject + message preview -->
            <td class="px-4 py-3.5 max-w-xs">
              <p v-if="msg.subject" class="text-gray-900 dark:text-white font-medium text-xs mb-0.5">
                {{ msg.subject }}
              </p>
              <p class="text-gray-400 text-xs truncate">{{ msg.message }}</p>
            </td>

            <!-- Date -->
            <td class="px-4 py-3.5 text-xs text-gray-400 whitespace-nowrap">
              {{ formatDate(msg.created_at) }}
            </td>

            <!-- Actions -->
            <td class="px-4 py-3.5" @click.stop>
              <div class="flex items-center gap-1">
                <button v-if="!msg.is_read" @click="markRead(msg)"
                  class="p-1.5 rounded-lg hover:bg-primary-500/10 text-gray-400 hover:text-primary-500 transition-colors"
                  title="O'qildi deb belgilash">
                  <Check class="w-4 h-4" />
                </button>
                <button @click="() => { selected.value = msg; showConfirm = true }"
                  class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="list.length === 0">
            <td colspan="7" class="px-4 py-16 text-center text-gray-400">Xabarlar yo'q</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail modal -->
    <AppModal :open="showDetail && !!selected" :title="selected?.full_name" @close="showDetail = false">
      <div v-if="selected" class="space-y-5 text-sm">

        <!-- Type -->
        <div class="flex items-center gap-2">
          <div v-if="isServiceRequest(selected)"
            class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-accent/10 text-accent text-xs font-medium">
            <Layers class="w-3.5 h-3.5" /> Xizmat so'rovi
          </div>
          <div v-else
            class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-blue-500/10 text-blue-500 text-xs font-medium">
            <MessageSquare class="w-3.5 h-3.5" /> Oddiy xabar
          </div>
          <span class="text-xs text-gray-400">{{ formatDate(selected.created_at) }}</span>
        </div>

        <!-- Contact info -->
        <div class="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
          <div>
            <p class="text-xs text-gray-400 mb-1">Ism familiya</p>
            <p class="font-medium text-gray-900 dark:text-white">{{ selected.full_name }}</p>
          </div>
          <div v-if="selected.phone">
            <p class="text-xs text-gray-400 mb-1">Telefon</p>
            <a :href="`tel:${selected.phone}`"
              class="font-medium text-primary-500 hover:underline flex items-center gap-1.5">
              <Phone class="w-3.5 h-3.5" /> {{ selected.phone }}
            </a>
          </div>
        </div>

        <!-- Subject (service name) -->
        <div v-if="selected.subject"
          class="p-4 rounded-xl border-l-4 border-primary-500 bg-primary-500/5">
          <p class="text-xs text-gray-400 mb-1">{{ isServiceRequest(selected) ? 'So\'ralgan xizmat' : 'Mavzu' }}</p>
          <p class="font-semibold text-gray-900 dark:text-white">{{ selected.subject }}</p>
        </div>

        <!-- Message -->
        <div>
          <p class="text-xs text-gray-400 mb-2">{{ isServiceRequest(selected) ? 'Loyiha tavsifi' : 'Xabar' }}</p>
          <p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4">
            {{ selected.message }}
          </p>
        </div>
      </div>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showDetail = false">Yopish</AppButton>
          <AppButton variant="danger" size="sm" type="button" @click="showConfirm = true">
            <Trash2 class="w-4 h-4" /> O'chirish
          </AppButton>
        </div>
      </template>
    </AppModal>

    <!-- Confirm delete -->
    <AppModal :open="showConfirm" title="O'chirishni tasdiqlash" size="sm" @close="showConfirm = false">
      <p class="text-gray-600 dark:text-gray-400">Bu xabarni o'chirishni tasdiqlaysizmi?</p>
      <template #footer>
        <div class="flex gap-3 justify-end">
          <AppButton variant="ghost" type="button" @click="showConfirm = false">Bekor</AppButton>
          <AppButton variant="danger" type="button" @click="confirmDelete">O'chirish</AppButton>
        </div>
      </template>
    </AppModal>
  </div>
</template>
