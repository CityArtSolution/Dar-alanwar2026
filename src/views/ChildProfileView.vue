<template>
  <div>
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <svg class="w-16 h-16 text-red-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
      </svg>
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchData" class="btn-primary">إعادة المحاولة</button>
    </div>

    <template v-else-if="child">
      <!-- Back Button -->
      <router-link to="/children" class="inline-flex items-center gap-2 text-gray-500 hover:text-primary-600 mb-4 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
        <span>العودة لقائمة الأبناء</span>
      </router-link>

      <!-- Profile Header -->
      <div class="card mb-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-5">
          <div class="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
            <img v-if="child.photo_url" :src="child.photo_url" :alt="child.name" class="w-20 h-20 rounded-full object-cover"/>
            <span v-else class="text-3xl font-bold text-primary-600">{{ child.name?.charAt(0) }}</span>
          </div>
          <div class="flex-1">
            <div class="flex flex-wrap items-center gap-3 mb-2">
              <h1 class="text-2xl font-bold">{{ child.name }}</h1>
              <span :class="stateClass(child.state)">{{ stateLabel(child.state) }}</span>
            </div>
            <p class="text-gray-500 mb-1">{{ child.arabic_name }}</p>
            <div class="flex flex-wrap gap-4 text-sm text-gray-500">
              <span v-if="child.code">الكود: {{ child.code }}</span>
              <span v-if="child.department?.name">القسم: {{ child.department.name }}</span>
              <span v-if="child.class?.name">الفصل: {{ child.class.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Navigation -->
      <div class="flex overflow-x-auto gap-1 mb-6 bg-white rounded-xl p-1 border border-gray-200">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="flex-shrink-0 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
          :class="activeTab === tab.key ? 'bg-primary-500 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'">
        <!-- Personal Info -->
        <div class="card mb-6">
          <h2 class="text-lg font-bold mb-4">المعلومات الشخصية</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الاسم الكامل</span>
              <span class="font-medium">{{ child.full_name || child.name }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الاسم بالعربية</span>
              <span class="font-medium">{{ child.arabic_name || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">تاريخ الميلاد</span>
              <span class="font-medium">{{ child.birth_date || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الجنس</span>
              <span class="font-medium">{{ child.gender === 'male' ? 'ذكر' : child.gender === 'female' ? 'أنثى' : '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الجنسية</span>
              <span class="font-medium">{{ child.nationality || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">رقم الهوية</span>
              <span class="font-medium">{{ child.id_number || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- Medical Info -->
        <div class="card mb-6">
          <h2 class="text-lg font-bold mb-4">المعلومات الصحية</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">فصيلة الدم</span>
              <span class="font-medium">{{ child.medical?.blood_type || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الحساسية</span>
              <span class="font-medium">{{ child.medical?.allergies || 'لا يوجد' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الأمراض المزمنة</span>
              <span class="font-medium">{{ child.medical?.chronic_conditions || 'لا يوجد' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">الأدوية</span>
              <span class="font-medium">{{ child.medical?.medications || 'لا يوجد' }}</span>
            </div>
          </div>
          <div v-if="child.medical?.notes" class="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
            <p class="text-sm text-yellow-800"><strong>ملاحظات طبية:</strong> {{ child.medical.notes }}</p>
          </div>
        </div>

        <!-- Guardian Info -->
        <div class="card">
          <h2 class="text-lg font-bold mb-4">معلومات ولي الأمر</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">اسم ولي الأمر</span>
              <span class="font-medium">{{ child.guardian?.name || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">صلة القرابة</span>
              <span class="font-medium">{{ child.guardian?.relation || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">رقم الهاتف</span>
              <span class="font-medium" dir="ltr">{{ child.guardian?.phone || '-' }}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="text-gray-500">البريد الإلكتروني</span>
              <span class="font-medium" dir="ltr">{{ child.guardian?.email || '-' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Attendance Tab -->
      <div v-if="activeTab === 'attendance'">
        <!-- Attendance Summary -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="stat-card">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-green-600">{{ attendanceSummary.present || 0 }}</p>
            <p class="text-sm text-gray-500">حاضر</p>
          </div>
          <div class="stat-card">
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-red-600">{{ attendanceSummary.absent || 0 }}</p>
            <p class="text-sm text-gray-500">غائب</p>
          </div>
          <div class="stat-card">
            <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-yellow-600">{{ attendanceSummary.late || 0 }}</p>
            <p class="text-sm text-gray-500">متأخر</p>
          </div>
          <div class="stat-card">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-blue-600">{{ attendanceSummary.excused || 0 }}</p>
            <p class="text-sm text-gray-500">بعذر</p>
          </div>
        </div>

        <!-- Loading attendance records -->
        <div v-if="attendanceLoading" class="flex justify-center py-10">
          <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
        </div>

        <!-- Attendance Records -->
        <div class="card">
          <h2 class="text-lg font-bold mb-4">سجل الحضور الأخير</h2>
          <div v-if="attendanceRecords.length === 0" class="text-center py-8 text-gray-500">
            لا توجد سجلات حضور
          </div>
          <div v-else class="divide-y divide-gray-100">
            <div v-for="record in attendanceRecords" :key="record.id" class="flex items-center justify-between py-3">
              <div class="flex items-center gap-3">
                <span
                  class="w-3 h-3 rounded-full flex-shrink-0"
                  :class="{
                    'bg-green-500': record.status === 'present',
                    'bg-red-500': record.status === 'absent',
                    'bg-yellow-500': record.status === 'late',
                    'bg-blue-500': record.status === 'excused',
                  }"
                ></span>
                <div>
                  <p class="font-medium">{{ formatDate(record.date) }}</p>
                  <p v-if="record.note" class="text-xs text-gray-400">{{ record.note }}</p>
                </div>
              </div>
              <span :class="attendanceStatusClass(record.status)">
                {{ attendanceStatusLabel(record.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Goals Tab -->
      <div v-if="activeTab === 'goals'">
        <div v-if="goalsLoading" class="flex justify-center py-10">
          <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
        </div>
        <div v-else-if="goals.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
          </svg>
          <p class="text-gray-500">لا توجد أهداف مسجلة حالياً</p>
        </div>
        <div v-else class="space-y-4">
          <div v-for="goal in goals" :key="goal.id" class="card">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h3 class="font-bold mb-1">{{ goal.title }}</h3>
                <p class="text-sm text-gray-500">{{ goal.description }}</p>
              </div>
              <span :class="goal.completed ? 'badge-success' : 'badge-warning'">
                {{ goal.completed ? 'مكتمل' : 'قيد التنفيذ' }}
              </span>
            </div>
            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div
                class="h-2.5 rounded-full transition-all duration-500"
                :class="goal.completed ? 'bg-green-500' : 'bg-primary-500'"
                :style="{ width: (goal.progress || 0) + '%' }"
              ></div>
            </div>
            <div class="flex justify-between items-center mt-2 text-xs text-gray-400">
              <span>{{ goal.category || '' }}</span>
              <span>{{ goal.progress || 0 }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Homework Tab -->
      <div v-if="activeTab === 'homework'">
        <div v-if="homeworkLoading" class="flex justify-center py-10">
          <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
        </div>
        <div v-else-if="homeworkList.length === 0" class="card text-center py-12">
          <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
          <p class="text-gray-500">لا توجد واجبات منزلية</p>
        </div>
        <div v-else class="card">
          <h2 class="text-lg font-bold mb-4">الواجبات المنزلية الأخيرة</h2>
          <div class="divide-y divide-gray-100">
            <div v-for="hw in homeworkList" :key="hw.id" class="py-4">
              <div class="flex items-start justify-between mb-2">
                <div>
                  <h3 class="font-medium">{{ hw.title }}</h3>
                  <p class="text-sm text-gray-500">{{ hw.subject || '' }}</p>
                </div>
                <div class="text-left">
                  <span v-if="hw.grade !== null && hw.grade !== undefined" class="text-lg font-bold" :class="gradeColor(hw.grade, hw.max_grade)">
                    {{ hw.grade }}<span class="text-sm text-gray-400">/{{ hw.max_grade || 100 }}</span>
                  </span>
                  <span v-else class="text-sm text-gray-400">لم يُقيّم بعد</span>
                </div>
              </div>
              <div class="flex items-center gap-4 text-xs text-gray-400">
                <span>تاريخ التسليم: {{ formatDate(hw.due_date) }}</span>
                <span :class="hw.submitted ? 'text-green-500' : 'text-red-500'">
                  {{ hw.submitted ? 'تم التسليم' : 'لم يسلّم' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financial Tab -->
      <div v-if="activeTab === 'financial'">
        <div v-if="financialLoading" class="flex justify-center py-10">
          <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
        </div>
        <template v-else>
          <!-- Subscriptions -->
          <div class="card mb-6">
            <h2 class="text-lg font-bold mb-4">الاشتراكات</h2>
            <div v-if="subscriptions.length === 0" class="text-center py-6 text-gray-500">
              لا توجد اشتراكات نشطة
            </div>
            <div v-else class="divide-y divide-gray-100">
              <div v-for="sub in subscriptions" :key="sub.id" class="py-4">
                <div class="flex items-center justify-between mb-2">
                  <div>
                    <h3 class="font-medium">{{ sub.name }}</h3>
                    <p class="text-sm text-gray-500">{{ sub.type || '' }}</p>
                  </div>
                  <span :class="sub.status === 'active' ? 'badge-success' : 'badge-warning'">
                    {{ sub.status === 'active' ? 'نشط' : sub.status === 'expired' ? 'منتهي' : sub.status }}
                  </span>
                </div>
                <div class="flex gap-4 text-sm text-gray-500">
                  <span>المبلغ: {{ sub.amount?.toLocaleString() || 0 }} ر.س</span>
                  <span>من: {{ formatDate(sub.start_date) }}</span>
                  <span>إلى: {{ formatDate(sub.end_date) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Installments -->
          <div class="card">
            <h2 class="text-lg font-bold mb-4">الأقساط</h2>
            <div v-if="installments.length === 0" class="text-center py-6 text-gray-500">
              لا توجد أقساط مستحقة
            </div>
            <div v-else class="divide-y divide-gray-100">
              <div v-for="inst in installments" :key="inst.id" class="flex items-center justify-between py-4">
                <div>
                  <h3 class="font-medium">{{ inst.description || 'قسط' }}</h3>
                  <p class="text-sm text-gray-500">تاريخ الاستحقاق: {{ formatDate(inst.due_date) }}</p>
                </div>
                <div class="flex items-center gap-3">
                  <span class="font-bold">{{ inst.amount?.toLocaleString() || 0 }} ر.س</span>
                  <span :class="inst.paid ? 'badge-success' : 'badge-danger'">
                    {{ inst.paid ? 'مدفوع' : 'غير مدفوع' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { childrenApi, attendanceApi, subscriptionsApi, invoicesApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const route = useRoute()
const authStore = useAuthStore()

const child = ref(null)
const loading = ref(false)
const error = ref(null)
const activeTab = ref('overview')

const tabs = [
  { key: 'overview', label: 'نظرة عامة' },
  { key: 'attendance', label: 'الحضور' },
  { key: 'goals', label: 'الأهداف' },
  { key: 'homework', label: 'الواجبات' },
  { key: 'financial', label: 'المالية' },
]

// Attendance
const attendanceSummary = ref({ present: 0, absent: 0, late: 0, excused: 0 })
const attendanceRecords = ref([])
const attendanceLoading = ref(false)

// Goals
const goals = ref([])
const goalsLoading = ref(false)

// Homework
const homeworkList = ref([])
const homeworkLoading = ref(false)

// Financial
const subscriptions = ref([])
const installments = ref([])
const financialLoading = ref(false)

function stateClass(state) {
  switch (state) {
    case 'enrolled': return 'badge-success'
    case 'graduated': return 'badge-success'
    case 'suspended': return 'badge-danger'
    default: return 'badge-warning'
  }
}

function stateLabel(state) {
  const labels = { enrolled: 'مسجل', graduated: 'متخرج', suspended: 'معلق', pending: 'قيد المراجعة', withdrawn: 'منسحب' }
  return labels[state] || state || '-'
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    return new Date(dateStr).toLocaleDateString('ar-SA')
  } catch {
    return dateStr
  }
}

function attendanceStatusClass(status) {
  switch (status) {
    case 'present': return 'badge-success'
    case 'absent': return 'badge-danger'
    case 'late': return 'badge-warning'
    case 'excused': return 'text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700'
    default: return 'badge-warning'
  }
}

function attendanceStatusLabel(status) {
  const labels = { present: 'حاضر', absent: 'غائب', late: 'متأخر', excused: 'بعذر' }
  return labels[status] || status
}

function gradeColor(grade, maxGrade) {
  const pct = (grade / (maxGrade || 100)) * 100
  if (pct >= 90) return 'text-green-600'
  if (pct >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

async function fetchData() {
  const childId = route.params.id
  loading.value = true
  error.value = null
  try {
    const { data } = await childrenApi.getDetail(childId)
    child.value = data
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل بيانات الطالب. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch child detail:', err)
  } finally {
    loading.value = false
  }
}

async function fetchAttendance() {
  const childId = route.params.id
  attendanceLoading.value = true
  try {
    const [summaryRes, recordsRes] = await Promise.all([
      attendanceApi.getSummary(childId),
      attendanceApi.getByStudent(childId, { limit: 30 }),
    ])
    attendanceSummary.value = summaryRes.data || { present: 0, absent: 0, late: 0, excused: 0 }
    attendanceRecords.value = recordsRes.data?.records || recordsRes.data || []
  } catch (err) {
    console.error('Failed to fetch attendance:', err)
  } finally {
    attendanceLoading.value = false
  }
}

async function fetchGoals() {
  const childId = route.params.id
  goalsLoading.value = true
  try {
    const { data } = await api.get(`/children/${childId}/goals`)
    goals.value = data.goals || data || []
  } catch (err) {
    console.error('Failed to fetch goals:', err)
  } finally {
    goalsLoading.value = false
  }
}

async function fetchHomework() {
  const childId = route.params.id
  homeworkLoading.value = true
  try {
    const { data } = await api.get(`/children/${childId}/homework`)
    homeworkList.value = data.homework || data || []
  } catch (err) {
    console.error('Failed to fetch homework:', err)
  } finally {
    homeworkLoading.value = false
  }
}

async function fetchFinancial() {
  const childId = route.params.id
  financialLoading.value = true
  try {
    const [subsRes, instRes] = await Promise.all([
      subscriptionsApi.getAll({ student_id: childId }),
      invoicesApi.getAll({ student_id: childId }),
    ])
    subscriptions.value = subsRes.data?.subscriptions || subsRes.data || []
    installments.value = instRes.data?.installments || instRes.data?.invoices || []
  } catch (err) {
    console.error('Failed to fetch financial data:', err)
  } finally {
    financialLoading.value = false
  }
}

// Fetch tab data on tab change
watch(activeTab, (newTab) => {
  if (newTab === 'attendance' && attendanceRecords.value.length === 0) {
    fetchAttendance()
  } else if (newTab === 'goals' && goals.value.length === 0) {
    fetchGoals()
  } else if (newTab === 'homework' && homeworkList.value.length === 0) {
    fetchHomework()
  } else if (newTab === 'financial' && subscriptions.value.length === 0 && installments.value.length === 0) {
    fetchFinancial()
  }
})

onMounted(() => {
  fetchData()
})
</script>
