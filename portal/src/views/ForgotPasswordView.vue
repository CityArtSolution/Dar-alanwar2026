<template>
  <div class="min-h-screen flex items-center justify-center bg-light p-6" dir="rtl">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-primary rounded-2xl mx-auto flex items-center justify-center mb-4">
          <span class="text-3xl font-bold text-white">د</span>
        </div>
        <h1 class="text-xl font-bold text-dark">أكاديمية دار الأنوار</h1>
      </div>

      <div class="card">
        <template v-if="!submitted">
          <h2 class="text-xl font-bold text-dark mb-2">نسيت كلمة المرور؟</h2>
          <p class="text-gray-500 text-sm mb-6">أدخل رقم هاتفك المسجل وسنرسل لك تعليمات إعادة التعيين</p>

          <!-- Error -->
          <div v-if="error"
               class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
            {{ error }}
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">رقم الهاتف</label>
              <div class="relative">
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                </span>
                <input
                  v-model="phone"
                  type="tel"
                  class="input-field pr-10"
                  placeholder="05xxxxxxxx"
                  required
                />
              </div>
            </div>

            <button type="submit" :disabled="loading"
                    class="btn-primary w-full flex items-center justify-center gap-2 py-3">
              <svg v-if="loading" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              <span>{{ loading ? 'جاري الإرسال...' : 'إرسال رابط الاستعادة' }}</span>
            </button>
          </form>
        </template>

        <!-- Success State -->
        <template v-else>
          <div class="text-center py-4">
            <div class="w-16 h-16 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <h3 class="text-lg font-bold text-dark mb-2">تم الإرسال</h3>
            <p class="text-gray-500 text-sm">
              إذا كان الرقم مسجلاً لدينا، ستصلك رسالة تحتوي على تعليمات إعادة تعيين كلمة المرور
            </p>
          </div>
        </template>

        <router-link to="/login"
                     class="flex items-center justify-center gap-2 mt-6 text-sm text-primary hover:underline font-medium">
          <svg class="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          العودة لتسجيل الدخول
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authApi } from '@/services/api'

const phone = ref('')
const loading = ref(false)
const submitted = ref(false)
const error = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  try {
    await authApi.forgotPassword({ phone: phone.value })
  } catch {
    // Show success even on error to avoid phone enumeration
  }
  submitted.value = true
  loading.value = false
}
</script>
