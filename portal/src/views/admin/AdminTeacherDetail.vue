<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/teachers" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">{{ teacher.name }}</h1>
        <p class="text-sm text-gray-500">{{ teacher.code }}</p>
      </div>
      <span :class="stateClass(teacher.state)" class="text-sm">{{ stateLabel(teacher.state) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="teacher.state === 'draft'" @click="doAction('activate')" class="btn-primary text-sm">تفعيل</button>
        <button v-if="teacher.state === 'active'" @click="doAction('on_leave')"
                class="bg-amber-50 text-amber-700 px-4 py-2 rounded-lg text-sm hover:bg-amber-100 transition-colors">إجازة</button>
        <button v-if="teacher.state === 'active' || teacher.state === 'on_leave'" @click="doAction('terminate')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">إنهاء الخدمة</button>
        <button v-if="teacher.state === 'terminated' || teacher.state === 'on_leave'" @click="doAction('reactivate')"
                class="btn-primary text-sm">إعادة تفعيل</button>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
        <!-- Personal Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
          <h3 class="font-bold text-dark mb-4">البيانات الشخصية</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">الاسم</span><span class="text-dark font-medium">{{ teacher.name }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الكود</span><span class="text-dark font-medium font-mono">{{ teacher.code || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الجنس</span><span class="text-dark font-medium">{{ teacher.gender === 'male' ? 'ذكر' : teacher.gender === 'female' ? 'أنثى' : '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الميلاد</span><span class="text-dark font-medium">{{ teacher.birthdate || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">العمر</span><span class="text-dark font-medium">{{ teacher.age || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">رقم الهوية</span><span class="text-dark font-medium font-mono">{{ teacher.id_number || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الهاتف</span><span class="text-dark font-medium font-mono direction-ltr">{{ teacher.phone || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الموبايل</span><span class="text-dark font-medium font-mono direction-ltr">{{ teacher.mobile || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">البريد</span><span class="text-dark font-medium">{{ teacher.email || '—' }}</span></div>
          </div>
        </div>

        <!-- Stats -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
          <h3 class="font-bold text-dark mb-2">إحصائيات</h3>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 text-sm">الفصول</span>
            <span class="font-bold text-dark">{{ teacher.class_count }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 text-sm">سجلات الحضور</span>
            <span class="font-bold text-dark">{{ teacher.attendance_count }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 text-sm">الراتب</span>
            <span class="font-bold text-dark">{{ teacher.salary?.toLocaleString() || 0 }} ج.م</span>
          </div>
        </div>
      </div>

      <!-- Job + Classes -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
        <!-- Job Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">بيانات العمل</h3>
          <div class="grid grid-cols-2 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">المسمى الوظيفي</span><span class="text-dark font-medium">{{ teacher.job_title || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">المؤهل</span><span class="text-dark font-medium">{{ teacher.qualification || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">القسم</span><span class="text-dark font-medium">{{ teacher.department || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الفرع</span><span class="text-dark font-medium">{{ teacher.branch || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">نوع الدوام</span><span class="text-dark font-medium">{{ shiftLabel(teacher.shift_type) }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ التعيين</span><span class="text-dark font-medium">{{ teacher.hire_date || '—' }}</span></div>
            <div v-if="teacher.end_date"><span class="text-gray-500 block mb-0.5">تاريخ الإنهاء</span><span class="text-dark font-medium text-red-600">{{ teacher.end_date }}</span></div>
          </div>
        </div>

        <!-- Assigned Classes -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">الفصول المسندة</h3>
          <div v-if="teacher.classes?.length" class="space-y-2">
            <div v-for="c in teacher.classes" :key="c.id" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <span class="text-xs font-bold text-primary">{{ c.name?.charAt(0) }}</span>
              </div>
              <span class="font-medium text-dark text-sm">{{ c.name }}</span>
            </div>
          </div>
          <p v-else class="text-gray-400 text-sm">لا توجد فصول مسندة</p>
        </div>
      </div>

      <!-- Portal Account -->
      <div class="bg-white rounded-xl border border-gray-100 p-5">
        <h3 class="font-bold text-dark mb-4">حساب البوابة</h3>
        <template v-if="teacher.portal_user">
          <div class="space-y-3 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-gray-500">اسم المستخدم</span>
              <span class="font-mono text-dark">{{ teacher.portal_user.username }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">النوع</span>
              <span class="badge-info text-xs">{{ userTypeLabel(teacher.portal_user.user_type) }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">الحالة</span>
              <span :class="teacher.portal_user.is_active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'">
                {{ teacher.portal_user.is_active ? 'مفعل' : 'معطل' }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">آخر دخول</span>
              <span class="text-dark text-xs">{{ teacher.portal_user.last_login || '—' }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">عدد مرات الدخول</span>
              <span class="text-dark">{{ teacher.portal_user.login_count }}</span>
            </div>
          </div>
          <div class="flex gap-2 mt-4">
            <button @click="togglePortalUser(teacher.portal_user.id)"
                    :class="teacher.portal_user.is_active ? 'bg-red-50 text-red-700 hover:bg-red-100' : 'btn-primary'"
                    class="text-sm px-3 py-1.5 rounded-lg transition-colors">
              {{ teacher.portal_user.is_active ? 'تعطيل الحساب' : 'تفعيل الحساب' }}
            </button>
            <button @click="showResetPw = teacher.portal_user.id" class="btn-outline text-sm">تغيير كلمة المرور</button>
          </div>
        </template>
        <template v-else>
          <p class="text-gray-400 text-sm mb-3">لا يوجد حساب على البوابة</p>
          <button @click="showCreatePu = true" class="btn-primary text-sm">إنشاء حساب</button>
        </template>
      </div>
    </template>

    <!-- Create Portal User Modal -->
    <div v-if="showCreatePu" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showCreatePu = false">
      <div class="bg-white rounded-2xl w-full max-w-md p-5">
        <h3 class="font-bold text-dark mb-4">إنشاء حساب بوابة للمعلم</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">اسم المستخدم</label>
            <input v-model="puForm.username" type="text" class="input-field text-sm w-full" :placeholder="teacher.phone || teacher.mobile || 'رقم الهاتف'" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
            <input v-model="puForm.password" type="text" class="input-field text-sm w-full" placeholder="6 أحرف على الأقل" />
          </div>
          <p v-if="puError" class="text-red-600 text-sm">{{ puError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showCreatePu = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="createTeacherPortalUser" :disabled="puSaving" class="btn-primary text-sm">إنشاء</button>
        </div>
      </div>
    </div>

    <!-- Reset Password Modal -->
    <div v-if="showResetPw" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showResetPw = null">
      <div class="bg-white rounded-2xl w-full max-w-md p-5">
        <h3 class="font-bold text-dark mb-4">تغيير كلمة المرور</h3>
        <input v-model="newPassword" type="text" class="input-field text-sm w-full" placeholder="كلمة المرور الجديدة" />
        <p v-if="puError" class="text-red-600 text-sm mt-2">{{ puError }}</p>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showResetPw = null" class="btn-outline text-sm">إلغاء</button>
          <button @click="resetPassword" :disabled="puSaving" class="btn-primary text-sm">حفظ</button>
        </div>
      </div>
    </div>

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
const teacher = ref({})
const loading = ref(true)
const actionMsg = ref('')

// Portal user
const showCreatePu = ref(false)
const showResetPw = ref(null)
const newPassword = ref('')
const puForm = ref({ username: '', password: '' })
const puError = ref('')
const puSaving = ref(false)

const stateLabels = { active: 'نشط', draft: 'مسودة', on_leave: 'إجازة', terminated: 'منتهي' }
const stateClasses = { active: 'badge-success', draft: 'badge-info', on_leave: 'badge-warning', terminated: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' }
const shiftLabels = { full_time: 'دوام كامل', part_time: 'دوام جزئي', contract: 'عقد' }
function stateLabel(v) { return stateLabels[v] || v || '—' }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function shiftLabel(v) { return shiftLabels[v] || '—' }
function userTypeLabel(v) { return { parent: 'ولي أمر', admin: 'مدير', teacher: 'معلم', student: 'طالب' }[v] || v }

async function fetchTeacher() {
  loading.value = true
  try {
    const { data } = await adminApi.getTeacher(route.params.id)
    teacher.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.teacherAction(route.params.id, action)
    actionMsg.value = data.message
    teacher.value.state = data.state
    teacher.value.active = data.active
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

// Portal user management
async function togglePortalUser(puId) {
  try {
    const { data } = await adminApi.togglePortalUser(puId)
    teacher.value.portal_user.is_active = data.is_active
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

async function createTeacherPortalUser() {
  if (!puForm.value.username || !puForm.value.password) {
    puError.value = 'جميع الحقول مطلوبة'
    return
  }
  if (puForm.value.password.length < 6) {
    puError.value = '6 أحرف على الأقل'
    return
  }
  puSaving.value = true
  puError.value = ''
  try {
    const { data } = await adminApi.createTeacherPortalUser(route.params.id, {
      username: puForm.value.username,
      password: puForm.value.password,
    })
    showCreatePu.value = false
    teacher.value.portal_user = data.portal_user
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    puError.value = e.response?.data?.error || 'حدث خطأ'
  } finally {
    puSaving.value = false
  }
}

async function resetPassword() {
  if (!newPassword.value || newPassword.value.length < 6) {
    puError.value = '6 أحرف على الأقل'
    return
  }
  puSaving.value = true
  puError.value = ''
  try {
    const { data } = await adminApi.resetPortalPassword(showResetPw.value, newPassword.value)
    showResetPw.value = null
    newPassword.value = ''
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    puError.value = e.response?.data?.error || 'حدث خطأ'
  } finally {
    puSaving.value = false
  }
}

onMounted(fetchTeacher)
</script>
