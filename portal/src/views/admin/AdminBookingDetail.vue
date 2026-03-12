<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/kids-area" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">حجز — {{ booking.student }}</h1>
        <p class="text-sm text-gray-500">{{ booking.slot?.service || '' }}</p>
      </div>
      <span :class="stateClass(booking.state)" class="text-sm">{{ stateLabel(booking.state) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="booking.state === 'draft'" @click="doAction('confirm')" class="btn-primary text-sm">تأكيد</button>
        <button v-if="booking.state === 'confirmed'" @click="doAction('check_in')"
                class="bg-green-50 text-green-700 px-4 py-2 rounded-lg text-sm hover:bg-green-100 transition-colors">تسجيل وصول</button>
        <button v-if="booking.state === 'checked_in'" @click="doAction('check_out')"
                class="bg-blue-50 text-blue-700 px-4 py-2 rounded-lg text-sm hover:bg-blue-100 transition-colors">تسجيل مغادرة</button>
        <button v-if="booking.state !== 'cancelled' && booking.state !== 'checked_out'" @click="doAction('cancel')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">إلغاء</button>
        <button v-if="booking.state === 'confirmed'" @click="doAction('no_show')"
                class="bg-amber-50 text-amber-700 px-4 py-2 rounded-lg text-sm hover:bg-amber-100 transition-colors">لم يحضر</button>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
        <!-- Booking Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">بيانات الحجز</h3>
          <div class="grid grid-cols-2 gap-y-4 gap-x-6 text-sm">
            <div>
              <span class="text-gray-500 block mb-0.5">الطالب</span>
              <router-link v-if="booking.student_id" :to="'/admin/students/' + booking.student_id" class="text-primary font-medium hover:underline">{{ booking.student }}</router-link>
              <span v-else class="text-dark font-medium">{{ booking.student || '—' }}</span>
            </div>
            <div>
              <span class="text-gray-500 block mb-0.5">ولي الأمر</span>
              <router-link v-if="booking.parent_id" :to="'/admin/parents/' + booking.parent_id" class="text-primary font-medium hover:underline">{{ booking.parent }}</router-link>
              <span v-else class="text-dark font-medium">{{ booking.parent || '—' }}</span>
            </div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الحجز</span><span class="text-dark font-medium">{{ formatDate(booking.booking_date) }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">المبلغ</span><span class="text-dark font-medium font-bold">{{ booking.amount?.toLocaleString() }} ج.م</span></div>
            <div><span class="text-gray-500 block mb-0.5">حالة الدفع</span><span :class="paymentClass(booking.payment_status)">{{ paymentLabel(booking.payment_status) }}</span></div>
            <div v-if="booking.qr_code"><span class="text-gray-500 block mb-0.5">كود QR</span><span class="text-dark font-mono text-xs">{{ booking.qr_code }}</span></div>
          </div>
          <div v-if="booking.notes" class="mt-4 pt-4 border-t border-gray-100">
            <span class="text-gray-500 block mb-1 text-sm">ملاحظات</span>
            <p class="text-sm text-dark">{{ booking.notes }}</p>
          </div>
        </div>

        <!-- Slot Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">بيانات الفترة</h3>
          <div v-if="booking.slot" class="grid grid-cols-2 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">الخدمة</span><span class="text-dark font-medium">{{ booking.slot.service || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">التاريخ</span><span class="text-dark font-medium">{{ booking.slot.date || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">من</span><span class="text-dark font-medium">{{ formatHour(booking.slot.time_from) }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">إلى</span><span class="text-dark font-medium">{{ formatHour(booking.slot.time_to) }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">السعة</span><span class="text-dark font-medium">{{ booking.slot.capacity }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">المحجوز</span><span class="text-dark font-medium">{{ booking.slot.booked_count }}</span></div>
            <div v-if="booking.slot.supervisor"><span class="text-gray-500 block mb-0.5">المشرف</span><span class="text-dark font-medium">{{ booking.slot.supervisor }}</span></div>
          </div>
          <p v-else class="text-gray-400 text-sm">لا توجد بيانات فترة</p>
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
const booking = ref({})
const loading = ref(true)
const actionMsg = ref('')

const stateLabels = { draft: 'مسودة', confirmed: 'مؤكد', checked_in: 'وصل', checked_out: 'غادر', cancelled: 'ملغي', no_show: 'لم يحضر' }
const stateClasses = {
  draft: 'badge-info', confirmed: 'badge-success', checked_in: 'badge-success',
  checked_out: 'bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded-full',
  cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full', no_show: 'badge-warning',
}
const paymentLabels = { pending: 'معلق', paid: 'مدفوع', refunded: 'مسترد' }
const paymentClasses = { pending: 'badge-warning', paid: 'badge-success', refunded: 'badge-info' }

function stateLabel(v) { return stateLabels[v] || v || '—' }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function paymentLabel(v) { return paymentLabels[v] || v || '—' }
function paymentClass(v) { return paymentClasses[v] || 'badge-info' }

function formatDate(dt) {
  if (!dt) return '—'
  return dt.replace('T', ' ').slice(0, 16)
}

function formatHour(h) {
  if (!h && h !== 0) return '—'
  const hours = Math.floor(h)
  const mins = Math.round((h - hours) * 60)
  return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}`
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getBooking(route.params.id)
    booking.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.bookingAction(route.params.id, action)
    actionMsg.value = data.message
    booking.value.state = data.state
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

onMounted(fetchData)
</script>
