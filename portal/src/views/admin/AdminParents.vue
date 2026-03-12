<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">أولياء الأمور</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} ولي أمر</p>
      </div>
      <button @click="openModal" class="btn-primary flex items-center gap-2 text-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        إضافة ولي أمر
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم أو الهاتف أو البريد..."
               class="input-field text-sm w-full" />
      </div>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ولي الأمر</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الهاتف</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">البريد</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">صلة القرابة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">عدد الأبناء</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الرصيد المستحق</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!parents.length">
              <td colspan="6" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="p in parents" :key="p.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/parents/' + p.id)">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-secondary/10 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-secondary">{{ p.name?.charAt(0) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ p.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 font-mono text-xs direction-ltr">{{ p.phone }}</td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ p.email || '—' }}</td>
              <td class="py-3 px-4 text-gray-600">
                <span class="badge-info text-xs" v-if="p.guardian_relation">{{ relationLabel(p.guardian_relation) }}</span>
                <span v-else class="text-gray-400">—</span>
              </td>
              <td class="py-3 px-4 text-center font-medium text-dark">{{ p.children_count }}</td>
              <td class="py-3 px-4">
                <span :class="p.children_balance_due > 0 ? 'text-red-600' : 'text-green-600'" class="font-medium">
                  {{ p.children_balance_due?.toLocaleString() || 0 }} ج.م
                </span>
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

    <!-- Add Parent Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showModal = false">
      <div class="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-5 border-b border-gray-100">
          <h2 class="text-lg font-bold text-dark">إضافة ولي أمر جديد</h2>
          <button @click="showModal = false" class="p-1.5 hover:bg-gray-100 rounded-lg">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-5 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">الاسم <span class="text-red-500">*</span></label>
            <input v-model="form.name" type="text" class="input-field text-sm w-full" placeholder="الاسم الكامل" />
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الهاتف</label>
              <input v-model="form.phone" type="text" class="input-field text-sm w-full" placeholder="01xxxxxxxxx" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">البريد الإلكتروني</label>
              <input v-model="form.email" type="email" class="input-field text-sm w-full" placeholder="email@example.com" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">صلة القرابة</label>
              <select v-model="form.guardian_relation" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="father">أب</option>
                <option value="mother">أم</option>
                <option value="guardian">ولي أمر</option>
                <option value="grandfather">جد</option>
                <option value="grandmother">جدة</option>
                <option value="uncle">عم / خال</option>
                <option value="aunt">عمة / خالة</option>
                <option value="other">أخرى</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الحالة الاجتماعية</label>
              <select v-model="form.parent_social_status" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="married">متزوج</option>
                <option value="divorced">مطلق</option>
                <option value="widowed">أرمل</option>
                <option value="separated">منفصل</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">رقم الهوية</label>
              <input v-model="form.id_number" type="text" class="input-field text-sm w-full" placeholder="رقم الهوية الوطنية" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">المستوى التعليمي</label>
              <select v-model="form.education_level" class="input-field text-sm w-full">
                <option value="">اختر</option>
                <option value="primary">ابتدائي</option>
                <option value="preparatory">إعدادي</option>
                <option value="secondary">ثانوي</option>
                <option value="university">جامعي</option>
                <option value="postgraduate">دراسات عليا</option>
                <option value="other">أخرى</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">جهة العمل</label>
            <input v-model="form.workplace" type="text" class="input-field text-sm w-full" placeholder="اسم جهة العمل" />
          </div>

          <p v-if="formError" class="text-red-600 text-sm">{{ formError }}</p>
          <p v-if="formSuccess" class="text-green-600 text-sm">{{ formSuccess }}</p>
        </div>
        <div class="flex items-center justify-end gap-3 p-5 border-t border-gray-100">
          <button @click="showModal = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="submitParent" :disabled="saving" class="btn-primary text-sm flex items-center gap-2">
            <div v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ saving ? 'جاري الحفظ...' : 'حفظ ولي الأمر' }}
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
const parents = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const showModal = ref(false)
const saving = ref(false)
const formError = ref('')
const formSuccess = ref('')

const emptyForm = () => ({
  name: '', phone: '', email: '', guardian_relation: '',
  parent_social_status: '', id_number: '', education_level: '', workplace: '',
})
const form = ref(emptyForm())

const relationLabels = {
  father: 'أب', mother: 'أم', guardian: 'ولي أمر', grandfather: 'جد',
  grandmother: 'جدة', uncle: 'عم / خال', aunt: 'عمة / خالة', other: 'أخرى',
}
function relationLabel(val) {
  return relationLabels[val] || val
}

function openModal() {
  showModal.value = true
  form.value = emptyForm()
  formError.value = ''
  formSuccess.value = ''
}

async function submitParent() {
  if (!form.value.name) {
    formError.value = 'اسم ولي الأمر مطلوب'
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
    const { data } = await adminApi.createParent(payload)
    formSuccess.value = data.message || 'تم إضافة ولي الأمر بنجاح'
    setTimeout(() => {
      showModal.value = false
      page.value = 1
      fetchParents()
    }, 1000)
  } catch (e) {
    formError.value = e.response?.data?.error || 'حدث خطأ أثناء الحفظ'
  } finally {
    saving.value = false
  }
}

async function fetchParents() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    const { data } = await adminApi.getParents(params)
    parents.value = data.parents || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load parents:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchParents()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchParents()
  }, 400)
})

onMounted(fetchParents)
</script>
