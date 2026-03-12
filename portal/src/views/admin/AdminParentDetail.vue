<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/parents" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">{{ parent.name }}</h1>
        <p class="text-sm text-gray-500">ولي أمر</p>
      </div>
      <span :class="parent.active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'" class="text-sm">
        {{ parent.active ? 'نشط' : 'مؤرشف' }}
      </span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="parent.active" @click="doAction('archive')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">أرشفة</button>
        <button v-else @click="doAction('reactivate')" class="btn-primary text-sm">إعادة تفعيل</button>
      </div>

      <!-- Tabs -->
      <div class="flex gap-1 mb-4 bg-white rounded-xl border border-gray-100 p-1">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
                :class="activeTab === tab.key ? 'bg-primary text-white' : 'text-gray-600 hover:bg-gray-50'"
                class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors">
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab: البيانات -->
      <div v-show="activeTab === 'info'">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          <!-- Personal Info -->
          <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
            <h3 class="font-bold text-dark mb-4">البيانات الشخصية</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
              <div><span class="text-gray-500 block mb-0.5">الاسم</span><span class="text-dark font-medium">{{ parent.name }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الهاتف</span><span class="text-dark font-medium font-mono direction-ltr">{{ parent.phone || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">البريد</span><span class="text-dark font-medium">{{ parent.email || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">صلة القرابة</span><span class="text-dark font-medium">{{ relationLabel(parent.guardian_relation) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">رقم الهوية</span><span class="text-dark font-medium font-mono">{{ parent.id_number || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الحالة الاجتماعية</span><span class="text-dark font-medium">{{ socialLabel(parent.parent_social_status) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">المستوى التعليمي</span><span class="text-dark font-medium">{{ educationLabel(parent.education_level) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">جهة العمل</span><span class="text-dark font-medium">{{ parent.workplace || '—' }}</span></div>
            </div>
          </div>

          <!-- Stats -->
          <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
            <h3 class="font-bold text-dark mb-2">إحصائيات</h3>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">عدد الأبناء</span>
              <span class="font-bold text-dark">{{ parent.children_count }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">الرصيد المستحق</span>
              <span :class="parent.children_balance_due > 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">
                {{ parent.children_balance_due?.toLocaleString() || 0 }} ج.م
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">إجمالي المدفوع</span>
              <span class="font-bold text-green-600">{{ parent.total_paid?.toLocaleString() || 0 }} ج.م</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">المتبقي</span>
              <span class="font-bold text-red-600">{{ parent.total_remaining?.toLocaleString() || 0 }} ج.م</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">حضور الأبناء</span>
              <span class="font-bold text-dark">{{ parent.children_attendance_pct || 0 }}%</span>
            </div>
          </div>
        </div>

        <!-- Children -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">الأبناء</h3>
          <div v-if="parent.children?.length" class="space-y-2">
            <div v-for="c in parent.children" :key="c.id"
                 @click="$router.push('/admin/students/' + c.id)"
                 class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors">
              <div class="w-9 h-9 bg-primary/10 rounded-lg flex items-center justify-center shrink-0">
                <span class="text-xs font-bold text-primary">{{ c.name?.charAt(0) }}</span>
              </div>
              <div class="flex-1">
                <p class="font-medium text-dark text-sm">{{ c.name }}</p>
                <p class="text-[11px] text-gray-400">{{ c.department }} · {{ c.class_name }}</p>
              </div>
              <span class="text-xs font-mono text-gray-400">{{ c.code }}</span>
              <span :class="c.state === 'enrolled' ? 'badge-success' : 'badge-info'" class="text-xs">
                {{ childStateLabel(c.state) }}
              </span>
            </div>
          </div>
          <p v-else class="text-gray-400 text-sm">لا يوجد أبناء مسجلين</p>
        </div>
      </div>

      <!-- Tab: اشتراكات الأبناء -->
      <div v-show="activeTab === 'subscriptions'">
        <div v-if="childrenDataLoading" class="flex items-center justify-center py-12">
          <div class="w-7 h-7 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
        <template v-else>
          <h3 class="font-bold text-dark mb-4">اشتراكات الأبناء</h3>

          <div v-if="!childrenData.length" class="bg-white rounded-xl border border-gray-100 p-8 text-center">
            <p class="text-gray-400">لا يوجد أبناء</p>
          </div>

          <div v-for="child in childrenData" :key="child.id" class="mb-6">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-7 h-7 bg-primary/10 rounded-lg flex items-center justify-center">
                <span class="text-xs font-bold text-primary">{{ child.name?.charAt(0) }}</span>
              </div>
              <h4 class="font-bold text-dark text-sm">{{ child.name }}</h4>
              <span class="text-xs text-gray-400 font-mono">{{ child.code }}</span>
            </div>

            <div v-if="!child.subscriptions?.length" class="bg-white rounded-xl border border-gray-100 p-4 text-center">
              <p class="text-gray-400 text-sm">لا توجد اشتراكات</p>
            </div>

            <div v-for="sub in child.subscriptions" :key="sub.id" class="bg-white rounded-xl border border-gray-100 p-4 mb-3">
              <div class="flex items-center justify-between mb-2">
                <div>
                  <span class="font-bold text-dark text-sm">{{ sub.type }}</span>
                  <span class="text-xs text-gray-400 mr-2">{{ sub.start_date }}</span>
                </div>
                <span :class="subStatusClass(sub.status)" class="text-xs">{{ subStatusLabel(sub.status) }}</span>
              </div>
              <div class="grid grid-cols-4 gap-2 text-xs">
                <div><span class="text-gray-500 block">الإجمالي</span><span class="font-bold text-dark">{{ sub.total_amount?.toLocaleString() }}</span></div>
                <div><span class="text-gray-500 block">الصافي</span><span class="font-bold text-dark">{{ sub.net_amount?.toLocaleString() }}</span></div>
                <div><span class="text-gray-500 block">المدفوع</span><span class="font-bold text-green-600">{{ sub.paid_amount?.toLocaleString() }}</span></div>
                <div><span class="text-gray-500 block">المتبقي</span><span class="font-bold text-red-600">{{ sub.remaining_amount?.toLocaleString() }}</span></div>
              </div>
              <!-- Installments -->
              <div v-if="sub.installments?.length" class="mt-3 pt-3 border-t border-gray-50">
                <table class="w-full text-xs">
                  <thead>
                    <tr class="text-gray-400">
                      <th class="text-right pb-1 font-medium">#</th>
                      <th class="text-right pb-1 font-medium">التاريخ</th>
                      <th class="text-right pb-1 font-medium">المبلغ</th>
                      <th class="text-right pb-1 font-medium">الحالة</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="inst in sub.installments" :key="inst.id" class="border-t border-gray-50">
                      <td class="py-1.5">{{ inst.sequence }}</td>
                      <td class="py-1.5">{{ inst.due_date }}</td>
                      <td class="py-1.5">{{ inst.amount?.toLocaleString() }}</td>
                      <td class="py-1.5">
                        <span :class="inst.is_paid ? 'text-green-600' : 'text-amber-600'" class="font-medium">{{ inst.is_paid ? 'مدفوع' : 'معلق' }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Tab: محتوى الأبناء -->
      <div v-show="activeTab === 'content'">
        <div v-if="childrenDataLoading" class="flex items-center justify-center py-12">
          <div class="w-7 h-7 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
        <template v-else>
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-dark">محتوى الأبناء</h3>
            <button @click="showGrantAll = true" class="btn-primary text-sm">منح محتوى للجميع</button>
          </div>

          <div v-if="!childrenData.length" class="bg-white rounded-xl border border-gray-100 p-8 text-center">
            <p class="text-gray-400">لا يوجد أبناء</p>
          </div>

          <div v-for="child in childrenData" :key="child.id" class="mb-6">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-7 h-7 bg-primary/10 rounded-lg flex items-center justify-center">
                <span class="text-xs font-bold text-primary">{{ child.name?.charAt(0) }}</span>
              </div>
              <h4 class="font-bold text-dark text-sm">{{ child.name }}</h4>
            </div>

            <div v-if="!child.content_access?.length" class="bg-white rounded-xl border border-gray-100 p-4 text-center">
              <p class="text-gray-400 text-sm">لا يوجد محتوى ممنوح</p>
            </div>

            <div v-else class="bg-white rounded-xl border border-gray-100 overflow-hidden">
              <table class="w-full text-sm">
                <thead>
                  <tr class="bg-gray-50 text-gray-500 text-xs">
                    <th class="text-right p-3 font-medium">المحتوى</th>
                    <th class="text-right p-3 font-medium">النوع</th>
                    <th class="text-right p-3 font-medium">تاريخ المنح</th>
                    <th class="text-right p-3 font-medium">الحالة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in child.content_access" :key="a.id" class="border-t border-gray-50">
                    <td class="p-3 text-dark font-medium">{{ a.content_name }}</td>
                    <td class="p-3 text-gray-500">{{ contentTypeLabel(a.content_type) }}</td>
                    <td class="p-3 text-dark">{{ a.granted_date }}</td>
                    <td class="p-3">
                      <span :class="a.is_active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'" class="text-xs">
                        {{ a.is_active ? 'نشط' : 'ملغى' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </template>
      </div>

      <!-- Tab: الحساب -->
      <div v-show="activeTab === 'account'">
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">حساب البوابة</h3>
          <template v-if="parent.portal_user">
            <div class="space-y-3 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-gray-500">اسم المستخدم</span>
                <span class="font-mono text-dark">{{ parent.portal_user.username }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">النوع</span>
                <span class="badge-info text-xs">{{ userTypeLabel(parent.portal_user.user_type) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">الحالة</span>
                <span :class="parent.portal_user.is_active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'">
                  {{ parent.portal_user.is_active ? 'مفعل' : 'معطل' }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">آخر دخول</span>
                <span class="text-dark text-xs">{{ parent.portal_user.last_login || '—' }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">عدد مرات الدخول</span>
                <span class="text-dark">{{ parent.portal_user.login_count }}</span>
              </div>
            </div>
            <div class="flex gap-2 mt-4">
              <button @click="togglePortalUser(parent.portal_user.id)"
                      :class="parent.portal_user.is_active ? 'bg-red-50 text-red-700 hover:bg-red-100' : 'btn-primary'"
                      class="text-sm px-3 py-1.5 rounded-lg transition-colors">
                {{ parent.portal_user.is_active ? 'تعطيل الحساب' : 'تفعيل الحساب' }}
              </button>
              <button @click="showResetPw = parent.portal_user.id" class="btn-outline text-sm">تغيير كلمة المرور</button>
            </div>
          </template>
          <template v-else>
            <p class="text-gray-400 text-sm mb-3">لا يوجد حساب على البوابة</p>
            <button @click="showCreatePu = true" class="btn-primary text-sm">إنشاء حساب</button>
          </template>
        </div>
      </div>
    </template>

    <!-- Grant Content to All Children Modal -->
    <div v-if="showGrantAll" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showGrantAll = false">
      <div class="bg-white rounded-2xl w-full max-w-lg p-5">
        <h3 class="font-bold text-dark mb-4">منح محتوى لجميع الأبناء</h3>
        <p class="text-sm text-gray-500 mb-3">سيتم منح المحتوى المختار لـ {{ parent.children?.length || 0 }} طالب</p>
        <div class="space-y-3">
          <div class="max-h-64 overflow-y-auto space-y-2 border border-gray-100 rounded-lg p-3">
            <label v-for="ci in contentItems" :key="ci.id"
                   class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" :value="ci.id" v-model="grantAllForm.content_item_ids"
                     class="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary" />
              <div>
                <span class="text-sm text-dark">{{ ci.name }}</span>
                <span class="text-xs text-gray-400 mr-2">{{ contentTypeLabel(ci.content_type) }}</span>
              </div>
            </label>
            <p v-if="!contentItems.length" class="text-gray-400 text-sm text-center py-2">لا يوجد محتوى متاح</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ الانتهاء (اختياري)</label>
            <input v-model="grantAllForm.expiry_date" type="date" class="input-field text-sm w-full" />
          </div>
          <p v-if="grantAllError" class="text-red-600 text-sm">{{ grantAllError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showGrantAll = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="grantContentToAll" :disabled="grantAllSaving" class="btn-primary text-sm">
            منح ({{ grantAllForm.content_item_ids.length }})
          </button>
        </div>
      </div>
    </div>

    <!-- Create Portal User Modal -->
    <div v-if="showCreatePu" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showCreatePu = false">
      <div class="bg-white rounded-2xl w-full max-w-md p-5">
        <h3 class="font-bold text-dark mb-4">إنشاء حساب بوابة</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">اسم المستخدم</label>
            <input v-model="puForm.username" type="text" class="input-field text-sm w-full" :placeholder="parent.phone || 'رقم الهاتف'" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
            <input v-model="puForm.password" type="text" class="input-field text-sm w-full" placeholder="6 أحرف على الأقل" />
          </div>
          <p v-if="puError" class="text-red-600 text-sm">{{ puError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showCreatePu = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="createPortalUser" :disabled="puSaving" class="btn-primary text-sm">إنشاء</button>
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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { adminApi } from '@/services/adminApi'

const route = useRoute()
const parent = ref({})
const loading = ref(true)
const actionMsg = ref('')
const activeTab = ref('info')

const tabs = [
  { key: 'info', label: 'البيانات' },
  { key: 'subscriptions', label: 'اشتراكات الأبناء' },
  { key: 'content', label: 'محتوى الأبناء' },
  { key: 'account', label: 'الحساب' },
]

// Children data (subscriptions + content)
const childrenData = ref([])
const childrenDataLoading = ref(false)
const childrenDataLoaded = ref(false)

// Content items for grant modal
const contentItems = ref([])
const contentItemsLoaded = ref(false)

// Grant content to all children
const showGrantAll = ref(false)
const grantAllForm = ref({ content_item_ids: [], expiry_date: '' })
const grantAllError = ref('')
const grantAllSaving = ref(false)

// Portal user
const showCreatePu = ref(false)
const showResetPw = ref(null)
const newPassword = ref('')
const puForm = ref({ username: '', password: '' })
const puError = ref('')
const puSaving = ref(false)

// Labels
const relationLabels = { father: 'أب', mother: 'أم', guardian: 'ولي أمر', grandfather: 'جد', grandmother: 'جدة', uncle: 'عم / خال', aunt: 'عمة / خالة', other: 'أخرى' }
const socialLabels = { married: 'متزوج', divorced: 'مطلق', widowed: 'أرمل', separated: 'منفصل' }
const educationLabels = { primary: 'ابتدائي', preparatory: 'إعدادي', secondary: 'ثانوي', university: 'جامعي', postgraduate: 'دراسات عليا', other: 'أخرى' }
const childStateLabels = { enrolled: 'مسجل', draft: 'مسودة', pending: 'معلق', suspended: 'موقوف', archived: 'مؤرشف' }
function relationLabel(v) { return relationLabels[v] || v || '—' }
function socialLabel(v) { return socialLabels[v] || v || '—' }
function educationLabel(v) { return educationLabels[v] || v || '—' }
function childStateLabel(v) { return childStateLabels[v] || v || '—' }
function userTypeLabel(v) { return { parent: 'ولي أمر', admin: 'مدير', teacher: 'معلم', student: 'طالب' }[v] || v }
function subStatusLabel(v) { return { draft: 'مسودة', active: 'نشط', expired: 'منتهي', cancelled: 'ملغى' }[v] || v }
function subStatusClass(v) { return { draft: 'badge-info', active: 'badge-success', expired: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full', cancelled: 'bg-gray-100 text-gray-500 text-xs px-2 py-0.5 rounded-full' }[v] || 'badge-info' }
function contentTypeLabel(v) { return { book: 'كتاب', game: 'لعبة', course: 'دورة', video: 'فيديو', kids_area: 'منطقة أطفال' }[v] || v || '—' }

// Lazy tab loading
watch(activeTab, async (tab) => {
  if ((tab === 'subscriptions' || tab === 'content') && !childrenDataLoaded.value) {
    await loadChildrenData()
  }
  if (tab === 'content' && !contentItemsLoaded.value) {
    loadContentItems()
  }
})

async function loadChildrenData() {
  childrenDataLoading.value = true
  try {
    const { data } = await adminApi.getParentChildrenData(route.params.id)
    childrenData.value = data.children
    childrenDataLoaded.value = true
  } catch (e) { console.error('Failed:', e) }
  finally { childrenDataLoading.value = false }
}

async function loadContentItems() {
  try {
    const { data } = await adminApi.getSubscriptionOptions()
    contentItems.value = data.content_items || []
    contentItemsLoaded.value = true
  } catch (e) { console.error('Failed:', e) }
}

async function fetchParent() {
  loading.value = true
  try {
    const { data } = await adminApi.getParent(route.params.id)
    parent.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.parentAction(route.params.id, action)
    actionMsg.value = data.message
    parent.value.active = data.active
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

// Grant content to all children
async function grantContentToAll() {
  if (!grantAllForm.value.content_item_ids.length) {
    grantAllError.value = 'اختر محتوى واحد على الأقل'
    return
  }
  grantAllSaving.value = true
  grantAllError.value = ''
  try {
    const { data } = await adminApi.grantContentToParentChildren(route.params.id, grantAllForm.value)
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 3000)
    showGrantAll.value = false
    grantAllForm.value = { content_item_ids: [], expiry_date: '' }
    childrenDataLoaded.value = false
    await loadChildrenData()
  } catch (e) {
    grantAllError.value = e.response?.data?.error || 'حدث خطأ'
  } finally { grantAllSaving.value = false }
}

// Portal user management
async function togglePortalUser(puId) {
  try {
    const { data } = await adminApi.togglePortalUser(puId)
    parent.value.portal_user.is_active = data.is_active
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

async function createPortalUser() {
  if (!puForm.value.username || !puForm.value.password) {
    puError.value = 'جميع الحقول مطلوبة'
    return
  }
  puSaving.value = true
  puError.value = ''
  try {
    await adminApi.createPortalUser({
      partner_id: parent.value.id,
      username: puForm.value.username,
      password: puForm.value.password,
      user_type: 'parent',
    })
    showCreatePu.value = false
    fetchParent()
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

onMounted(fetchParent)
</script>
