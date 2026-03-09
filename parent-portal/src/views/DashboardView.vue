<template>
  <div>
    <!-- Welcome Header -->
    <div class="bg-gradient-to-l from-primary to-secondary rounded-2xl p-6 sm:p-8 mb-8 text-white">
      <h1 class="text-2xl sm:text-3xl font-bold mb-2">مرحباً، {{ authStore.parentName }}</h1>
      <p class="text-white/80">تابع أحدث المستجدات عن أبنائك من هنا</p>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="stat-card">
        <div class="w-11 h-11 bg-primary/10 rounded-xl flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-xs text-gray-500">عدد الأبناء</p>
          <p class="text-xl font-bold text-dark">{{ children.length }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="w-11 h-11 bg-secondary/10 rounded-xl flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-xs text-gray-500">نسبة الحضور</p>
          <p class="text-xl font-bold text-dark">{{ avgAttendance }}%</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="w-11 h-11 bg-accent/10 rounded-xl flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-xs text-gray-500">الرصيد المستحق</p>
          <p class="text-xl font-bold text-dark">{{ totalBalance.toLocaleString() }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="w-11 h-11 bg-blue-50 rounded-xl flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-xs text-gray-500">رسائل جديدة</p>
          <p class="text-xl font-bold text-dark">{{ unreadMessages }}</p>
        </div>
      </div>
    </div>

    <!-- Children Cards -->
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-dark">أبنائي</h2>
      <router-link to="/children" class="text-sm text-primary hover:underline">عرض الكل</router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
      <router-link v-for="child in children" :key="child.id"
                   :to="`/children/${child.id}`"
                   class="card group hover:shadow-md hover:border-primary/20 transition-all cursor-pointer">
        <div class="flex items-center gap-4 mb-4">
          <div class="w-14 h-14 bg-primary/10 rounded-full flex items-center justify-center shrink-0 group-hover:bg-primary/20 transition-colors">
            <img v-if="child.photo_url" :src="child.photo_url" class="w-14 h-14 rounded-full object-cover" />
            <span v-else class="text-xl font-bold text-primary">{{ child.name?.charAt(0) }}</span>
          </div>
          <div class="min-w-0">
            <h3 class="font-bold text-dark truncate">{{ child.name }}</h3>
            <p class="text-sm text-gray-500">{{ child.arabic_name }}</p>
          </div>
          <span :class="child.state === 'enrolled' ? 'badge-success' : 'badge-warning'" class="mr-auto shrink-0">
            {{ child.state === 'enrolled' ? 'مسجل' : child.state }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-light rounded-lg p-2.5 text-center">
            <p class="text-gray-500 text-xs mb-0.5">القسم</p>
            <p class="font-medium text-dark">{{ child.department?.name || '-' }}</p>
          </div>
          <div class="bg-light rounded-lg p-2.5 text-center">
            <p class="text-gray-500 text-xs mb-0.5">الفصل</p>
            <p class="font-medium text-dark">{{ child.class?.name || '-' }}</p>
          </div>
          <div class="bg-light rounded-lg p-2.5 text-center">
            <p class="text-gray-500 text-xs mb-0.5">الحضور</p>
            <p class="font-medium text-secondary">{{ child.attendance_rate?.toFixed(0) || 0 }}%</p>
          </div>
          <div class="bg-light rounded-lg p-2.5 text-center">
            <p class="text-gray-500 text-xs mb-0.5">المستحق</p>
            <p class="font-medium text-primary">{{ child.balance_due?.toLocaleString() || 0 }}</p>
          </div>
        </div>
      </router-link>

      <!-- Empty State -->
      <div v-if="!children.length" class="card col-span-full text-center py-12">
        <div class="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
        </div>
        <p class="text-gray-500">لا يوجد أبناء مسجلين حالياً</p>
      </div>
    </div>

    <!-- Quick Actions -->
    <h2 class="text-lg font-bold text-dark mb-4">وصول سريع</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <router-link v-for="action in quickActions" :key="action.to"
                   :to="action.to"
                   class="card text-center hover:shadow-md hover:border-primary/20 transition-all group">
        <div :class="action.bgClass"
             class="w-12 h-12 rounded-xl mx-auto mb-3 flex items-center justify-center transition-transform group-hover:scale-110">
          <svg :class="action.iconClass" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon"/>
          </svg>
        </div>
        <p class="text-sm font-medium text-dark">{{ action.label }}</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { paymentsApi, messagesApi } from '@/services/api'

const authStore = useAuthStore()
const children = computed(() => authStore.children || [])
const totalBalance = ref(0)
const unreadMessages = ref(0)

const avgAttendance = computed(() => {
  if (!children.value.length) return 0
  const sum = children.value.reduce((acc, c) => acc + (c.attendance_rate || 0), 0)
  return (sum / children.value.length).toFixed(0)
})

const quickActions = [
  {
    to: '/my-payments',
    label: 'المدفوعات',
    bgClass: 'bg-primary/10',
    iconClass: 'text-primary',
    icon: 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
  },
  {
    to: '/books',
    label: 'المكتبة',
    bgClass: 'bg-secondary/10',
    iconClass: 'text-secondary',
    icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
  },
  {
    to: '/kids-area',
    label: 'منطقة الأطفال',
    bgClass: 'bg-accent/10',
    iconClass: 'text-accent-600',
    icon: 'M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  },
  {
    to: '/messages',
    label: 'الرسائل',
    bgClass: 'bg-blue-50',
    iconClass: 'text-blue-600',
    icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
  },
]

onMounted(async () => {
  try {
    const [balanceRes, unreadRes] = await Promise.all([
      paymentsApi.getBalance(),
      messagesApi.getUnreadCount(),
    ])
    totalBalance.value = balanceRes.data.total_balance || 0
    unreadMessages.value = unreadRes.data.unread_count || 0
  } catch (err) {
    console.error('Failed to load dashboard data:', err)
  }
})
</script>
