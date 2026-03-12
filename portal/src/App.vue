<template>
  <div class="min-h-screen bg-light">
    <!-- Loading State (only on auth-required pages) -->
    <div v-if="!authStore.initialized && currentRoute?.meta?.auth" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        <p class="text-gray-500 text-sm">جاري التحميل...</p>
      </div>
    </div>

    <!-- Admin Layout -->
    <template v-else-if="isAdminPage">
      <AdminLayout />
    </template>

    <!-- Public Layout (homepage, about, etc.) -->
    <template v-else-if="isPublicPage">
      <PublicNavBar />
      <main>
        <router-view />
      </main>
      <FooterSection />
    </template>

    <!-- Authenticated Layout (dashboard, children, etc.) -->
    <template v-else-if="authStore.isAuthenticated">
      <NavBar />
      <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        <router-view />
      </main>
    </template>

    <!-- Guest Layout (login, forgot password — no nav) -->
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import PublicNavBar from '@/components/PublicNavBar.vue'
import FooterSection from '@/components/FooterSection.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

const authStore = useAuthStore()
const currentRoute = useRoute()

const isPublicPage = computed(() => currentRoute.meta?.public === true)
const isAdminPage = computed(() => currentRoute.meta?.admin === true)

onMounted(() => {
  authStore.initAuth()
})
</script>
