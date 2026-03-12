<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/attendance" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">حضور {{ att.date }}</h1>
        <p class="text-sm text-gray-500">{{ att.department }} — {{ att.class_name }}</p>
      </div>
      <span :class="stateClass(att.state)" class="text-sm">{{ stateLabel(att.state) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="att.state === 'draft'" @click="doAction('confirm')" class="btn-primary text-sm">تأكيد</button>
        <button v-if="att.state === 'confirmed'" @click="doAction('lock')"
                class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm hover:bg-gray-200 transition-colors">قفل</button>
        <button v-if="att.state !== 'draft'" @click="doAction('draft')" class="btn-outline text-sm">إرجاع لمسودة</button>
      </div>

      <!-- Summary Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
        <div class="bg-white rounded-xl border border-gray-100 p-4 text-center">
          <p class="text-2xl font-bold text-green-600">{{ att.present_count }}</p>
          <p class="text-xs text-gray-500 mt-1">حاضر</p>
        </div>
        <div class="bg-white rounded-xl border border-gray-100 p-4 text-center">
          <p class="text-2xl font-bold text-red-600">{{ att.absent_count }}</p>
          <p class="text-xs text-gray-500 mt-1">غائب</p>
        </div>
        <div class="bg-white rounded-xl border border-gray-100 p-4 text-center">
          <p class="text-2xl font-bold text-amber-600">{{ att.late_count }}</p>
          <p class="text-xs text-gray-500 mt-1">متأخر</p>
        </div>
        <div class="bg-white rounded-xl border border-gray-100 p-4 text-center">
          <p class="text-2xl font-bold text-dark">{{ att.total_count }}</p>
          <p class="text-xs text-gray-500 mt-1">الإجمالي</p>
        </div>
      </div>

      <!-- Info -->
      <div class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-4">بيانات الحضور</h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
          <div><span class="text-gray-500 block mb-0.5">التاريخ</span><span class="text-dark font-medium">{{ att.date }}</span></div>
          <div><span class="text-gray-500 block mb-0.5">القسم</span><span class="text-dark font-medium">{{ att.department || '—' }}</span></div>
          <div><span class="text-gray-500 block mb-0.5">الفصل</span><span class="text-dark font-medium">{{ att.class_name || '—' }}</span></div>
          <div><span class="text-gray-500 block mb-0.5">المسجل</span><span class="text-dark font-medium">{{ att.recorded_by || '—' }}</span></div>
        </div>
        <div v-if="att.notes" class="mt-4 pt-4 border-t border-gray-100">
          <span class="text-gray-500 block mb-1 text-sm">ملاحظات</span>
          <p class="text-sm text-dark">{{ att.notes }}</p>
        </div>
      </div>

      <!-- Attendance Lines -->
      <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
        <div class="p-4 border-b border-gray-100">
          <h3 class="font-bold text-dark">سجل الطلاب ({{ att.lines?.length || 0 }})</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50/80">
              <tr>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الطالب</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">وقت الحضور</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">وقت الانصراف</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">دقائق التأخير</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ملاحظات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!att.lines?.length">
                <td colspan="6" class="py-10 text-center text-gray-400 text-sm">لا توجد سجلات</td>
              </tr>
              <tr v-for="ln in att.lines" :key="ln.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
                <td class="py-3 px-4">
                  <router-link v-if="ln.student_id" :to="'/admin/students/' + ln.student_id" class="text-primary font-medium hover:underline">{{ ln.student }}</router-link>
                  <span v-else class="font-medium text-dark">{{ ln.student }}</span>
                </td>
                <td class="py-3 px-4">
                  <span :class="lineStatusClass(ln.status)">{{ lineStatusLabel(ln.status) }}</span>
                </td>
                <td class="py-3 px-4 text-gray-500 text-xs font-mono">{{ formatTime(ln.check_in_time) }}</td>
                <td class="py-3 px-4 text-gray-500 text-xs font-mono">{{ formatTime(ln.check_out_time) }}</td>
                <td class="py-3 px-4">
                  <span v-if="ln.late_minutes" class="text-amber-600 font-medium">{{ ln.late_minutes }} د</span>
                  <span v-else class="text-gray-400">—</span>
                </td>
                <td class="py-3 px-4 text-gray-500 text-xs">{{ ln.notes || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Action feedback -->
    <div v-if="actionMsg" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-dark text-white px-5 py-2.5 rounded-xl text-sm shadow-lg z-50">
      {{ actionMsg }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { adminApi } from '@/services/adminApi'

const route = useRoute()
const att = ref({})
const loading = ref(true)
const actionMsg = ref('')

const stateLabels = { draft: 'مسودة', confirmed: 'مؤكد', locked: 'مقفل' }
const stateClasses = { draft: 'badge-info', confirmed: 'badge-success', locked: 'bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded-full' }
const lineStatusLabels = { present: 'حاضر', absent: 'غائب', late: 'متأخر', excused: 'معذور' }
const lineStatusClasses = { present: 'badge-success', absent: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full', late: 'badge-warning', excused: 'badge-info' }

function stateLabel(v) { return stateLabels[v] || v || '—' }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function lineStatusLabel(v) { return lineStatusLabels[v] || v || '—' }
function lineStatusClass(v) { return lineStatusClasses[v] || 'badge-info' }

function formatTime(dt) {
  if (!dt) return '—'
  return dt.replace('T', ' ').slice(11, 16)
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getAttendanceRecord(route.params.id)
    att.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.attendanceAction(route.params.id, action)
    actionMsg.value = data.message
    att.value.state = data.state
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

onMounted(fetchData)
</script>
