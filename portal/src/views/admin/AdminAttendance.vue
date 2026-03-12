<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">الحضور</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} سجل حضور</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالفصل أو القسم..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="draft">مسودة</option>
        <option value="confirmed">مؤكد</option>
        <option value="locked">مقفل</option>
      </select>
      <input v-model="dateFrom" type="date" class="input-field text-sm w-auto" placeholder="من تاريخ" />
      <input v-model="dateTo" type="date" class="input-field text-sm w-auto" placeholder="إلى تاريخ" />
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">التاريخ</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">القسم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الفصل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحاضرون</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الغائبون</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المتأخرون</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الإجمالي</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المسجل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!records.length">
              <td colspan="9" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="a in records" :key="a.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/attendance/' + a.id)">
              <td class="py-3 px-4 text-gray-600 text-xs font-medium">{{ a.date }}</td>
              <td class="py-3 px-4 text-gray-600">{{ a.department || '—' }}</td>
              <td class="py-3 px-4 font-medium text-dark">{{ a.class_name || '—' }}</td>
              <td class="py-3 px-4 text-green-600 font-medium">{{ a.present_count }}</td>
              <td class="py-3 px-4 text-red-600 font-medium">{{ a.absent_count }}</td>
              <td class="py-3 px-4 text-amber-600 font-medium">{{ a.late_count }}</td>
              <td class="py-3 px-4 text-dark font-medium">{{ a.total_count }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ a.recorded_by || '—' }}</td>
              <td class="py-3 px-4">
                <span :class="stateClass(a.state)">{{ stateLabel(a.state) }}</span>
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
const dateFrom = ref('')
const dateTo = ref('')
const records = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const stateLabels = { draft: 'مسودة', confirmed: 'مؤكد', locked: 'مقفل' }
const stateClasses = {
  draft: 'badge-info',
  confirmed: 'badge-success',
  locked: 'bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded-full',
}
function stateLabel(v) { return stateLabels[v] || v }
function stateClass(v) { return stateClasses[v] || 'badge-info' }

async function fetchAttendance() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value
    const { data } = await adminApi.getAttendance(params)
    records.value = data.attendance || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load attendance:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchAttendance()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchAttendance()
  }, 400)
})

watch([filterStatus, dateFrom, dateTo], () => {
  page.value = 1
  fetchAttendance()
})

onMounted(fetchAttendance)
</script>
