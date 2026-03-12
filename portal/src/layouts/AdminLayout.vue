<template>
  <div class="min-h-screen bg-gray-50/80">
    <!-- Mobile Overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black/40 z-40 lg:hidden" @click="sidebarOpen = false"></div>

    <!-- Sidebar -->
    <aside :class="[sidebarOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0']"
           class="fixed top-0 right-0 z-50 h-screen w-72 bg-white border-l border-gray-200 transition-transform duration-300 lg:translate-x-0 flex flex-col">
      <!-- Logo -->
      <div class="h-16 flex items-center gap-3 px-6 border-b border-gray-100">
        <img src="/logo.png" alt="دار الأنوار" class="w-10 h-10 rounded-xl object-contain" />
        <div>
          <h1 class="text-sm font-bold text-dark leading-tight">دار الأنوار</h1>
          <p class="text-[10px] text-gray-400">لوحة التحكم</p>
        </div>
        <button @click="sidebarOpen = false" class="lg:hidden mr-auto p-1 hover:bg-gray-100 rounded-lg">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        <p class="px-3 mb-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider">الرئيسية</p>
        <router-link to="/admin" class="admin-nav-link" exact-active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          <span>لوحة التحكم</span>
        </router-link>

        <p class="px-3 mt-5 mb-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider">الأفراد</p>
        <router-link to="/admin/students" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"/>
          </svg>
          <span>الطلاب</span>
        </router-link>
        <router-link to="/admin/parents" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <span>أولياء الأمور</span>
        </router-link>
        <router-link to="/admin/teachers" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
          </svg>
          <span>المعلمين</span>
        </router-link>

        <p class="px-3 mt-5 mb-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider">المالية</p>
        <router-link to="/admin/subscriptions" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
          </svg>
          <span>الاشتراكات</span>
        </router-link>
        <router-link to="/admin/invoices" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2z"/>
          </svg>
          <span>الفواتير</span>
        </router-link>

        <p class="px-3 mt-5 mb-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider">الإدارة</p>
        <router-link to="/admin/attendance" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
          </svg>
          <span>الحضور</span>
        </router-link>
        <router-link to="/admin/content" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <span>المحتوى</span>
        </router-link>
        <router-link to="/admin/kids-area" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span>منطقة الأطفال</span>
        </router-link>
        <router-link to="/admin/messages" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
          </svg>
          <span>الرسائل</span>
        </router-link>

        <p class="px-3 mt-5 mb-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider">النظام</p>
        <router-link to="/admin/portal-users" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span>مستخدمو البوابة</span>
        </router-link>
        <router-link to="/admin/reports" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          <span>التقارير</span>
        </router-link>
        <router-link to="/admin/settings" class="admin-nav-link" active-class="active" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <span>الإعدادات</span>
        </router-link>
      </nav>

      <!-- User Section -->
      <div class="p-4 border-t border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-gradient-to-bl from-primary to-secondary rounded-lg flex items-center justify-center">
            <span class="text-white text-sm font-bold">م</span>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-dark truncate">{{ authStore.parentName || 'المدير' }}</p>
            <p class="text-[11px] text-gray-400">مدير النظام</p>
          </div>
          <button @click="handleLogout" class="p-2 hover:bg-red-50 rounded-lg transition-colors group" title="تسجيل الخروج">
            <svg class="w-4 h-4 text-gray-400 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="lg:mr-72">
      <!-- Top Bar -->
      <header class="sticky top-0 z-30 h-16 bg-white/80 backdrop-blur-md border-b border-gray-200/60 flex items-center px-4 sm:px-6 gap-4">
        <button @click="sidebarOpen = true" class="lg:hidden p-2 hover:bg-gray-100 rounded-lg">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <h2 class="text-lg font-bold text-dark">{{ pageTitle }}</h2>

        <div class="flex-1"></div>

        <!-- Search -->
        <div class="hidden sm:flex items-center bg-gray-100/80 rounded-xl px-3 py-2 gap-2 w-72">
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input type="text" placeholder="بحث..." class="bg-transparent border-none outline-none text-sm text-gray-600 placeholder:text-gray-400 w-full text-right" />
        </div>

        <!-- Notifications -->
        <button class="relative p-2 hover:bg-gray-100 rounded-xl transition-colors">
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
      </header>

      <!-- Page Content -->
      <main class="p-4 sm:p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const sidebarOpen = ref(false)

const pageTitles = {
  'AdminDashboard': 'لوحة التحكم',
  'AdminStudents': 'إدارة الطلاب',
  'AdminParents': 'أولياء الأمور',
  'AdminTeachers': 'المعلمين',
  'AdminSubscriptions': 'الاشتراكات',
  'AdminInvoices': 'الفواتير',
  'AdminAttendance': 'الحضور',
  'AdminContent': 'المحتوى',
  'AdminKidsArea': 'منطقة الأطفال',
  'AdminMessages': 'الرسائل',
  'AdminPortalUsers': 'مستخدمو البوابة',
  'AdminReports': 'التقارير',
  'AdminSettings': 'الإعدادات',
}

const pageTitle = computed(() => pageTitles[route.name] || 'لوحة التحكم')

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
