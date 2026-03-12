<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/invoices" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">فاتورة {{ inv.name }}</h1>
        <p class="text-sm text-gray-500">{{ inv.partner }}</p>
      </div>
      <span :class="paymentClass(inv)" class="text-sm">{{ paymentLabel(inv) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Info Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
        <!-- Invoice Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
          <h3 class="font-bold text-dark mb-4">بيانات الفاتورة</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">رقم الفاتورة</span><span class="text-dark font-medium font-mono">{{ inv.name || '—' }}</span></div>
            <div>
              <span class="text-gray-500 block mb-0.5">العميل</span>
              <router-link v-if="inv.partner_id" :to="'/admin/parents/' + inv.partner_id" class="text-primary font-medium hover:underline">{{ inv.partner }}</router-link>
              <span v-else class="text-dark font-medium">{{ inv.partner || '—' }}</span>
            </div>
            <div><span class="text-gray-500 block mb-0.5">المرجع</span><span class="text-dark font-medium">{{ inv.ref || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الفاتورة</span><span class="text-dark font-medium">{{ inv.date || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الاستحقاق</span><span class="text-dark font-medium">{{ inv.due_date || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">حالة الفاتورة</span><span class="badge-info text-xs">{{ stateLabel(inv.state) }}</span></div>
          </div>
        </div>

        <!-- Financial Summary -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
          <h3 class="font-bold text-dark mb-2">الملخص المالي</h3>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">المبلغ قبل الضريبة</span>
            <span class="font-bold text-dark">{{ inv.amount_untaxed?.toLocaleString() }} ج.م</span>
          </div>
          <div v-if="inv.amount_tax" class="flex items-center justify-between text-sm">
            <span class="text-gray-500">الضريبة</span>
            <span class="font-bold text-dark">{{ inv.amount_tax?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm border-t border-gray-100 pt-3">
            <span class="text-gray-500">الإجمالي</span>
            <span class="font-bold text-dark text-lg">{{ inv.amount_total?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">المدفوع</span>
            <span class="font-bold text-green-600">{{ inv.amount_paid?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">المتبقي</span>
            <span :class="inv.amount_residual > 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">{{ inv.amount_residual?.toLocaleString() }} ج.م</span>
          </div>
        </div>
      </div>

      <!-- Invoice Lines -->
      <div class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-4">بنود الفاتورة</h3>
        <div v-if="!inv.lines?.length" class="text-gray-400 text-sm py-4 text-center">لا توجد بنود</div>
        <table v-else class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">البند</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">الكمية</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">سعر الوحدة</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">الإجمالي</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ln in inv.lines" :key="ln.id" class="border-t border-gray-50">
              <td class="py-2 px-3 text-dark">{{ ln.name }}</td>
              <td class="py-2 px-3 text-gray-600">{{ ln.quantity }}</td>
              <td class="py-2 px-3 text-gray-600">{{ ln.price_unit?.toLocaleString() }} ج.م</td>
              <td class="py-2 px-3 font-medium text-dark">{{ ln.price_subtotal?.toLocaleString() }} ج.م</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Payments -->
      <div v-if="inv.payments?.length" class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-4">المدفوعات</h3>
        <table class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">التاريخ</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">المبلغ</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">الوسيلة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in inv.payments" :key="p.id" class="border-t border-gray-50">
              <td class="py-2 px-3 text-gray-500 text-xs">{{ p.date }}</td>
              <td class="py-2 px-3 font-medium text-green-600">{{ p.amount?.toLocaleString() }} ج.م</td>
              <td class="py-2 px-3 text-gray-600">{{ p.journal || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Notes -->
      <div v-if="inv.narration" class="bg-white rounded-xl border border-gray-100 p-5">
        <h3 class="font-bold text-dark mb-2">ملاحظات</h3>
        <div class="text-sm text-gray-600" v-html="inv.narration"></div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { adminApi } from '@/services/adminApi'

const route = useRoute()
const inv = ref({})
const loading = ref(true)

const stateLabels = { draft: 'مسودة', posted: 'مؤكدة', cancel: 'ملغية' }
function stateLabel(v) { return stateLabels[v] || v || '—' }

function paymentLabel(inv) {
  if (inv.state === 'draft') return 'مسودة'
  if (inv.payment_state === 'paid') return 'مدفوعة'
  if (inv.due_date && inv.due_date < new Date().toISOString().slice(0, 10) && inv.payment_state !== 'paid') return 'متأخرة'
  return 'معلقة'
}

function paymentClass(inv) {
  if (inv.state === 'draft') return 'badge-info'
  if (inv.payment_state === 'paid') return 'badge-success'
  if (inv.due_date && inv.due_date < new Date().toISOString().slice(0, 10) && inv.payment_state !== 'paid')
    return 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'
  return 'badge-warning'
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getInvoice(route.params.id)
    inv.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>
