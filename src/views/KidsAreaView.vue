<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">منطقة الأطفال</h1>

    <!-- Tab Navigation -->
    <div class="flex gap-1 mb-6 bg-white rounded-xl p-1 border border-gray-200">
      <button
        @click="activeTab = 'services'"
        class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="activeTab === 'services' ? 'bg-primary-500 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
      >
        الخدمات والحجز
      </button>
      <button
        @click="activeTab = 'bookings'"
        class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="activeTab === 'bookings' ? 'bg-primary-500 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
      >
        حجوزاتي
      </button>
    </div>

    <!-- Services & Booking Tab -->
    <div v-if="activeTab === 'services'">
      <!-- Services Loading -->
      <div v-if="servicesLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
      </div>

      <template v-else>
        <!-- Services Section -->
        <div class="mb-8">
          <h2 class="text-lg font-bold mb-4">الخدمات المتاحة</h2>
          <div v-if="services.length === 0" class="card text-center py-10 text-gray-500">
            لا توجد خدمات متاحة حالياً
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="service in services" :key="service.id" class="card hover:shadow-md transition-shadow">
              <div class="flex items-start gap-3 mb-3">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                     :class="service.color ? `bg-${service.color}-100` : 'bg-purple-100'">
                  <svg class="w-6 h-6" :class="service.color ? `text-${service.color}-600` : 'text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-bold">{{ service.name }}</h3>
                  <p v-if="service.description" class="text-sm text-gray-500 mt-1">{{ service.description }}</p>
                </div>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span v-if="service.price" class="font-bold text-primary-600">{{ service.price.toLocaleString() }} ر.س</span>
                <span v-if="service.duration" class="text-gray-400">{{ service.duration }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Available Slots Section -->
        <div class="card mb-6">
          <h2 class="text-lg font-bold mb-4">المواعيد المتاحة</h2>

          <!-- Filters -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">التاريخ</label>
              <input
                type="date"
                v-model="selectedDate"
                class="input-field"
                :min="todayDate"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الخدمة</label>
              <select v-model="selectedServiceFilter" class="input-field">
                <option :value="null">جميع الخدمات</option>
                <option v-for="service in services" :key="service.id" :value="service.id">
                  {{ service.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Slots Loading -->
          <div v-if="slotsLoading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
          </div>

          <!-- Slots List -->
          <div v-else-if="availableSlots.length === 0" class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <p>لا توجد مواعيد متاحة في التاريخ المحدد</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div
              v-for="slot in availableSlots"
              :key="slot.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div>
                <p class="font-medium">{{ slot.service_name || 'خدمة' }}</p>
                <div class="flex items-center gap-2 text-sm text-gray-500 mt-1">
                  <span>{{ formatTime(slot.start_time) }} - {{ formatTime(slot.end_time) }}</span>
                  <span v-if="slot.available_spots" class="text-xs">
                    ({{ slot.available_spots }} {{ slot.available_spots === 1 ? 'مكان' : 'أماكن' }} متاحة)
                  </span>
                </div>
              </div>
              <button
                @click="openBookingModal(slot)"
                class="btn-primary text-sm px-4 py-2"
                :disabled="slot.available_spots === 0"
              >
                احجز
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- My Bookings Tab -->
    <div v-if="activeTab === 'bookings'">
      <div v-if="bookingsLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
      </div>

      <div v-else-if="bookings.length === 0" class="card text-center py-16">
        <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        <p class="text-gray-500 text-lg">لا توجد حجوزات</p>
        <button @click="activeTab = 'services'" class="btn-primary mt-4">تصفح الخدمات والحجز</button>
      </div>

      <div v-else class="space-y-4">
        <div v-for="booking in bookings" :key="booking.id" class="card">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="font-bold">{{ booking.service_name || 'حجز' }}</h3>
              <p class="text-sm text-gray-500">{{ booking.child_name }}</p>
            </div>
            <span :class="bookingStatusClass(booking.status)">
              {{ bookingStatusLabel(booking.status) }}
            </span>
          </div>

          <div class="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
            <span class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              {{ formatDate(booking.date) }}
            </span>
            <span class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ formatTime(booking.start_time) }} - {{ formatTime(booking.end_time) }}
            </span>
          </div>

          <!-- QR Code -->
          <div v-if="booking.qr_code && booking.status === 'confirmed'" class="bg-gray-50 rounded-lg p-4 text-center mb-4">
            <p class="text-sm text-gray-500 mb-2">رمز الدخول</p>
            <img :src="booking.qr_code" alt="QR Code" class="w-32 h-32 mx-auto"/>
            <p class="text-xs text-gray-400 mt-2">أظهر هذا الرمز عند الدخول</p>
          </div>
          <div v-else-if="booking.booking_code && booking.status === 'confirmed'" class="bg-gray-50 rounded-lg p-4 text-center mb-4">
            <p class="text-sm text-gray-500 mb-2">رمز الحجز</p>
            <p class="text-2xl font-bold text-primary-600 tracking-widest">{{ booking.booking_code }}</p>
          </div>

          <!-- Cancel Button -->
          <div v-if="booking.status === 'confirmed' || booking.status === 'pending'" class="flex justify-end">
            <button
              @click="cancelBooking(booking)"
              class="text-sm text-red-500 hover:text-red-700 hover:bg-red-50 px-4 py-2 rounded-lg transition-colors"
              :disabled="cancelling === booking.id"
            >
              <span v-if="cancelling === booking.id">جارٍ الإلغاء...</span>
              <span v-else>إلغاء الحجز</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50" @click="showBookingModal = false"></div>
      <div class="relative bg-white rounded-2xl max-w-md w-full shadow-2xl">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-6">تأكيد الحجز</h2>

          <!-- Booking Details -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <div class="flex justify-between py-2">
              <span class="text-gray-500">الخدمة</span>
              <span class="font-medium">{{ bookingSlot?.service_name }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="text-gray-500">التاريخ</span>
              <span class="font-medium">{{ formatDate(selectedDate) }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="text-gray-500">الوقت</span>
              <span class="font-medium">{{ formatTime(bookingSlot?.start_time) }} - {{ formatTime(bookingSlot?.end_time) }}</span>
            </div>
          </div>

          <!-- Select Child -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">اختر الطفل</label>
            <select v-model="selectedChildId" class="input-field">
              <option :value="null" disabled>اختر الطفل</option>
              <option v-for="child in children" :key="child.id" :value="child.id">
                {{ child.name }} - {{ child.arabic_name }}
              </option>
            </select>
          </div>

          <!-- Error -->
          <div v-if="bookingError" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-red-700">{{ bookingError }}</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-3">
            <button
              @click="confirmBooking"
              class="btn-primary flex-1"
              :disabled="!selectedChildId || bookingSubmitting"
            >
              <span v-if="bookingSubmitting">جارٍ الحجز...</span>
              <span v-else>تأكيد الحجز</span>
            </button>
            <button @click="showBookingModal = false" class="btn-secondary flex-1">إلغاء</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { kidsAreaApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const children = computed(() => authStore.children || [])

const activeTab = ref('services')

// Services
const services = ref([])
const servicesLoading = ref(false)

// Slots
const selectedDate = ref(new Date().toISOString().split('T')[0])
const selectedServiceFilter = ref(null)
const availableSlots = ref([])
const slotsLoading = ref(false)

// Bookings
const bookings = ref([])
const bookingsLoading = ref(false)
const cancelling = ref(null)

// Booking Modal
const showBookingModal = ref(false)
const bookingSlot = ref(null)
const selectedChildId = ref(null)
const bookingSubmitting = ref(false)
const bookingError = ref(null)

const todayDate = computed(() => new Date().toISOString().split('T')[0])

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    return new Date(dateStr).toLocaleDateString('ar-SA')
  } catch {
    return dateStr
  }
}

function formatTime(timeStr) {
  if (!timeStr) return '-'
  // Handle HH:mm or full datetime
  if (timeStr.includes('T')) {
    return new Date(timeStr).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })
  }
  return timeStr
}

function bookingStatusClass(status) {
  switch (status) {
    case 'confirmed': return 'badge-success'
    case 'pending': return 'badge-warning'
    case 'cancelled': return 'badge-danger'
    case 'completed': return 'badge-success'
    default: return 'badge-warning'
  }
}

function bookingStatusLabel(status) {
  const labels = {
    confirmed: 'مؤكد',
    pending: 'قيد الانتظار',
    cancelled: 'ملغي',
    completed: 'مكتمل',
    expired: 'منتهي',
  }
  return labels[status] || status
}

function openBookingModal(slot) {
  bookingSlot.value = slot
  selectedChildId.value = children.value.length === 1 ? children.value[0].id : null
  bookingError.value = null
  showBookingModal.value = true
}

async function confirmBooking() {
  if (!selectedChildId.value || !bookingSlot.value) return

  bookingSubmitting.value = true
  bookingError.value = null
  try {
    await kidsAreaApi.createBooking({
      slot_id: bookingSlot.value.id,
      child_id: selectedChildId.value,
      date: selectedDate.value,
    })
    showBookingModal.value = false
    // Refresh bookings
    fetchBookings()
    // Switch to bookings tab
    activeTab.value = 'bookings'
  } catch (err) {
    bookingError.value = err.response?.data?.message || 'حدث خطأ أثناء الحجز. يرجى المحاولة مرة أخرى.'
    console.error('Failed to create booking:', err)
  } finally {
    bookingSubmitting.value = false
  }
}

async function cancelBooking(booking) {
  if (!confirm('هل أنت متأكد من إلغاء هذا الحجز؟')) return

  cancelling.value = booking.id
  try {
    await kidsAreaApi.cancelBooking(booking.id)
    // Refresh bookings
    fetchBookings()
  } catch (err) {
    console.error('Failed to cancel booking:', err)
    alert(err.response?.data?.message || 'حدث خطأ أثناء إلغاء الحجز.')
  } finally {
    cancelling.value = null
  }
}

async function fetchServices() {
  servicesLoading.value = true
  try {
    const { data } = await kidsAreaApi.getServices()
    services.value = data?.services || data || []
  } catch (err) {
    console.error('Failed to fetch services:', err)
  } finally {
    servicesLoading.value = false
  }
}

async function fetchSlots() {
  slotsLoading.value = true
  try {
    const params = { date: selectedDate.value }
    if (selectedServiceFilter.value) {
      params.service_id = selectedServiceFilter.value
    }
    const { data } = await kidsAreaApi.getSlots(params)
    availableSlots.value = data?.slots || data || []
  } catch (err) {
    console.error('Failed to fetch slots:', err)
    availableSlots.value = []
  } finally {
    slotsLoading.value = false
  }
}

async function fetchBookings() {
  bookingsLoading.value = true
  try {
    const { data } = await kidsAreaApi.getBookings()
    bookings.value = data?.bookings || data || []
  } catch (err) {
    console.error('Failed to fetch bookings:', err)
  } finally {
    bookingsLoading.value = false
  }
}

// Watch for date/service filter changes to refresh slots
watch([selectedDate, selectedServiceFilter], () => {
  fetchSlots()
})

// Watch for tab change to load bookings
watch(activeTab, (newTab) => {
  if (newTab === 'bookings' && bookings.value.length === 0) {
    fetchBookings()
  }
})

onMounted(async () => {
  await fetchServices()
  fetchSlots()
  fetchBookings()
})
</script>
