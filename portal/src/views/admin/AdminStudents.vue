<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">إدارة الطلاب</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} طالب مسجل</p>
      </div>
      <button class="btn-primary flex items-center gap-2 text-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        إضافة طالب
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم أو الرقم..."
               class="input-field text-sm" />
      </div>
      <select v-model="filterDept" class="input-field text-sm w-auto min-w-[150px]">
        <option value="">كل الأقسام</option>
        <option value="tahfiz">تحفيظ</option>
        <option value="languages">لغات</option>
      </select>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[130px]">
        <option value="">كل الحالات</option>
        <option value="enrolled">مسجل</option>
        <option value="new">جديد</option>
        <option value="graduated">متخرج</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الرقم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">القسم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الفصل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ولي الأمر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحضور</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-primary">{{ s.name?.charAt(0) }}</span>
                  </div>
                  <div>
                    <p class="font-medium text-dark">{{ s.name }}</p>
                    <p class="text-[11px] text-gray-400">{{ s.arabic_name }}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 font-mono text-xs">{{ s.code }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.department }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.class_name }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.parent_name }}</td>
              <td class="py-3 px-4">
                <span :class="s.state === 'enrolled' ? 'badge-success' : s.state === 'new' ? 'badge-info' : 'badge-warning'">
                  {{ s.state === 'enrolled' ? 'مسجل' : s.state === 'new' ? 'جديد' : 'متخرج' }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div class="h-full rounded-full" :class="s.attendance > 80 ? 'bg-green-500' : s.attendance > 60 ? 'bg-yellow-500' : 'bg-red-500'"
                         :style="{ width: s.attendance + '%' }"></div>
                  </div>
                  <span class="text-xs text-gray-500">{{ s.attendance }}%</span>
                </div>
              </td>
              <td class="py-3 px-4">
                <button class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
                  </svg>
                </button>
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
const filterDept = ref('')
const filterStatus = ref('')

const students = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

async function fetchStudents() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterDept.value) params.department = filterDept.value === 'tahfiz' ? 'تحفيظ' : 'لغات'
    if (filterStatus.value) params.status = filterStatus.value

    const { data } = await adminApi.getStudents(params)
    students.value = data.students || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load students:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchStudents()
}

// Debounced search
watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchStudents()
  }, 400)
})

watch([filterDept, filterStatus], () => {
  page.value = 1
  fetchStudents()
})

onMounted(fetchStudents)
</script>
