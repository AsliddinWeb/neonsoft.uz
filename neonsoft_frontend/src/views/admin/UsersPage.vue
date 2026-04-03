<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { UserPlus, Trash2, ShieldCheck, ShieldOff } from 'lucide-vue-next'
import { usersApi } from '@/api/users'
import { useToast } from 'vue-toastification'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import type { User } from '@/types'

const toast = useToast()
const users = ref<User[]>([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)

const form = reactive({ full_name: '', email: '', password: '', role: 'admin' })

onMounted(fetchUsers)

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await usersApi.list()
    users.value = data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  Object.assign(form, { full_name: '', email: '', password: '', role: 'admin' })
  showModal.value = true
}

async function create() {
  saving.value = true
  try {
    const { data } = await usersApi.create(form)
    users.value.unshift(data)
    showModal.value = false
    toast.success('Foydalanuvchi yaratildi')
  } catch { /* handled */ } finally {
    saving.value = false
  }
}

async function toggleActive(user: User) {
  try {
    const { data } = await usersApi.update(user.id, { is_active: !user.is_active })
    const idx = users.value.findIndex(u => u.id === user.id)
    if (idx !== -1) users.value[idx] = data
    toast.success(data.is_active ? 'Faollashtirildi' : 'Bloklandi')
  } catch { /* handled */ }
}

async function remove(user: User) {
  if (!confirm(`"${user.full_name}" ni o'chirishni tasdiqlaysizmi?`)) return
  try {
    await usersApi.delete(user.id)
    users.value = users.value.filter(u => u.id !== user.id)
    toast.success("O'chirildi")
  } catch { /* handled */ }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Foydalanuvchilar</h1>
      <AppButton @click="openCreate" size="sm">
        <UserPlus class="w-4 h-4" />
        Yangi
      </AppButton>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="animate-pulse space-y-3">
      <div v-for="i in 4" :key="i" class="skeleton h-16 rounded-xl" />
    </div>

    <!-- Table -->
    <div v-else class="card overflow-hidden p-0">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
          <tr>
            <th class="text-left px-5 py-3.5 font-medium text-gray-500 dark:text-gray-400">Foydalanuvchi</th>
            <th class="text-left px-5 py-3.5 font-medium text-gray-500 dark:text-gray-400">Email</th>
            <th class="text-left px-5 py-3.5 font-medium text-gray-500 dark:text-gray-400">Rol</th>
            <th class="text-left px-5 py-3.5 font-medium text-gray-500 dark:text-gray-400">Holat</th>
            <th class="px-5 py-3.5" />
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">
            <td class="px-5 py-4">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-primary-500/10 flex items-center justify-center text-primary-500 font-bold text-sm shrink-0">
                  {{ user.full_name?.[0]?.toUpperCase() || 'A' }}
                </div>
                <span class="font-medium text-gray-900 dark:text-white">{{ user.full_name }}</span>
              </div>
            </td>
            <td class="px-5 py-4 text-gray-500 dark:text-gray-400">{{ user.email }}</td>
            <td class="px-5 py-4">
              <AppBadge :variant="user.role === 'superadmin' ? 'primary' : 'default'">
                {{ user.role }}
              </AppBadge>
            </td>
            <td class="px-5 py-4">
              <AppBadge :variant="user.is_active ? 'success' : 'danger'">
                {{ user.is_active ? 'Faol' : 'Bloklangan' }}
              </AppBadge>
            </td>
            <td class="px-5 py-4">
              <div class="flex items-center gap-2 justify-end">
                <button
                  @click="toggleActive(user)"
                  :title="user.is_active ? 'Bloklash' : 'Faollashtirish'"
                  class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 hover:text-primary-500 transition-colors"
                >
                  <ShieldOff v-if="user.is_active" class="w-4 h-4" />
                  <ShieldCheck v-else class="w-4 h-4" />
                </button>
                <button
                  v-if="user.role !== 'superadmin'"
                  @click="remove(user)"
                  class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="5" class="px-5 py-12 text-center text-gray-400">Foydalanuvchilar yo'q</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Modal -->
    <AppModal :open="showModal" title="Yangi foydalanuvchi" @close="showModal = false">
      <form @submit.prevent="create" class="space-y-4">
        <AppInput v-model="form.full_name" label="Ism familiya" required />
        <AppInput v-model="form.email" type="email" label="Email" required />
        <AppInput v-model="form.password" type="password" label="Parol" required />
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Rol</label>
          <select v-model="form.role" class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option value="admin">Admin</option>
            <option value="superadmin">Superadmin</option>
          </select>
        </div>
        <div class="flex gap-3 justify-end pt-2">
          <AppButton type="button" variant="outline" @click="showModal = false">Bekor</AppButton>
          <AppButton type="submit" :loading="saving">Saqlash</AppButton>
        </div>
      </form>
    </AppModal>
  </div>
</template>
