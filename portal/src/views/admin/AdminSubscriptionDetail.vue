<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/subscriptions" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">اشتراك — {{ sub.student }}</h1>
        <p class="text-sm text-gray-500">{{ sub.subscription_type }}</p>
      </div>
      <span :class="statusClass(sub.status)" class="text-sm">{{ statusLabel(sub.status) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="sub.status === 'draft'" @click="doAction('activate')" class="btn-primary text-sm">تفعيل</button>
        <button v-if="sub.status === 'active'" @click="doAction('expire')"
                class="bg-amber-50 text-amber-700 px-4 py-2 rounded-lg text-sm hover:bg-amber-100 transition-colors">إنهاء</button>
        <button v-if="sub.status !== 'cancelled'" @click="doAction('cancel')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">إلغاء</button>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
        <!-- Subscription Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
          <h3 class="font-bold text-dark mb-4">بيانات الاشتراك</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
            <div>
              <span class="text-gray-500 block mb-0.5">الطالب</span>
              <router-link v-if="sub.student_id" :to="'/admin/students/' + sub.student_id" class="text-primary font-medium hover:underline">{{ sub.student }}</router-link>
              <span v-else class="text-dark font-medium">{{ sub.student || '—' }}</span>
            </div>
            <div><span class="text-gray-500 block mb-0.5">كود الطالب</span><span class="text-dark font-medium font-mono">{{ sub.student_code || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">نوع الاشتراك</span><span class="text-dark font-medium">{{ sub.subscription_type || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">خطة الدفع</span><span class="text-dark font-medium">{{ sub.payment_plan || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">العام الدراسي</span><span class="text-dark font-medium">{{ sub.academic_year || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ البدء</span><span class="text-dark font-medium">{{ sub.start_date || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الانتهاء</span><span class="text-dark font-medium">{{ sub.end_date || '—' }}</span></div>
          </div>
        </div>

        <!-- Financial Summary -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
          <h3 class="font-bold text-dark mb-2">الملخص المالي</h3>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">الإجمالي</span>
            <span class="font-bold text-dark">{{ sub.total_amount?.toLocaleString() }} ج.م</span>
          </div>
          <div v-if="sub.discount_amount" class="flex items-center justify-between text-sm">
            <span class="text-gray-500">الخصم</span>
            <span class="font-bold text-green-600">-{{ sub.discount_amount?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm border-t border-gray-100 pt-3">
            <span class="text-gray-500">الصافي</span>
            <span class="font-bold text-dark">{{ sub.net_amount?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">المدفوع</span>
            <span class="font-bold text-green-600">{{ sub.paid_amount?.toLocaleString() }} ج.م</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">المتبقي</span>
            <span :class="sub.remaining_amount > 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">{{ sub.remaining_amount?.toLocaleString() }} ج.م</span>
          </div>
        </div>
      </div>

      <!-- Installments -->
      <div class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-4">الأقساط ({{ sub.installment_count }})</h3>
        <div v-if="!sub.installments?.length" class="text-gray-400 text-sm py-4 text-center">لا توجد أقساط</div>
        <table v-else class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">#</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">تاريخ الاستحقاق</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">المبلغ</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">المدفوع</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">المتبقي</th>
              <th class="text-right py-2 px-3 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inst in sub.installments" :key="inst.id" class="border-t border-gray-50">
              <td class="py-2 px-3 text-dark">{{ inst.sequence }}</td>
              <td class="py-2 px-3 text-gray-500 text-xs">{{ inst.due_date }}</td>
              <td class="py-2 px-3 font-medium text-dark">{{ inst.amount?.toLocaleString() }} ج.م</td>
              <td class="py-2 px-3 text-green-600">{{ inst.paid_amount?.toLocaleString() }} ج.م</td>
              <td class="py-2 px-3" :class="inst.remaining_amount > 0 ? 'text-red-600' : 'text-green-600'">{{ inst.remaining_amount?.toLocaleString() }} ج.م</td>
              <td class="py-2 px-3"><span :class="inst.is_paid ? 'badge-success' : 'badge-warning'">{{ inst.is_paid ? 'مدفوع' : 'غير مدفوع' }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Notes -->
      <div v-if="sub.notes" class="bg-white rounded-xl border border-gray-100 p-5">
        <h3 class="font-bold text-dark mb-2">ملاحظات</h3>
        <p class="text-sm text-gray-600">{{ sub.notes }}</p>
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
const sub = ref({})
const loading = ref(true)
const actionMsg = ref('')

const statusLabels = { draft: 'مسودة', active: 'نشط', expired: 'منتهي', cancelled: 'ملغي' }
const statusClasses = { draft: 'badge-info', active: 'badge-success', expired: 'bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded-full', cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' }
const instStateLabels = { draft: 'غير مدفوع', paid: 'مدفوع', partial: 'جزئي', overdue: 'متأخر' }
const instStateClasses = { draft: 'badge-warning', paid: 'badge-success', partial: 'badge-info', overdue: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' }

function statusLabel(v) { return statusLabels[v] || v || '—' }
function statusClass(v) { return statusClasses[v] || 'badge-info' }
function instStateLabel(v) { return instStateLabels[v] || v || '—' }
function instStateClass(v) { return instStateClasses[v] || 'badge-info' }

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getSubscription(route.params.id)
    sub.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.subscriptionAction(route.params.id, action)
    actionMsg.value = data.message
    sub.value.status = data.status
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

onMounted(fetchData)
</script>
