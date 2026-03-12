<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">منطقة الأطفال</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} {{ activeView === 'services' ? 'خدمة' : 'حجز' }}</p>
      </div>
      <div class="flex gap-2">
        <button @click="switchView('services')"
                :class="activeView === 'services' ? 'btn-primary' : 'btn-outline'" class="text-sm">
          الخدمات
        </button>
        <button @click="switchView('bookings')"
                :class="activeView === 'bookings' ? 'btn-primary' : 'btn-outline'" class="text-sm">
          الحجوزات
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text"
               :placeholder="activeView === 'services' ? 'بحث بالاسم...' : 'بحث بالطالب أو ولي الأمر...'"
               class="input-field text-sm w-full" />
      </div>
      <select v-if="activeView === 'bookings'" v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="draft">مسودة</option>
        <option value="confirmed">مؤكد</option>
        <option value="checked_in">وصل</option>
        <option value="checked_out">غادر</option>
        <option value="cancelled">ملغي</option>
        <option value="no_show">لم يحضر</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Services Table -->
    <div v-else-if="activeView === 'services'" class="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الخدمة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">نوع النشاط</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">التسعير</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">السعر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">السعة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">العمر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المدة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!services.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="s in services" :key="s.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-pink-50 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-pink-600">{{ activityIcon(s.activity_type) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ s.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="badge-info text-xs">{{ activityLabel(s.activity_type) }}</span>
              </td>
              <td class="py-3 px-4 text-gray-600 text-xs">{{ pricingLabel(s.pricing_type) }}</td>
              <td class="py-3 px-4 font-medium text-dark">{{ s.price?.toLocaleString() }} ج.م</td>
              <td class="py-3 px-4 text-center text-dark">{{ s.capacity }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ s.min_age }} - {{ s.max_age }} سنة</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ s.duration_minutes }} د</td>
              <td class="py-3 px-4">
                <span :class="s.active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'">
                  {{ s.active ? 'نشط' : 'معطل' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Bookings Table -->
    <div v-else class="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50/80">
            <tr>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الطالب</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ولي الأمر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الخدمة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الحجز</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المبلغ</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الدفع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!bookings.length">
              <td colspan="7" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="b in bookings" :key="b.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/kidsarea/booking/' + b.id)">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-primary">{{ b.student?.charAt(0) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ b.student }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-600">{{ b.parent || '—' }}</td>
              <td class="py-3 px-4 text-gray-600">{{ b.service || '—' }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ formatDate(b.booking_date) }}</td>
              <td class="py-3 px-4 font-medium text-dark">{{ b.amount?.toLocaleString() }} ج.م</td>
              <td class="py-3 px-4">
                <span :class="paymentClass(b.payment_status)">{{ paymentLabel(b.payment_status) }}</span>
              </td>
              <td class="py-3 px-4">
                <span :class="bookingStateClass(b.state)">{{ bookingStateLabel(b.state) }}</span>
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

const activeView = ref('services')
const search = ref('')
const filterStatus = ref('')
const services = ref([])
const bookings = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const activityLabels = { play: 'لعب', learning: 'تعلم', craft: 'أشغال يدوية', sport: 'رياضة' }
const activityIcons = { play: 'ل', learning: 'ت', craft: 'ي', sport: 'ر' }
const pricingLabels = { hourly: 'بالساعة', session: 'بالجلسة', package: 'باقة' }
const bookingStateLabels = { draft: 'مسودة', confirmed: 'مؤكد', checked_in: 'وصل', checked_out: 'غادر', cancelled: 'ملغي', no_show: 'لم يحضر' }
const bookingStateClasses = {
  draft: 'badge-info', confirmed: 'badge-success', checked_in: 'badge-success',
  checked_out: 'bg-gray-100 text-gray-700 text-xs px-2 py-0.5 rounded-full',
  cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full',
  no_show: 'badge-warning',
}
const paymentLabels = { pending: 'معلق', paid: 'مدفوع', refunded: 'مسترد' }
const paymentClasses = { pending: 'badge-warning', paid: 'badge-success', refunded: 'badge-info' }

function activityLabel(v) { return activityLabels[v] || v }
function activityIcon(v) { return activityIcons[v] || '؟' }
function pricingLabel(v) { return pricingLabels[v] || v }
function bookingStateLabel(v) { return bookingStateLabels[v] || v }
function bookingStateClass(v) { return bookingStateClasses[v] || 'badge-info' }
function paymentLabel(v) { return paymentLabels[v] || v }
function paymentClass(v) { return paymentClasses[v] || 'badge-info' }

function formatDate(dt) {
  if (!dt) return '—'
  return dt.replace('T', ' ').slice(0, 16)
}

function switchView(view) {
  activeView.value = view
  search.value = ''
  filterStatus.value = ''
  page.value = 1
  fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const params = { page: page.value, view: activeView.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getKidsArea(params)
    if (activeView.value === 'bookings') {
      bookings.value = data.bookings || []
    } else {
      services.value = data.services || []
    }
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load kids area:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchData()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchData()
  }, 400)
})

watch(filterStatus, () => {
  page.value = 1
  fetchData()
})

onMounted(fetchData)
</script>
