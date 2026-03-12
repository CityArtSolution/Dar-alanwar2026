<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">المعلمين</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} معلم</p>
      </div>
      <button @click="openModal" class="btn-primary flex items-center gap-2 text-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        إضافة معلم
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم أو الكود أو الهاتف..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الحالات</option>
        <option value="active">نشط</option>
        <option value="draft">مسودة</option>
        <option value="on_leave">إجازة</option>
        <option value="terminated">منتهي</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الكود</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المعلم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الهاتف</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المسمى الوظيفي</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">القسم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">نوع الدوام</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ التعيين</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!teachers.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="t in teachers" :key="t.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/teachers/' + t.id)">
              <td class="py-3 px-4 font-mono text-xs text-gray-600">{{ t.code || '—' }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-emerald-600">{{ t.name?.charAt(0) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ t.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 font-mono text-xs direction-ltr">{{ t.phone || '—' }}</td>
              <td class="py-3 px-4 text-gray-600">{{ t.job_title || '—' }}</td>
              <td class="py-3 px-4 text-gray-600">{{ t.department || '—' }}</td>
              <td class="py-3 px-4">
                <span class="badge-info text-xs" v-if="t.shift_type">{{ shiftLabel(t.shift_type) }}</span>
                <span v-else class="text-gray-400">—</span>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ t.hire_date || '—' }}</td>
              <td class="py-3 px-4">
                <span :class="stateClass(t.state)">{{ stateLabel(t.state) }}</span>
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

    <!-- Add Teacher Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showModal = false">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-5 border-b border-gray-100">
          <h2 class="text-lg font-bold text-dark">إضافة معلم جديد</h2>
          <button @click="showModal = false" class="p-1.5 hover:bg-gray-100 rounded-lg">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-5 space-y-4">
          <!-- Row 1 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الاسم <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text" class="input-field text-sm w-full" placeholder="الاسم الكامل" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الجنس</label>
              <select v-model="form.gender" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="male">ذكر</option>
                <option value="female">أنثى</option>
              </select>
            </div>
          </div>
          <!-- Row 2 -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الهاتف</label>
              <input v-model="form.phone" type="text" class="input-field text-sm w-full" placeholder="رقم الهاتف" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الموبايل</label>
              <input v-model="form.mobile" type="text" class="input-field text-sm w-full" placeholder="رقم الموبايل" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">البريد الإلكتروني</label>
              <input v-model="form.email" type="email" class="input-field text-sm w-full" placeholder="email@example.com" />
            </div>
          </div>
          <!-- Row 3 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">المسمى الوظيفي</label>
              <input v-model="form.job_title" type="text" class="input-field text-sm w-full" placeholder="معلم قرآن" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">المؤهل</label>
              <input v-model="form.qualification" type="text" class="input-field text-sm w-full" placeholder="بكالوريوس" />
            </div>
          </div>
          <!-- Row 4 -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">القسم</label>
              <select v-model="form.department_id" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option v-for="d in opts.departments" :key="d.id" :value="d.id">{{ d.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الفرع</label>
              <select v-model="form.branch_id" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option v-for="b in opts.branches" :key="b.id" :value="b.id">{{ b.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">نوع الدوام</label>
              <select v-model="form.shift_type" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="full_time">دوام كامل</option>
                <option value="part_time">دوام جزئي</option>
                <option value="contract">عقد</option>
              </select>
            </div>
          </div>
          <!-- Row 5 -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ الميلاد</label>
              <input v-model="form.birthdate" type="date" class="input-field text-sm w-full" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ التعيين</label>
              <input v-model="form.hire_date" type="date" class="input-field text-sm w-full" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الراتب</label>
              <input v-model="form.salary" type="number" class="input-field text-sm w-full" placeholder="0" />
            </div>
          </div>
          <!-- Row 6 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">رقم الهوية</label>
            <input v-model="form.id_number" type="text" class="input-field text-sm w-full" placeholder="رقم الهوية الوطنية" />
          </div>

          <p v-if="formError" class="text-red-600 text-sm">{{ formError }}</p>
          <p v-if="formSuccess" class="text-green-600 text-sm">{{ formSuccess }}</p>
        </div>
        <div class="flex items-center justify-end gap-3 p-5 border-t border-gray-100">
          <button @click="showModal = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="submitTeacher" :disabled="saving" class="btn-primary text-sm flex items-center gap-2">
            <div v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ saving ? 'جاري الحفظ...' : 'حفظ المعلم' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { adminApi } from '@/services/adminApi'

const search = ref('')
const filterStatus = ref('')
const teachers = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const showModal = ref(false)
const saving = ref(false)
const formError = ref('')
const formSuccess = ref('')
const opts = ref({ departments: [], branches: [] })

const emptyForm = () => ({
  name: '', gender: '', phone: '', mobile: '', email: '',
  job_title: '', qualification: '', department_id: '', branch_id: '',
  shift_type: '', birthdate: '', hire_date: '', salary: '', id_number: '',
})
const form = ref(emptyForm())

const stateLabels = { active: 'نشط', draft: 'مسودة', on_leave: 'إجازة', terminated: 'منتهي' }
const stateClasses = {
  active: 'badge-success',
  draft: 'badge-info',
  on_leave: 'badge-warning',
  terminated: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full',
}
const shiftLabels = { full_time: 'دوام كامل', part_time: 'دوام جزئي', contract: 'عقد' }

function stateLabel(v) { return stateLabels[v] || v }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function shiftLabel(v) { return shiftLabels[v] || v }

async function openModal() {
  showModal.value = true
  form.value = emptyForm()
  formError.value = ''
  formSuccess.value = ''
  if (!opts.value.departments.length) {
    try {
      const { data } = await adminApi.getOptions()
      opts.value = data
    } catch (e) {
      console.error('Failed to load options:', e)
    }
  }
}

async function submitTeacher() {
  if (!form.value.name) {
    formError.value = 'اسم المعلم مطلوب'
    return
  }
  saving.value = true
  formError.value = ''
  formSuccess.value = ''
  try {
    const payload = {}
    for (const [k, v] of Object.entries(form.value)) {
      if (v) payload[k] = v
    }
    const { data } = await adminApi.createTeacher(payload)
    formSuccess.value = data.message || 'تم إضافة المعلم بنجاح'
    setTimeout(() => {
      showModal.value = false
      page.value = 1
      fetchTeachers()
    }, 1000)
  } catch (e) {
    formError.value = e.response?.data?.error || 'حدث خطأ أثناء الحفظ'
  } finally {
    saving.value = false
  }
}

async function fetchTeachers() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getTeachers(params)
    teachers.value = data.teachers || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load teachers:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchTeachers()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchTeachers()
  }, 400)
})

watch(filterStatus, () => {
  page.value = 1
  fetchTeachers()
})

onMounted(fetchTeachers)
</script>
