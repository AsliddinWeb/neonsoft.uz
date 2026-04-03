<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Send, CheckCircle2 } from 'lucide-vue-next'
import { contactApi } from '@/api/contact'
import { servicesApi } from '@/api/services'
import { useToast } from 'vue-toastification'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import { SERVICE_ICONS } from '@/utils/serviceIcons'
import type { Service } from '@/types'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const loading = ref(false)
const submitted = ref(false)
const services = ref<Service[]>([])
const selectedId = ref<number | null>(null)

const form = reactive({ full_name: '', phone: '', message: '' })

const selectedService = computed(() =>
  services.value.find(s => s.id === selectedId.value) || null
)

onMounted(async () => {
  try {
    const { data } = await servicesApi.list()
    services.value = data
    const id = Number(route.query.id)
    if (id && data.find(s => s.id === id)) {
      selectedId.value = id
    } else if (data.length) {
      selectedId.value = data[0].id
    }
  } catch {}
})

async function submit() {
  if (!form.full_name || !form.phone || !form.message) {
    toast.error("Iltimos, barcha maydonlarni to'ldiring")
    return
  }
  loading.value = true
  try {
    await contactApi.send({
      full_name: form.full_name,
      email: '',
      phone: form.phone,
      subject: selectedService.value?.title || 'Xizmat so\'rovi',
      message: form.message,
      source: 'service',
    })
    submitted.value = true
  } catch {} finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-secondary pt-32 pb-20">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-2xl">

      <!-- Back -->
      <button @click="router.back()" class="flex items-center gap-2 text-gray-500 hover:text-primary-500 transition-colors mb-8 text-sm">
        <ArrowLeft class="w-4 h-4" /> Ortga
      </button>

      <!-- Success state -->
      <div v-if="submitted" class="text-center py-16 space-y-4">
        <div class="w-20 h-20 rounded-full bg-primary-500/10 flex items-center justify-center mx-auto">
          <CheckCircle2 class="w-10 h-10 text-primary-500" />
        </div>
        <h2 class="font-display font-bold text-2xl text-gray-900 dark:text-white">Rahmat! So'rovingiz qabul qilindi</h2>
        <p class="text-gray-500 dark:text-gray-400">Mutaxassisimiz 24 soat ichida siz bilan bog'lanadi.</p>
        <button @click="router.push('/')" class="btn-primary mt-4">Bosh sahifaga</button>
      </div>

      <!-- Form -->
      <div v-else class="space-y-6">
        <div>
          <h1 class="font-display font-bold text-3xl text-gray-900 dark:text-white">Buyurtma berish</h1>
          <p class="text-gray-500 dark:text-gray-400 mt-2">Kerakli xizmatni tanlang, qolganini biz hal qilamiz</p>
        </div>

        <!-- Service picker -->
        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="svc in services"
            :key="svc.id"
            type="button"
            @click="selectedId = svc.id"
            :class="[
              'flex items-center gap-3 p-4 rounded-2xl border-2 text-left transition-all',
              selectedId === svc.id
                ? 'border-primary-500 bg-primary-500/5 text-primary-600 dark:text-primary-400'
                : 'border-gray-200 dark:border-gray-700 hover:border-primary-500/50 text-gray-700 dark:text-gray-300',
            ]"
          >
            <component
              :is="SERVICE_ICONS[svc.icon] || SERVICE_ICONS['Zap']"
              class="w-5 h-5 shrink-0"
            />
            <span class="text-sm font-medium leading-tight">{{ svc.title }}</span>
          </button>
        </div>

        <!-- Fields -->
        <div class="bg-white dark:bg-surface rounded-2xl border border-gray-100 dark:border-gray-800 p-6 space-y-4">
          <AppInput v-model="form.full_name" label="Ism familiya" placeholder="Abdullayev Sardor" required />
          <AppInput v-model="form.phone" label="Telefon raqam" placeholder="+998 90 000 00 00" required />
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
              Loyiha haqida qisqacha <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="form.message"
              rows="4"
              placeholder="Loyihangiz haqida qisqacha: nima kerak, qachongacha..."
              class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none transition-colors"
            />
          </div>
          <AppButton @click="submit" :loading="loading" size="lg" class="w-full">
            <Send class="w-4 h-4" />
            Yuborish
          </AppButton>
        </div>
      </div>

    </div>
  </div>
</template>
