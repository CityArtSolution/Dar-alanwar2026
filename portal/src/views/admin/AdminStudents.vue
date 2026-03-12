<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">إدارة الطلاب</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} طالب مسجل</p>
      </div>
      <button @click="openModal" class="btn-primary flex items-center gap-2 text-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        إضافة طالب
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم أو الرقم..."
               class="input-field text-sm" />
      </div>
      <select v-model="filterDept" class="input-field text-sm w-auto min-w-[150px]">
        <option value="">كل الأقسام</option>
        <option value="tahfiz">تحفيظ</option>
        <option value="languages">لغات</option>
      </select>
      <select v-model="filterStatus" class="input-field text-sm w-auto min-w-[130px]">
        <option value="">كل الحالات</option>
        <option value="enrolled">مسجل</option>
        <option value="new">جديد</option>
        <option value="graduated">متخرج</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الطالب</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الرقم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">القسم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الفصل</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ولي الأمر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحضور</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!students.length">
              <td colspan="8" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="s in students" :key="s.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/students/' + s.id)">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-primary">{{ s.name?.charAt(0) }}</span>
                  </div>
                  <div>
                    <p class="font-medium text-dark">{{ s.name }}</p>
                    <p class="text-[11px] text-gray-400">{{ s.arabic_name }}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 font-mono text-xs">{{ s.code }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.department }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.class_name }}</td>
              <td class="py-3 px-4 text-gray-600">{{ s.parent_name }}</td>
              <td class="py-3 px-4">
                <span :class="s.state === 'enrolled' ? 'badge-success' : s.state === 'new' ? 'badge-info' : 'badge-warning'">
                  {{ stateLabel(s.state) }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div class="h-full rounded-full" :class="s.attendance > 80 ? 'bg-green-500' : s.attendance > 60 ? 'bg-yellow-500' : 'bg-red-500'"
                         :style="{ width: s.attendance + '%' }"></div>
                  </div>
                  <span class="text-xs text-gray-500">{{ s.attendance }}%</span>
                </div>
              </td>
              <td class="py-3 px-4">
                <button class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
                  </svg>
                </button>
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

    <!-- Add Student Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showModal = false">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-5 border-b border-gray-100">
          <h2 class="text-lg font-bold text-dark">إضافة طالب جديد</h2>
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
              <label class="block text-sm font-medium text-gray-700 mb-1">الاسم بالعربي <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text" class="input-field text-sm w-full" placeholder="الاسم الكامل" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الاسم بالإنجليزي</label>
              <input v-model="form.arabic_name" type="text" class="input-field text-sm w-full" placeholder="Full Name" />
            </div>
          </div>
          <!-- Row 2 -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الجنس</label>
              <select v-model="form.gender" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="male">ذكر</option>
                <option value="female">أنثى</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ الميلاد</label>
              <input v-model="form.birthdate" type="date" class="input-field text-sm w-full" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الفترة</label>
              <select v-model="form.period" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="morning">صباحي</option>
                <option value="afternoon">مسائي</option>
                <option value="full_day">يوم كامل</option>
              </select>
            </div>
          </div>
          <!-- Row 3 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">القسم</label>
              <select v-model="form.department_id" class="input-field text-sm w-full">
                <option value="">اختر القسم</option>
                <option v-for="d in options.departments" :key="d.id" :value="d.id">{{ d.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الفصل</label>
              <select v-model="form.class_id" class="input-field text-sm w-full">
                <option value="">اختر الفصل</option>
                <option v-for="c in filteredClasses" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
          </div>
          <!-- Row 4 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الأب</label>
              <select v-model="form.father_id" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option v-for="g in options.guardians" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الأم</label>
              <select v-model="form.mother_id" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option v-for="g in options.guardians" :key="g.id" :value="g.id">{{ g.name }}</option>
              </select>
            </div>
          </div>
          <!-- Row 5 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الهاتف</label>
              <input v-model="form.phone" type="text" class="input-field text-sm w-full" placeholder="رقم الهاتف" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الفرع</label>
              <select v-model="form.branch_id" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option v-for="b in options.branches" :key="b.id" :value="b.id">{{ b.name }}</option>
              </select>
            </div>
          </div>

          <!-- Error -->
          <p v-if="formError" class="text-red-600 text-sm">{{ formError }}</p>
          <!-- Success -->
          <p v-if="formSuccess" class="text-green-600 text-sm">{{ formSuccess }}</p>
        </div>
        <div class="flex items-center justify-end gap-3 p-5 border-t border-gray-100">
          <button @click="showModal = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="submitStudent" :disabled="saving" class="btn-primary text-sm flex items-center gap-2">
            <div v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ saving ? 'جاري الحفظ...' : 'حفظ الطالب' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { adminApi } from '@/services/adminApi'

const search = ref('')
const filterDept = ref('')
const filterStatus = ref('')

const students = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const showModal = ref(false)
const saving = ref(false)
const formError = ref('')
const formSuccess = ref('')
const options = ref({ departments: [], classes: [], branches: [], guardians: [] })

const emptyForm = () => ({
  name: '', arabic_name: '', gender: '', birthdate: '', period: '',
  department_id: '', class_id: '', father_id: '', mother_id: '',
  phone: '', branch_id: '',
})
const form = ref(emptyForm())

const stateLabels = { enrolled: 'مسجل', new: 'جديد', draft: 'مسودة', graduated: 'متخرج', pending: 'معلق', suspended: 'موقوف', archived: 'مؤرشف' }
function stateLabel(v) { return stateLabels[v] || v }

const filteredClasses = computed(() => {
  if (!form.value.department_id) return options.value.classes
  return options.value.classes.filter(c => c.department_id === parseInt(form.value.department_id))
})

async function openModal() {
  showModal.value = true
  form.value = emptyForm()
  formError.value = ''
  formSuccess.value = ''
  if (!options.value.departments.length) {
    try {
      const { data } = await adminApi.getOptions()
      options.value = data
    } catch (e) {
      console.error('Failed to load options:', e)
    }
  }
}

async function submitStudent() {
  if (!form.value.name) {
    formError.value = 'اسم الطالب مطلوب'
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
    const { data } = await adminApi.createStudent(payload)
    formSuccess.value = data.message || 'تم إضافة الطالب بنجاح'
    setTimeout(() => {
      showModal.value = false
      page.value = 1
      fetchStudents()
    }, 1000)
  } catch (e) {
    formError.value = e.response?.data?.error || 'حدث خطأ أثناء الحفظ'
  } finally {
    saving.value = false
  }
}

async function fetchStudents() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterDept.value) params.department = filterDept.value === 'tahfiz' ? 'تحفيظ' : 'لغات'
    if (filterStatus.value) params.status = filterStatus.value

    const { data } = await adminApi.getStudents(params)
    students.value = data.students || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load students:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchStudents()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchStudents()
  }, 400)
})

watch([filterDept, filterStatus], () => {
  page.value = 1
  fetchStudents()
})

onMounted(fetchStudents)
</script>
