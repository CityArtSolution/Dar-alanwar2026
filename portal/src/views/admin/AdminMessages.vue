<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">الرسائل</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} رسالة</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالموضوع أو الرقم..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="draft">مسودة</option>
        <option value="scheduled">مجدولة</option>
        <option value="sent">مرسلة</option>
        <option value="cancelled">ملغية</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الرقم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الموضوع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">نوع المستلم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المستلمون</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المرسل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الجدولة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الإرسال</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!messages.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="m in messages" :key="m.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/messages/' + m.id)">
              <td class="py-3 px-4 font-mono text-xs text-gray-600">{{ m.name || '—' }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center shrink-0">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <span class="font-medium text-dark">{{ m.subject }}</span>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="badge-info text-xs">{{ recipientLabel(m.recipient_type) }}</span>
              </td>
              <td class="py-3 px-4 text-dark font-medium">{{ m.recipient_count }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">
                <span v-if="m.sent_count" class="text-green-600">{{ m.sent_count }} مرسلة</span>
                <span v-else>—</span>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ formatDate(m.scheduled_date) }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ formatDate(m.sent_date) }}</td>
              <td class="py-3 px-4">
                <span :class="stateClass(m.state)">{{ stateLabel(m.state) }}</span>
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
const messages = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const stateLabels = { draft: 'مسودة', scheduled: 'مجدولة', sent: 'مرسلة', cancelled: 'ملغية' }
const stateClasses = {
  draft: 'badge-info',
  scheduled: 'badge-warning',
  sent: 'badge-success',
  cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full',
}
const recipientLabels = { all: 'الكل', department: 'قسم', class: 'فصل', individual: 'فردي' }

function stateLabel(v) { return stateLabels[v] || v }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function recipientLabel(v) { return recipientLabels[v] || v }

function formatDate(dt) {
  if (!dt) return '—'
  return dt.replace('T', ' ').slice(0, 16)
}

async function fetchMessages() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getMessages(params)
    messages.value = data.messages || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load messages:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchMessages()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchMessages()
  }, 400)
})

watch(filterStatus, () => {
  page.value = 1
  fetchMessages()
})

onMounted(fetchMessages)
</script>
