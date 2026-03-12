<template>
  <div>
    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
    <!-- Welcome Banner -->
    <div class="bg-gradient-to-l from-primary via-primary-600 to-secondary rounded-2xl p-6 sm:p-8 mb-6 text-white relative overflow-hidden">
      <div class="absolute left-0 top-0 w-40 h-40 bg-white/5 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
      <div class="absolute left-20 bottom-0 w-24 h-24 bg-white/5 rounded-full translate-y-1/2"></div>
      <div class="relative">
        <p class="text-white/70 text-sm mb-1">مرحباً بك</p>
        <h1 class="text-2xl sm:text-3xl font-bold mb-1">لوحة تحكم دار الأنوار</h1>
        <p class="text-white/70 text-sm">إليك ملخص أحدث البيانات والإحصائيات</p>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
      <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-xl border border-gray-100 p-4 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-3">
          <div :class="stat.bgClass" class="w-10 h-10 rounded-xl flex items-center justify-center">
            <svg :class="stat.iconClass" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="stat.icon"/>
            </svg>
          </div>
          <span v-if="stat.trend" :class="stat.trend > 0 ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'"
                class="text-[11px] font-medium px-1.5 py-0.5 rounded-md">
            {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
          </span>
        </div>
        <p class="text-2xl font-bold text-dark mb-0.5">{{ stat.value }}</p>
        <p class="text-xs text-gray-500">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- Revenue Chart Placeholder -->
      <div class="lg:col-span-2 bg-white rounded-xl border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-bold text-dark">الإيرادات الشهرية</h3>
          <div class="flex gap-1 bg-gray-100 rounded-lg p-0.5">
            <button v-for="period in ['أسبوعي', 'شهري', 'سنوي']" :key="period"
                    :class="selectedPeriod === period ? 'bg-white shadow-sm text-dark' : 'text-gray-500'"
                    class="px-3 py-1 rounded-md text-xs font-medium transition-all"
                    @click="selectedPeriod = period">
              {{ period }}
            </button>
          </div>
        </div>
        <!-- Chart Bars -->
        <div class="flex items-end gap-2 h-48">
          <div v-for="(bar, i) in chartData" :key="i" class="flex-1 flex flex-col items-center gap-1">
            <div class="w-full rounded-t-lg transition-all duration-500"
                 :class="i === chartData.length - 1 ? 'bg-gradient-to-t from-primary to-primary-400' : 'bg-gray-200 hover:bg-primary-200'"
                 :style="{ height: bar.height + '%' }"></div>
            <span class="text-[10px] text-gray-400">{{ bar.label }}</span>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-6 text-sm">
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-sm bg-primary"></div>
            <span class="text-gray-500">الشهر الحالي</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-sm bg-gray-200"></div>
            <span class="text-gray-500">الأشهر السابقة</span>
          </div>
        </div>
      </div>

      <!-- Quick Stats Cards -->
      <div class="space-y-4">
        <!-- Subscriptions Summary -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark text-sm mb-4">حالة الاشتراكات</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full bg-green-500"></div>
                <span class="text-sm text-gray-600">نشط</span>
              </div>
              <span class="text-sm font-bold text-dark">{{ subscriptionStats.active }}</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full bg-yellow-500"></div>
                <span class="text-sm text-gray-600">قيد المراجعة</span>
              </div>
              <span class="text-sm font-bold text-dark">{{ subscriptionStats.draft }}</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full bg-red-500"></div>
                <span class="text-sm text-gray-600">منتهي</span>
              </div>
              <span class="text-sm font-bold text-dark">{{ subscriptionStats.expired }}</span>
            </div>
          </div>
          <!-- Progress Bar -->
          <div class="mt-4 h-2 bg-gray-100 rounded-full overflow-hidden flex">
            <div class="bg-green-500 rounded-r-full" :style="{ width: subscriptionPercent.active + '%' }"></div>
            <div class="bg-yellow-500" :style="{ width: subscriptionPercent.draft + '%' }"></div>
            <div class="bg-red-500 rounded-l-full" :style="{ width: subscriptionPercent.expired + '%' }"></div>
          </div>
        </div>

        <!-- Invoice Summary -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark text-sm mb-4">ملخص الفواتير</h3>
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-green-50 rounded-lg p-3 text-center">
              <p class="text-lg font-bold text-green-700">{{ invoiceStats.paid }}</p>
              <p class="text-[11px] text-green-600">مدفوعة</p>
            </div>
            <div class="bg-yellow-50 rounded-lg p-3 text-center">
              <p class="text-lg font-bold text-yellow-700">{{ invoiceStats.pending }}</p>
              <p class="text-[11px] text-yellow-600">معلقة</p>
            </div>
            <div class="bg-blue-50 rounded-lg p-3 text-center">
              <p class="text-lg font-bold text-blue-700">{{ invoiceStats.draft }}</p>
              <p class="text-[11px] text-blue-600">مسودة</p>
            </div>
            <div class="bg-red-50 rounded-lg p-3 text-center">
              <p class="text-lg font-bold text-red-700">{{ invoiceStats.overdue }}</p>
              <p class="text-[11px] text-red-600">متأخرة</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity & Quick Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Students -->
      <div class="lg:col-span-2 bg-white rounded-xl border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-dark">أحدث الطلاب المسجلين</h3>
          <router-link to="/admin/students" class="text-xs text-primary hover:underline">عرض الكل</router-link>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="text-right py-3 px-2 text-gray-500 font-medium text-xs">الطالب</th>
                <th class="text-right py-3 px-2 text-gray-500 font-medium text-xs">القسم</th>
                <th class="text-right py-3 px-2 text-gray-500 font-medium text-xs">الفصل</th>
                <th class="text-right py-3 px-2 text-gray-500 font-medium text-xs">الحالة</th>
                <th class="text-right py-3 px-2 text-gray-500 font-medium text-xs">التاريخ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in recentStudents" :key="student.id" class="border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
                <td class="py-3 px-2">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                      <span class="text-xs font-bold text-primary">{{ student.name?.charAt(0) }}</span>
                    </div>
                    <span class="font-medium text-dark">{{ student.name }}</span>
                  </div>
                </td>
                <td class="py-3 px-2 text-gray-600">{{ student.department }}</td>
                <td class="py-3 px-2 text-gray-600">{{ student.class_name }}</td>
                <td class="py-3 px-2">
                  <span :class="student.state === 'enrolled' ? 'badge-success' : 'badge-warning'">
                    {{ student.state === 'enrolled' ? 'مسجل' : 'جديد' }}
                  </span>
                </td>
                <td class="py-3 px-2 text-gray-400 text-xs">{{ student.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="space-y-4">
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark text-sm mb-4">إجراءات سريعة</h3>
          <div class="space-y-2">
            <router-link v-for="action in quickActions" :key="action.to" :to="action.to"
                         class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-colors group">
              <div :class="action.bgClass" class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <svg :class="action.iconClass" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.icon"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-dark">{{ action.label }}</p>
                <p class="text-[11px] text-gray-400">{{ action.desc }}</p>
              </div>
              <svg class="w-4 h-4 text-gray-300 mr-auto rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </router-link>
          </div>
        </div>

        <!-- Today's Summary -->
        <div class="bg-gradient-to-bl from-secondary/5 to-primary/5 rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark text-sm mb-3">ملخص اليوم</h3>
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-dark">{{ todaySummaryFormatted.present }} حاضر</p>
                <p class="text-[11px] text-gray-400">من أصل {{ todaySummaryFormatted.total }} طالب</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2z"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-dark">{{ todaySummaryFormatted.invoices }} فاتورة جديدة</p>
                <p class="text-[11px] text-gray-400">بإجمالي {{ todaySummaryFormatted.invoiceTotal.toLocaleString() }} ج.م</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-dark">{{ todaySummaryFormatted.newStudents }} طالب جديد</p>
                <p class="text-[11px] text-gray-400">تم التسجيل اليوم</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/services/adminApi'

const selectedPeriod = ref('شهري')
const loading = ref(true)

const statIcons = [
  { key: 'student_count', label: 'إجمالي الطلاب', bgClass: 'bg-primary/10', iconClass: 'text-primary', icon: 'M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222' },
  { key: 'parent_count', label: 'أولياء الأمور', bgClass: 'bg-secondary/10', iconClass: 'text-secondary', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
  { key: 'teacher_count', label: 'المعلمين', bgClass: 'bg-accent/10', iconClass: 'text-accent-600', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
  { key: 'active_subscriptions', label: 'الاشتراكات النشطة', bgClass: 'bg-green-50', iconClass: 'text-green-600', icon: 'M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z' },
  { key: 'total_revenue', label: 'إجمالي الإيرادات', bgClass: 'bg-blue-50', iconClass: 'text-blue-600', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', format: 'currency' },
  { key: 'attendance_rate', label: 'نسبة الحضور', bgClass: 'bg-purple-50', iconClass: 'text-purple-600', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4', format: 'percent' },
]

const dashboardData = ref(null)

const stats = computed(() => {
  const d = dashboardData.value
  if (!d) return statIcons.map(s => ({ ...s, value: '—', trend: null }))
  return statIcons.map(s => {
    let value = d[s.key] ?? 0
    if (s.format === 'currency') value = value.toLocaleString('ar-EG')
    else if (s.format === 'percent') value = value + '%'
    else value = String(value)
    return { ...s, value, trend: null }
  })
})

const chartData = [
  { label: 'يناير', height: 45 },
  { label: 'فبراير', height: 60 },
  { label: 'مارس', height: 35 },
  { label: 'أبريل', height: 70 },
  { label: 'مايو', height: 55 },
  { label: 'يونيو', height: 80 },
  { label: 'يوليو', height: 65 },
  { label: 'أغسطس', height: 40 },
  { label: 'سبتمبر', height: 75 },
  { label: 'أكتوبر', height: 50 },
  { label: 'نوفمبر', height: 85 },
  { label: 'ديسمبر', height: 95 },
]

const subscriptionStats = computed(() =>
  dashboardData.value?.subscription_stats || { active: 0, draft: 0, expired: 0 }
)
const subscriptionPercent = computed(() => {
  const s = subscriptionStats.value
  const total = s.active + s.draft + s.expired
  if (!total) return { active: 0, draft: 0, expired: 0 }
  return {
    active: ((s.active / total) * 100).toFixed(0),
    draft: ((s.draft / total) * 100).toFixed(0),
    expired: ((s.expired / total) * 100).toFixed(0),
  }
})

const invoiceStats = computed(() =>
  dashboardData.value?.invoice_stats || { paid: 0, pending: 0, draft: 0, overdue: 0 }
)

const recentStudents = computed(() =>
  dashboardData.value?.recent_students || []
)

const quickActions = [
  { to: '/admin/students', label: 'إضافة طالب', desc: 'تسجيل طالب جديد', bgClass: 'bg-primary/10', iconClass: 'text-primary', icon: 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z' },
  { to: '/admin/subscriptions', label: 'اشتراك جديد', desc: 'إنشاء اشتراك', bgClass: 'bg-secondary/10', iconClass: 'text-secondary', icon: 'M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z' },
  { to: '/admin/invoices', label: 'إنشاء فاتورة', desc: 'فاتورة جديدة', bgClass: 'bg-blue-50', iconClass: 'text-blue-600', icon: 'M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2z' },
  { to: '/admin/reports', label: 'عرض التقارير', desc: 'التقارير والإحصائيات', bgClass: 'bg-purple-50', iconClass: 'text-purple-600', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
]

const todaySummary = computed(() =>
  dashboardData.value?.today_summary || { present: 0, total: 0, invoices: 0, invoiceTotal: 0, newStudents: 0 }
)

// Alias for template (API returns snake_case)
const todaySummaryFormatted = computed(() => ({
  present: todaySummary.value.present,
  total: todaySummary.value.total,
  invoices: todaySummary.value.invoices,
  invoiceTotal: todaySummary.value.invoice_total || todaySummary.value.invoiceTotal || 0,
  newStudents: todaySummary.value.new_students || todaySummary.value.newStudents || 0,
}))

onMounted(async () => {
  try {
    const { data } = await adminApi.getDashboard()
    dashboardData.value = data
  } catch (e) {
    console.error('Failed to load dashboard:', e)
  } finally {
    loading.value = false
  }
})
</script>
