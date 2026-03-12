<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">مستخدمو البوابة</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} مستخدم</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4">
      <div class="flex flex-wrap gap-3">
        <div class="flex-1 min-w-[200px]">
          <input v-model="search" type="text" placeholder="بحث بالاسم أو الهاتف أو البريد..."
                 class="input-field text-sm w-full" />
        </div>
        <select v-model="filterType" class="input-field text-sm w-40">
          <option value="">كل الأنواع</option>
          <option value="parent">ولي أمر</option>
          <option value="teacher">معلم</option>
          <option value="student">طالب</option>
          <option value="admin">مدير</option>
        </select>
        <select v-model="filterStatus" class="input-field text-sm w-36">
          <option value="">كل الحالات</option>
          <option value="active">نشط</option>
          <option value="inactive">معطل</option>
        </select>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المستخدم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">اسم المستخدم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">النوع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">البريد</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">آخر دخول</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">عدد الدخول</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الإنشاء</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">إجراءات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!users.length">
              <td colspan="9" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="u in users" :key="u.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                       :class="typeColors[u.user_type]?.bg || 'bg-gray-100'">
                    <span class="text-xs font-bold" :class="typeColors[u.user_type]?.text || 'text-gray-600'">{{ u.name?.charAt(0) || '?' }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ u.name || '—' }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 font-mono text-xs direction-ltr">{{ u.username }}</td>
              <td class="py-3 px-4">
                <span class="text-xs px-2 py-1 rounded-lg font-medium"
                      :class="typeColors[u.user_type]?.badge || 'bg-gray-100 text-gray-600'">
                  {{ typeLabels[u.user_type] || u.user_type }}
                </span>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">{{ u.email || '—' }}</td>
              <td class="py-3 px-4">
                <span :class="u.is_active ? 'badge-success' : 'badge-danger'">
                  {{ u.is_active ? 'نشط' : 'معطل' }}
                </span>
              </td>
              <td class="py-3 px-4 text-gray-400 text-xs">{{ u.last_login || '—' }}</td>
              <td class="py-3 px-4 text-center text-gray-600">{{ u.login_count }}</td>
              <td class="py-3 px-4 text-gray-400 text-xs">{{ u.create_date }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-1">
                  <!-- Toggle Active -->
                  <button @click="toggleUser(u)" :title="u.is_active ? 'تعطيل' : 'تفعيل'"
                          class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                    <svg class="w-4 h-4" :class="u.is_active ? 'text-red-500' : 'text-green-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path v-if="u.is_active" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </button>
                  <!-- Reset Password -->
                  <button @click="openResetPassword(u)" title="تغيير كلمة المرور"
                          class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                    <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                    </svg>
                  </button>
                </div>
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

    <!-- Reset Password Modal -->
    <div v-if="resetModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="resetModal = false">
      <div class="bg-white rounded-2xl w-full max-w-md">
        <div class="flex items-center justify-between p-5 border-b border-gray-100">
          <h2 class="text-lg font-bold text-dark">تغيير كلمة المرور</h2>
          <button @click="resetModal = false" class="p-1.5 hover:bg-gray-100 rounded-lg">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-5 space-y-4">
          <p class="text-sm text-gray-600">تغيير كلمة المرور للمستخدم: <strong>{{ resetUser?.name }}</strong> ({{ resetUser?.username }})</p>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">كلمة المرور الجديدة <span class="text-red-500">*</span></label>
            <input v-model="newPassword" type="text" class="input-field text-sm w-full" placeholder="6 أحرف على الأقل" />
          </div>
          <p v-if="resetError" class="text-red-600 text-sm">{{ resetError }}</p>
          <p v-if="resetSuccess" class="text-green-600 text-sm">{{ resetSuccess }}</p>
        </div>
        <div class="flex items-center justify-end gap-3 p-5 border-t border-gray-100">
          <button @click="resetModal = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="submitResetPassword" :disabled="resetting" class="btn-primary text-sm flex items-center gap-2">
            <div v-if="resetting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ resetting ? 'جاري التغيير...' : 'تغيير كلمة المرور' }}
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
const filterType = ref('')
const filterStatus = ref('')
const users = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const typeLabels = {
  parent: 'ولي أمر',
  teacher: 'معلم',
  student: 'طالب',
  admin: 'مدير',
}

const typeColors = {
  parent: { bg: 'bg-secondary/10', text: 'text-secondary', badge: 'bg-secondary/10 text-secondary' },
  teacher: { bg: 'bg-accent/10', text: 'text-accent-600', badge: 'bg-accent/10 text-accent-600' },
  student: { bg: 'bg-primary/10', text: 'text-primary', badge: 'bg-primary/10 text-primary' },
  admin: { bg: 'bg-red-50', text: 'text-red-600', badge: 'bg-red-50 text-red-600' },
}

// Reset password modal
const resetModal = ref(false)
const resetUser = ref(null)
const newPassword = ref('')
const resetError = ref('')
const resetSuccess = ref('')
const resetting = ref(false)

function openResetPassword(user) {
  resetUser.value = user
  newPassword.value = ''
  resetError.value = ''
  resetSuccess.value = ''
  resetModal.value = true
}

async function submitResetPassword() {
  if (!newPassword.value || newPassword.value.length < 6) {
    resetError.value = 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'
    return
  }
  resetting.value = true
  resetError.value = ''
  resetSuccess.value = ''
  try {
    const { data } = await adminApi.resetPortalPassword(resetUser.value.id, newPassword.value)
    resetSuccess.value = data.message || 'تم تغيير كلمة المرور بنجاح'
    setTimeout(() => { resetModal.value = false }, 1000)
  } catch (e) {
    resetError.value = e.response?.data?.error || 'حدث خطأ'
  } finally {
    resetting.value = false
  }
}

async function toggleUser(user) {
  try {
    const { data } = await adminApi.togglePortalUser(user.id)
    user.is_active = data.is_active
  } catch (e) {
    console.error('Toggle failed:', e)
  }
}

async function fetchUsers() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterType.value) params.user_type = filterType.value
    if (filterStatus.value) params.status = filterStatus.value
    const { data } = await adminApi.getPortalUsers(params)
    users.value = data.users || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load portal users:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchUsers()
}

watch([search, filterType, filterStatus], () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchUsers()
  }, 400)
})

onMounted(fetchUsers)
</script>
