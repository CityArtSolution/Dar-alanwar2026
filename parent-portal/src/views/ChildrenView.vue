<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">أبنائي</h1>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <svg class="w-16 h-16 text-red-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
      </svg>
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchData" class="btn-primary">إعادة المحاولة</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="children.length === 0" class="card text-center py-16">
      <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
      </svg>
      <p class="text-gray-500 text-lg">لا يوجد أبناء مسجلين حالياً</p>
    </div>

    <!-- Children Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="child in children"
        :key="child.id"
        :to="`/children/${child.id}`"
        class="card hover:shadow-lg transition-shadow cursor-pointer group"
      >
        <!-- Avatar & Name -->
        <div class="flex items-center gap-4 mb-5">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
            <img
              v-if="child.photo_url"
              :src="child.photo_url"
              :alt="child.name"
              class="w-16 h-16 rounded-full object-cover"
            />
            <span v-else class="text-2xl font-bold text-primary-600">
              {{ child.name?.charAt(0) || child.arabic_name?.charAt(0) || '?' }}
            </span>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-bold text-lg truncate group-hover:text-primary-600 transition-colors">
              {{ child.name }}
            </h3>
            <p class="text-sm text-gray-500 truncate">{{ child.arabic_name }}</p>
          </div>
          <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </div>

        <!-- Info Grid -->
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <p class="text-gray-500 text-xs mb-1">القسم</p>
            <p class="font-medium">{{ child.department?.name || '-' }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <p class="text-gray-500 text-xs mb-1">الفصل</p>
            <p class="font-medium">{{ child.class?.name || '-' }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <p class="text-gray-500 text-xs mb-1">نسبة الحضور</p>
            <p class="font-medium" :class="attendanceColor(child.attendance_rate)">
              {{ child.attendance_rate?.toFixed(0) || 0 }}%
            </p>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <p class="text-gray-500 text-xs mb-1">الرصيد المستحق</p>
            <p class="font-medium text-yellow-600">
              {{ child.balance_due?.toLocaleString() || 0 }} ر.س
            </p>
          </div>
        </div>

        <!-- Status Badge -->
        <div class="mt-4 flex items-center justify-between">
          <span :class="stateClass(child.state)">
            {{ stateLabel(child.state) }}
          </span>
          <span class="text-xs text-gray-400">{{ child.code }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { childrenApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const children = ref([])
const loading = ref(false)
const error = ref(null)

function attendanceColor(rate) {
  if (!rate) return 'text-gray-500'
  if (rate >= 90) return 'text-green-600'
  if (rate >= 75) return 'text-yellow-600'
  return 'text-red-600'
}

function stateClass(state) {
  switch (state) {
    case 'enrolled': return 'badge-success'
    case 'graduated': return 'badge-success'
    case 'suspended': return 'badge-danger'
    case 'pending': return 'badge-warning'
    default: return 'badge-warning'
  }
}

function stateLabel(state) {
  const labels = {
    enrolled: 'مسجل',
    graduated: 'متخرج',
    suspended: 'معلق',
    pending: 'قيد المراجعة',
    withdrawn: 'منسحب',
  }
  return labels[state] || state || '-'
}

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const { data } = await childrenApi.getAll()
    children.value = data.children || []
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل بيانات الأبناء. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch children:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Use cached data from auth store if available, otherwise fetch
  if (authStore.children?.length) {
    children.value = authStore.children
  } else {
    fetchData()
  }
})
</script>
