<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">الاشتراكات</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} اشتراك</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالطالب أو نوع الاشتراك..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="active">نشط</option>
        <option value="draft">مسودة</option>
        <option value="expired">منتهي</option>
        <option value="cancelled">ملغي</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الطالب</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">نوع الاشتراك</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ البدء</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الانتهاء</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الإجمالي</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المدفوع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المتبقي</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!subscriptions.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="s in subscriptions" :key="s.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/subscriptions/' + s.id)">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-primary">{{ s.student?.charAt(0) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ s.student }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-600">{{ s.type || '—' }}</td>
              <td class="py-3 px-4">
                <span :class="statusClass(s.status)">{{ statusLabel(s.status) }}</span>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ s.start_date }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ s.end_date }}</td>
              <td class="py-3 px-4 font-medium text-dark">{{ s.total_amount?.toLocaleString() }}</td>
              <td class="py-3 px-4 text-green-600 font-medium">{{ s.paid_amount?.toLocaleString() }}</td>
              <td class="py-3 px-4">
                <span :class="s.remaining_amount > 0 ? 'text-red-600' : 'text-green-600'" class="font-medium">
                  {{ s.remaining_amount?.toLocaleString() }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-4">
      <button @click="changePage(page - 1)" :disabled="page <= 1"
              class="px-3 py-1.5 text-sm rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
        السابق
      </button>
      <span class="text-sm text-gray-500">{{ page }} / {{ totalPages }}</span>
      <button @click="changePage(page + 1)" :disabled="page >= totalPages"
              class="px-3 py-1.5 text-sm rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
        التالي
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { adminApi } from '@/services/adminApi'

const search = ref('')
const filterStatus = ref('')
const subscriptions = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const statusLabels = { active: 'نشط', draft: 'مسودة', expired: 'منتهي', cancelled: 'ملغي' }
const statusClasses = {
  active: 'badge-success',
  draft: 'badge-info',
  expired: 'badge-warning',
  cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full',
}
function statusLabel(v) { return statusLabels[v] || v }
function statusClass(v) { return statusClasses[v] || 'badge-info' }

async function fetchSubscriptions() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getSubscriptions(params)
    subscriptions.value = data.subscriptions || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load subscriptions:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchSubscriptions()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchSubscriptions()
  }, 400)
})

watch(filterStatus, () => {
  page.value = 1
  fetchSubscriptions()
})

onMounted(fetchSubscriptions)
</script>
