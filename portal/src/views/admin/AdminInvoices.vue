<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">الفواتير</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} فاتورة</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم أو رقم الفاتورة..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="paid">مدفوعة</option>
        <option value="pending">معلقة</option>
        <option value="draft">مسودة</option>
        <option value="overdue">متأخرة</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">رقم الفاتورة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">العميل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">التاريخ</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الاستحقاق</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المبلغ</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المدفوع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المتبقي</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!invoices.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="inv in invoices" :key="inv.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
              <td class="py-3 px-4 font-mono text-xs text-gray-600">{{ inv.name }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-blue-600">{{ inv.partner?.charAt(0) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ inv.partner }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ inv.date }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ inv.due_date || '—' }}</td>
              <td class="py-3 px-4 font-medium text-dark">{{ inv.amount?.toLocaleString() }}</td>
              <td class="py-3 px-4 text-green-600 font-medium">{{ inv.paid_amount?.toLocaleString() }}</td>
              <td class="py-3 px-4">
                <span :class="inv.residual > 0 ? 'text-red-600' : 'text-green-600'" class="font-medium">
                  {{ inv.residual?.toLocaleString() }}
                </span>
              </td>
              <td class="py-3 px-4">
                <span :class="paymentStatusClass(inv)">{{ paymentStatusLabel(inv) }}</span>
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
const invoices = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

function paymentStatusLabel(inv) {
  if (inv.state === 'draft') return 'مسودة'
  if (inv.payment_state === 'paid') return 'مدفوعة'
  if (inv.due_date && inv.due_date < new Date().toISOString().slice(0, 10) && inv.payment_state !== 'paid') return 'متأخرة'
  return 'معلقة'
}

function paymentStatusClass(inv) {
  if (inv.state === 'draft') return 'badge-info'
  if (inv.payment_state === 'paid') return 'badge-success'
  if (inv.due_date && inv.due_date < new Date().toISOString().slice(0, 10) && inv.payment_state !== 'paid')
    return 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'
  return 'badge-warning'
}

async function fetchInvoices() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getInvoices(params)
    invoices.value = data.invoices || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load invoices:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchInvoices()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchInvoices()
  }, 400)
})

watch(filterStatus, () => {
  page.value = 1
  fetchInvoices()
})

onMounted(fetchInvoices)
</script>
