<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Send, Phone } from 'lucide-vue-next'
import { contactApi } from '@/api/contact'
import { useToast } from 'vue-toastification'
import { useSettingsStore } from '@/stores/settings'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'

const toast = useToast()
const store = useSettingsStore()
const loading = ref(false)
const form = reactive({ full_name: '', phone: '', message: '' })

async function submit() {
  loading.value = true
  try {
    await contactApi.send({ ...form, email: '', subject: 'Bosh sahifadan', source: 'contact' })
    toast.success("Xabaringiz yuborildi! Tez orada bog'lanamiz.")
    Object.assign(form, { full_name: '', phone: '', message: '' })
  } catch {
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section id="contact" class="py-28 bg-secondary relative overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/4 left-0 w-96 h-96 bg-primary-500/10 rounded-full blur-[120px]" />
      <div class="absolute bottom-0 right-0 w-80 h-80 bg-accent/5 rounded-full blur-[100px]" />
      <div class="absolute inset-0 bg-[linear-gradient(rgba(0,212,170,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(0,212,170,0.02)_1px,transparent_1px)] bg-[size:48px_48px]" />
    </div>

    <div class="container mx-auto px-4 sm:px-6 lg:px-8 relative">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <!-- Left: Text -->
        <div>
          <span class="inline-flex items-center gap-2 text-primary-400 text-sm font-semibold uppercase tracking-widest mb-4">
            <span class="w-8 h-px bg-primary-500" /> Aloqa
          </span>
          <h2 class="font-display font-bold text-4xl lg:text-5xl text-white leading-tight mb-6">
            Keyingi loyiha
            <span class="gradient-text">sizniki bo'lsin</span>
          </h2>
          <p class="text-gray-400 text-lg leading-relaxed mb-8">
            Birinchi konsultatsiya bepul. Loyihangiz haqida yozing yoki qo'ng'iroq qiling — 24 soat ichida javob beramiz.
          </p>

          <!-- Phone CTA -->
          <a
            v-if="store.settings?.phone"
            :href="`tel:${store.settings.phone}`"
            class="inline-flex items-center gap-4 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-primary-500/30 rounded-2xl p-5 transition-all duration-300 group"
          >
            <div class="w-12 h-12 rounded-xl bg-primary-500/15 flex items-center justify-center group-hover:bg-primary-500/25 transition-colors">
              <Phone class="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p class="text-xs text-gray-500 mb-0.5">Bizga qo'ng'iroq qiling</p>
              <p class="text-white font-semibold text-lg">{{ store.settings.phone }}</p>
            </div>
          </a>
        </div>

        <!-- Right: Form -->
        <div class="bg-white dark:bg-surface rounded-3xl border border-gray-100 dark:border-gray-800 p-8 shadow-2xl shadow-black/5 dark:shadow-black/20">
          <h3 class="font-display font-semibold text-xl text-gray-900 dark:text-white mb-6">Xabar qoldiring</h3>
          <form @submit.prevent="submit" class="space-y-4">
            <AppInput v-model="form.full_name" label="Ism familiya" placeholder="Sardor Abdullayev" required />
            <AppInput v-model="form.phone" label="Telefon raqam" placeholder="+998 90 000 00 00" required />
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Xabar <span class="text-red-500">*</span></label>
              <textarea
                v-model="form.message"
                rows="4"
                required
                placeholder="Loyihangiz haqida qisqacha..."
                class="w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
              />
            </div>
            <AppButton type="submit" :loading="loading" size="lg" class="w-full">
              <Send class="w-4 h-4" />
              Yuborish
            </AppButton>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>
