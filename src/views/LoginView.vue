<template>
  <div class="min-h-screen flex" dir="rtl">
    <!-- Right Side — Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary to-secondary relative overflow-hidden items-center justify-center">
      <div class="relative z-10 text-center px-12">
        <div class="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-3xl mx-auto flex items-center justify-center mb-8">
          <span class="text-5xl font-bold text-white">د</span>
        </div>
        <h1 class="text-4xl font-bold text-white mb-4">أكاديمية دار الأنوار</h1>
        <p class="text-white/80 text-lg leading-relaxed max-w-md mx-auto">
          بوابة أولياء الأمور — تابع تقدم أبنائك الدراسي، الحضور، والمدفوعات من مكان واحد
        </p>
      </div>
      <!-- Decorative circles -->
      <div class="absolute top-10 left-10 w-64 h-64 bg-white/5 rounded-full"></div>
      <div class="absolute bottom-20 right-10 w-48 h-48 bg-white/5 rounded-full"></div>
      <div class="absolute top-1/2 left-1/3 w-32 h-32 bg-white/5 rounded-full"></div>
    </div>

    <!-- Left Side — Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 bg-light">
      <div class="w-full max-w-md">
        <!-- Mobile Logo -->
        <div class="lg:hidden text-center mb-8">
          <div class="w-16 h-16 bg-primary rounded-2xl mx-auto flex items-center justify-center mb-4">
            <span class="text-3xl font-bold text-white">د</span>
          </div>
          <h1 class="text-xl font-bold text-dark">أكاديمية دار الأنوار</h1>
        </div>

        <div class="mb-8">
          <h2 class="text-2xl font-bold text-dark">تسجيل الدخول</h2>
          <p class="text-gray-500 mt-1">أدخل بياناتك للوصول إلى حسابك</p>
        </div>

        <!-- Error Alert -->
        <div v-if="authStore.error"
             class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm flex items-center gap-2">
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Phone -->
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
                autocomplete="tel"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">كلمة المرور</label>
            <div class="relative">
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </span>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="input-field pr-10 pl-10"
                placeholder="••••••••"
                required
                autocomplete="current-password"
              />
              <button type="button" @click="showPassword = !showPassword"
                      class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="!showPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Submit -->
          <button type="submit" :disabled="authStore.loading"
                  class="btn-primary w-full flex items-center justify-center gap-2 py-3">
            <svg v-if="authStore.loading" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <span>{{ authStore.loading ? 'جاري الدخول...' : 'تسجيل الدخول' }}</span>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          نسيت كلمة المرور؟
          <router-link to="/forgot-password" class="text-primary hover:underline font-medium">إعادة تعيين</router-link>
        </p>

        <p class="text-center text-gray-400 text-xs mt-8">
          Dar Al-Anwar Academy &copy; {{ new Date().getFullYear() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const phone = ref('')
const password = ref('')
const showPassword = ref(false)

async function handleLogin() {
  const credentials = {
    phone: phone.value,
    password: password.value,
  }

  const success = await authStore.login(credentials)
  if (success) {
    router.push('/dashboard')
  }
}
</script>
