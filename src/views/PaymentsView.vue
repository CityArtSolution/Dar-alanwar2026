<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">المدفوعات</h1>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchData" class="btn-primary">إعادة المحاولة</button>
    </div>

    <template v-else>
      <!-- Balance Summary -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <div v-for="childBalance in balances" :key="childBalance.child_id" class="stat-card">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-sm font-bold text-primary-600">
                {{ childBalance.child_name?.charAt(0) || '?' }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium truncate">{{ childBalance.child_name }}</p>
              <p class="text-xs text-gray-500">{{ childBalance.child_arabic_name }}</p>
            </div>
          </div>
          <div class="flex items-end justify-between">
            <div>
              <p class="text-sm text-gray-500">المبلغ المستحق</p>
              <p class="text-2xl font-bold" :class="childBalance.total_due > 0 ? 'text-red-600' : 'text-green-600'">
                {{ childBalance.total_due?.toLocaleString() || 0 }} <span class="text-sm">ر.س</span>
              </p>
            </div>
            <span v-if="childBalance.total_due <= 0" class="badge-success">مسدد</span>
          </div>
        </div>

        <!-- Total Summary -->
        <div v-if="balances.length > 1" class="stat-card bg-gradient-to-br from-primary-50 to-primary-100 border-primary-200">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
            <p class="font-medium">الإجمالي</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">إجمالي المبلغ المستحق</p>
            <p class="text-2xl font-bold text-primary-700">
              {{ totalDue.toLocaleString() }} <span class="text-sm">ر.س</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Tab Navigation -->
      <div class="flex gap-1 mb-6 bg-white rounded-xl p-1 border border-gray-200">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
          :class="activeTab === tab.key ? 'bg-primary-500 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Invoices Tab -->
      <div v-if="activeTab === 'invoices'">
        <!-- Status Filters -->
        <div class="flex flex-wrap gap-2 mb-4">
          <button
            @click="invoiceFilter = null"
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
            :class="!invoiceFilter ? 'bg-primary-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
          >
            الكل ({{ invoices.length }})
          </button>
          <button
            @click="invoiceFilter = 'paid'"
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
            :class="invoiceFilter === 'paid' ? 'bg-green-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
          >
            مدفوع ({{ invoicesByStatus('paid').length }})
          </button>
          <button
            @click="invoiceFilter = 'pending'"
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
            :class="invoiceFilter === 'pending' ? 'bg-yellow-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
          >
            معلق ({{ invoicesByStatus('pending').length }})
          </button>
          <button
            @click="invoiceFilter = 'overdue'"
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
            :class="invoiceFilter === 'overdue' ? 'bg-red-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
          >
            متأخر ({{ invoicesByStatus('overdue').length }})
          </button>
        </div>

        <!-- Invoice List -->
        <div v-if="filteredInvoices.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <p class="text-gray-500">لا توجد فواتير</p>
        </div>

        <div v-else class="space-y-3">
          <div v-for="invoice in filteredInvoices" :key="invoice.id" class="card">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h3 class="font-bold">{{ invoice.description || invoice.title || 'فاتورة' }}</h3>
                  <span :class="invoiceStatusClass(invoice.status)">
                    {{ invoiceStatusLabel(invoice.status) }}
                  </span>
                </div>
                <div class="flex flex-wrap gap-4 text-sm text-gray-500">
                  <span v-if="invoice.invoice_number">رقم: {{ invoice.invoice_number }}</span>
                  <span v-if="invoice.child_name">الطالب: {{ invoice.child_name }}</span>
                  <span>التاريخ: {{ formatDate(invoice.date || invoice.created_at) }}</span>
                  <span v-if="invoice.due_date">الاستحقاق: {{ formatDate(invoice.due_date) }}</span>
                </div>
              </div>

              <div class="flex items-center gap-3">
                <span class="text-lg font-bold" :class="invoice.status === 'paid' ? 'text-green-600' : 'text-gray-900'">
                  {{ invoice.amount?.toLocaleString() || 0 }} ر.س
                </span>
                <button
                  v-if="invoice.status === 'paid' && invoice.receipt_url"
                  @click="downloadReceipt(invoice)"
                  class="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                  title="تحميل الإيصال"
                >
                  <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Partial Payment Details -->
            <div v-if="invoice.paid_amount && invoice.paid_amount < invoice.amount" class="mt-3 pt-3 border-t border-gray-100">
              <div class="flex justify-between items-center text-sm mb-1">
                <span class="text-gray-500">المدفوع</span>
                <span class="text-green-600 font-medium">{{ invoice.paid_amount?.toLocaleString() || 0 }} ر.س</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-gray-500">المتبقي</span>
                <span class="text-red-600 font-medium">{{ (invoice.amount - invoice.paid_amount)?.toLocaleString() || 0 }} ر.س</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Subscriptions Tab -->
      <div v-if="activeTab === 'subscriptions'">
        <div v-if="subscriptions.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          <p class="text-gray-500 text-lg">لا توجد اشتراكات نشطة</p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="sub in subscriptions" :key="sub.id" class="card">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="font-bold text-lg">{{ sub.name }}</h3>
                <p class="text-sm text-gray-500">{{ sub.child_name }}</p>
              </div>
              <span :class="sub.status === 'active' ? 'badge-success' : sub.status === 'expired' ? 'badge-danger' : 'badge-warning'">
                {{ subStatusLabel(sub.status) }}
              </span>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm mb-4">
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-gray-500 text-xs mb-1">المبلغ الإجمالي</p>
                <p class="font-bold">{{ sub.total_amount?.toLocaleString() || 0 }} ر.س</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-gray-500 text-xs mb-1">المدفوع</p>
                <p class="font-bold text-green-600">{{ sub.paid_amount?.toLocaleString() || 0 }} ر.س</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-gray-500 text-xs mb-1">المتبقي</p>
                <p class="font-bold text-red-600">{{ sub.remaining_amount?.toLocaleString() || 0 }} ر.س</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-gray-500 text-xs mb-1">عدد الأقساط</p>
                <p class="font-bold">{{ sub.installments_count || 0 }}</p>
              </div>
            </div>

            <!-- Installments for this subscription -->
            <div v-if="sub.installments && sub.installments.length > 0">
              <h4 class="font-medium text-sm text-gray-600 mb-2">جدول الأقساط</h4>
              <div class="divide-y divide-gray-100 border border-gray-200 rounded-lg">
                <div v-for="inst in sub.installments" :key="inst.id" class="flex items-center justify-between p-3">
                  <div>
                    <p class="font-medium text-sm">{{ inst.description || `القسط ${inst.number || ''}` }}</p>
                    <p class="text-xs text-gray-400">{{ formatDate(inst.due_date) }}</p>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="font-bold text-sm">{{ inst.amount?.toLocaleString() || 0 }} ر.س</span>
                    <span :class="inst.paid ? 'badge-success' : isOverdue(inst.due_date) ? 'badge-danger' : 'badge-warning'">
                      {{ inst.paid ? 'مدفوع' : isOverdue(inst.due_date) ? 'متأخر' : 'مستحق' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Installments Tab -->
      <div v-if="activeTab === 'installments'">
        <div v-if="allInstallments.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <p class="text-gray-500 text-lg">لا توجد أقساط مستحقة</p>
        </div>

        <div v-else class="card">
          <div class="divide-y divide-gray-100">
            <div v-for="inst in allInstallments" :key="inst.id" class="flex items-center justify-between py-4">
              <div class="flex-1">
                <h3 class="font-medium">{{ inst.description || 'قسط' }}</h3>
                <div class="flex flex-wrap gap-3 text-sm text-gray-500 mt-1">
                  <span>{{ inst.child_name }}</span>
                  <span>تاريخ الاستحقاق: {{ formatDate(inst.due_date) }}</span>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span class="font-bold">{{ inst.amount?.toLocaleString() || 0 }} ر.س</span>
                <span v-if="inst.paid" class="badge-success">مدفوع</span>
                <template v-else>
                  <span :class="isOverdue(inst.due_date) ? 'badge-danger' : 'badge-warning'">
                    {{ isOverdue(inst.due_date) ? 'متأخر' : 'غير مدفوع' }}
                  </span>
                  <button @click="payInstallment(inst)" class="btn-primary text-sm px-3 py-1.5" :disabled="paying === inst.id">
                    {{ paying === inst.id ? 'جارٍ...' : 'ادفع' }}
                  </button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment History Tab -->
      <div v-if="activeTab === 'history'">
        <div v-if="paymentHistory.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p class="text-gray-500 text-lg">لا توجد مدفوعات سابقة</p>
        </div>

        <div v-else class="card">
          <div class="divide-y divide-gray-100">
            <div v-for="payment in paymentHistory" :key="payment.id" class="flex items-center justify-between py-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                </div>
                <div>
                  <h3 class="font-medium">{{ payment.description || 'دفعة' }}</h3>
                  <div class="flex flex-wrap gap-2 text-xs text-gray-400 mt-1">
                    <span>{{ payment.child_name }}</span>
                    <span>{{ formatDate(payment.payment_date || payment.created_at) }}</span>
                    <span v-if="payment.method">{{ paymentMethodLabel(payment.method) }}</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span class="font-bold text-green-600">{{ payment.amount?.toLocaleString() || 0 }} ر.س</span>
                <button
                  v-if="payment.receipt_url"
                  @click="downloadReceipt(payment)"
                  class="text-sm text-primary-500 hover:text-primary-700 hover:bg-primary-50 px-3 py-1.5 rounded-lg transition-colors"
                  title="تحميل الإيصال"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </button>
                <button
                  v-else
                  class="text-sm text-gray-400 px-3 py-1.5 rounded-lg cursor-not-allowed"
                  title="الإيصال غير متاح"
                  disabled
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </button>
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
import { paymentsApi, subscriptionsApi, invoicesApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)
const error = ref(null)
const activeTab = ref('invoices')
const paying = ref(null)

const tabs = [
  { key: 'invoices', label: 'الفواتير' },
  { key: 'subscriptions', label: 'الاشتراكات' },
  { key: 'installments', label: 'الأقساط' },
  { key: 'history', label: 'سجل المدفوعات' },
]

const balances = ref([])
const invoices = ref([])
const invoiceFilter = ref(null)
const subscriptions = ref([])
const allInstallments = ref([])
const paymentHistory = ref([])

const filteredInvoices = computed(() => {
  if (!invoiceFilter.value) return invoices.value
  return invoices.value.filter((inv) => inv.status === invoiceFilter.value)
})

function invoicesByStatus(status) {
  return invoices.value.filter((inv) => inv.status === status)
}

function invoiceStatusClass(status) {
  switch (status) {
    case 'paid': return 'badge-success'
    case 'pending': return 'badge-warning'
    case 'overdue': return 'badge-danger'
    case 'partial': return 'text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700'
    default: return 'badge-warning'
  }
}

function invoiceStatusLabel(status) {
  const labels = { paid: 'مدفوع', pending: 'معلق', overdue: 'متأخر', partial: 'مدفوع جزئياً', cancelled: 'ملغي' }
  return labels[status] || status || '-'
}

const totalDue = computed(() => {
  return balances.value.reduce((sum, b) => sum + (b.total_due || 0), 0)
})

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    return new Date(dateStr).toLocaleDateString('ar-SA')
  } catch {
    return dateStr
  }
}

function isOverdue(dueDate) {
  if (!dueDate) return false
  return new Date(dueDate) < new Date()
}

function subStatusLabel(status) {
  const labels = { active: 'نشط', expired: 'منتهي', suspended: 'معلق', pending: 'قيد الانتظار' }
  return labels[status] || status
}

function paymentMethodLabel(method) {
  const labels = { cash: 'نقداً', card: 'بطاقة', transfer: 'تحويل', online: 'إلكتروني' }
  return labels[method] || method
}

function downloadReceipt(payment) {
  if (payment.receipt_url) {
    window.open(payment.receipt_url, '_blank')
  }
}

async function payInstallment(inst) {
  paying.value = inst.id
  try {
    await paymentsApi.create({
      installment_id: inst.id,
      amount: inst.amount,
    })
    // Mark as paid in UI
    inst.paid = true
    // Refresh data
    fetchData()
  } catch (err) {
    console.error('Failed to process payment:', err)
    alert(err.response?.data?.message || 'حدث خطأ أثناء معالجة الدفع. يرجى المحاولة مرة أخرى.')
  } finally {
    paying.value = null
  }
}

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const [balanceRes, subsRes, installmentsRes, historyRes] = await Promise.all([
      paymentsApi.getBalance(),
      subscriptionsApi.getAll(),
      invoicesApi.getAll({ status: 'all' }),
      paymentsApi.getAll({ limit: 50 }),
    ])

    // Balance per child
    const balanceData = balanceRes.data
    if (balanceData?.children) {
      balances.value = balanceData.children
    } else if (balanceData?.total_balance !== undefined) {
      // Fallback: construct from auth store children data
      balances.value = (authStore.children || []).map((child) => ({
        child_id: child.id,
        child_name: child.name,
        child_arabic_name: child.arabic_name,
        total_due: child.balance_due || 0,
      }))
    }

    subscriptions.value = subsRes.data?.subscriptions || subsRes.data || []
    const invoiceData = installmentsRes.data?.invoices || installmentsRes.data?.installments || installmentsRes.data || []
    allInstallments.value = invoiceData
    invoices.value = invoiceData
    paymentHistory.value = historyRes.data?.payments || historyRes.data || []
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل بيانات المدفوعات. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch payment data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>
