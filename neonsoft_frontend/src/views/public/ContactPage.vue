<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Send, Mail, Phone, MapPin } from 'lucide-vue-next'
import { contactApi } from '@/api/contact'
import { useToast } from 'vue-toastification'
import { useSeo } from '@/composables/useSeo'
import { useSettingsStore } from '@/stores/settings'
import PageHeader from '@/components/public/PageHeader.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'

useSeo({ title: 'Aloqa' })
const toast = useToast()
const store = useSettingsStore()
const loading = ref(false)
const form = reactive({ full_name: '', phone: '', subject: '', message: '' })

async function submit() {
  loading.value = true
  try {
    await contactApi.send({ ...form, email: '' })
    toast.success("Xabaringiz yuborildi!")
    Object.assign(form, { full_name: '', phone: '', subject: '', message: '' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <PageHeader label="Aloqa" title="Loyihangizni boshlaylik" description="Bizga yozing yoki qo'ng'iroq qiling — 24 soat ichida javob beramiz" />
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-16">

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <!-- Contact info -->
        <div class="space-y-6">
          <div v-if="store.settings?.email" class="flex items-start gap-4">
            <div class="w-11 h-11 rounded-xl bg-primary-500/10 flex items-center justify-center shrink-0">
              <Mail class="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Email</p>
              <a :href="`mailto:${store.settings.email}`" class="font-medium text-gray-900 dark:text-white hover:text-primary-500 transition-colors">
                {{ store.settings.email }}
              </a>
            </div>
          </div>
          <div v-if="store.settings?.phone" class="flex items-start gap-4">
            <div class="w-11 h-11 rounded-xl bg-primary-500/10 flex items-center justify-center shrink-0">
              <Phone class="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Telefon</p>
              <a :href="`tel:${store.settings.phone}`" class="font-medium text-gray-900 dark:text-white hover:text-primary-500 transition-colors">
                {{ store.settings.phone }}
              </a>
            </div>
          </div>
          <div v-if="store.settings?.address" class="flex items-start gap-4">
            <div class="w-11 h-11 rounded-xl bg-primary-500/10 flex items-center justify-center shrink-0">
              <MapPin class="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Manzil</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ store.settings.address }}</p>
            </div>
          </div>

          <!-- Map placeholder -->
          <div class="rounded-2xl bg-gray-100 dark:bg-gray-800 h-48 flex items-center justify-center text-gray-400 text-sm mt-6">
            📍 Xarita
          </div>
        </div>

        <!-- Form -->
        <div class="lg:col-span-2">
          <form @submit.prevent="submit" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <AppInput v-model="form.full_name" label="Ism familiya" placeholder="Sardor Abdullayev" required />
              <AppInput v-model="form.phone" label="Telefon raqam" placeholder="+998 90 000 00 00" required />
            </div>
            <div>
              <AppInput v-model="form.subject" label="Mavzu" placeholder="Loyiha haqida" />
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Xabar <span class="text-red-500">*</span></label>
              <textarea v-model="form.message" rows="6" required placeholder="Xabaringizni yozing..."
                class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none" />
            </div>
            <AppButton type="submit" :loading="loading" size="lg">
              <Send class="w-4 h-4" /> Yuborish
            </AppButton>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
