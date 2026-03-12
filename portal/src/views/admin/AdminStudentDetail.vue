<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/students" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">{{ student.name }}</h1>
        <p class="text-sm text-gray-500">{{ student.code }}</p>
      </div>
      <span :class="stateClass(student.state)" class="text-sm">{{ stateLabel(student.state) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="student.state === 'draft'" @click="doAction('pending')"
                class="btn-outline text-sm">تقديم للتسجيل</button>
        <button v-if="student.state === 'pending' || student.state === 'draft'" @click="doAction('enroll')"
                class="btn-primary text-sm">تسجيل الطالب</button>
        <button v-if="student.state === 'enrolled'" @click="doAction('suspend')"
                class="bg-amber-50 text-amber-700 px-4 py-2 rounded-lg text-sm hover:bg-amber-100 transition-colors">إيقاف</button>
        <button v-if="student.state !== 'archived'" @click="doAction('archive')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">أرشفة</button>
        <button v-if="student.state === 'archived' || student.state === 'suspended'" @click="doAction('reactivate')"
                class="btn-primary text-sm">إعادة تفعيل</button>
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
              <div><span class="text-gray-500 block mb-0.5">الاسم</span><span class="text-dark font-medium">{{ student.name }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الاسم بالإنجليزي</span><span class="text-dark font-medium">{{ student.arabic_name || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الكود</span><span class="text-dark font-medium font-mono">{{ student.code || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الجنس</span><span class="text-dark font-medium">{{ genderLabel(student.gender) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">تاريخ الميلاد</span><span class="text-dark font-medium">{{ student.birthdate || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">العمر</span><span class="text-dark font-medium">{{ student.age || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الهاتف</span><span class="text-dark font-medium font-mono direction-ltr">{{ student.phone || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الديانة</span><span class="text-dark font-medium">{{ religionLabel(student.religion) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">فصيلة الدم</span><span class="text-dark font-medium">{{ student.blood_type || '—' }}</span></div>
            </div>
          </div>

          <!-- Stats -->
          <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
            <h3 class="font-bold text-dark mb-2">إحصائيات</h3>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">الحضور</span>
              <span class="font-bold text-dark">{{ student.attendance_rate }}%</span>
            </div>
            <div class="w-full h-2 bg-gray-100 rounded-full">
              <div class="h-full rounded-full" :class="student.attendance_rate > 80 ? 'bg-green-500' : student.attendance_rate > 60 ? 'bg-yellow-500' : 'bg-red-500'"
                   :style="{ width: student.attendance_rate + '%' }"></div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">الرصيد المستحق</span>
              <span :class="student.balance_due > 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">{{ student.balance_due?.toLocaleString() }} ج.م</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500 text-sm">الاشتراكات</span>
              <span class="font-bold text-dark">{{ student.subscription_count }}</span>
            </div>
          </div>
        </div>

        <!-- Academic + Parents -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
          <div class="bg-white rounded-xl border border-gray-100 p-5">
            <h3 class="font-bold text-dark mb-4">البيانات الأكاديمية</h3>
            <div class="grid grid-cols-2 gap-y-4 gap-x-6 text-sm">
              <div><span class="text-gray-500 block mb-0.5">القسم</span><span class="text-dark font-medium">{{ student.department || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الفصل</span><span class="text-dark font-medium">{{ student.class_name || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الفترة</span><span class="text-dark font-medium">{{ periodLabel(student.period) }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">الفرع</span><span class="text-dark font-medium">{{ student.branch || '—' }}</span></div>
              <div><span class="text-gray-500 block mb-0.5">تاريخ التسجيل</span><span class="text-dark font-medium">{{ student.enrollment_date || '—' }}</span></div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-5">
            <h3 class="font-bold text-dark mb-4">أولياء الأمور</h3>
            <div class="space-y-3">
              <div v-if="student.father" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                   @click="$router.push('/admin/parents/' + student.father.id)">
                <div class="w-9 h-9 bg-blue-50 rounded-lg flex items-center justify-center">
                  <span class="text-xs font-bold text-blue-600">أ</span>
                </div>
                <div>
                  <p class="font-medium text-dark text-sm">{{ student.father.name }}</p>
                  <p class="text-xs text-gray-400">الأب</p>
                </div>
              </div>
              <div v-if="student.mother" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                   @click="$router.push('/admin/parents/' + student.mother.id)">
                <div class="w-9 h-9 bg-pink-50 rounded-lg flex items-center justify-center">
                  <span class="text-xs font-bold text-pink-600">أ</span>
                </div>
                <div>
                  <p class="font-medium text-dark text-sm">{{ student.mother.name }}</p>
                  <p class="text-xs text-gray-400">الأم</p>
                </div>
              </div>
              <p v-if="!student.father && !student.mother" class="text-gray-400 text-sm">لا يوجد أولياء أمور مسجلين</p>
            </div>
            <div v-if="student.siblings?.length" class="mt-4 pt-4 border-t border-gray-100">
              <p class="text-xs text-gray-500 mb-2">الأشقاء</p>
              <div class="flex flex-wrap gap-2">
                <router-link v-for="sib in student.siblings" :key="sib.id" :to="'/admin/students/' + sib.id"
                             class="badge-info text-xs">{{ sib.name }}</router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Medical -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">معلومات طبية</h3>
          <div class="space-y-3 text-sm">
            <div><span class="text-gray-500 block mb-0.5">الحساسية</span><span class="text-dark">{{ student.allergies || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">ملاحظات طبية</span><span class="text-dark">{{ student.medical_notes || '—' }}</span></div>
          </div>
        </div>
      </div>

      <!-- Tab: الاشتراكات -->
      <div v-show="activeTab === 'subscriptions'">
        <div v-if="subsLoading" class="flex items-center justify-center py-12">
          <div class="w-7 h-7 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
        <template v-else>
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-dark">الاشتراكات ({{ subscriptions.length }})</h3>
            <button @click="showCreateSub = true" class="btn-primary text-sm">إضافة اشتراك</button>
          </div>

          <div v-if="!subscriptions.length" class="bg-white rounded-xl border border-gray-100 p-8 text-center">
            <p class="text-gray-400">لا توجد اشتراكات</p>
          </div>

          <div v-for="sub in subscriptions" :key="sub.id" class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h4 class="font-bold text-dark">{{ sub.type }}</h4>
                <p class="text-xs text-gray-400">{{ sub.plan }} · {{ sub.start_date }}</p>
              </div>
              <span :class="subStatusClass(sub.status)" class="text-xs">{{ subStatusLabel(sub.status) }}</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm mb-4">
              <div><span class="text-gray-500 block text-xs">الإجمالي</span><span class="font-bold text-dark">{{ sub.total_amount?.toLocaleString() }}</span></div>
              <div><span class="text-gray-500 block text-xs">الخصم</span><span class="font-bold text-dark">{{ sub.discount?.toLocaleString() }}</span></div>
              <div><span class="text-gray-500 block text-xs">المدفوع</span><span class="font-bold text-green-600">{{ sub.paid_amount?.toLocaleString() }}</span></div>
              <div><span class="text-gray-500 block text-xs">المتبقي</span><span class="font-bold text-red-600">{{ sub.remaining_amount?.toLocaleString() }}</span></div>
            </div>
            <!-- Installments -->
            <div v-if="sub.installments?.length" class="border-t border-gray-100 pt-3">
              <p class="text-xs text-gray-500 mb-2">الأقساط</p>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="text-gray-500 text-xs">
                      <th class="text-right pb-2 font-medium">#</th>
                      <th class="text-right pb-2 font-medium">التاريخ</th>
                      <th class="text-right pb-2 font-medium">المبلغ</th>
                      <th class="text-right pb-2 font-medium">المدفوع</th>
                      <th class="text-right pb-2 font-medium">الحالة</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="inst in sub.installments" :key="inst.id" class="border-t border-gray-50">
                      <td class="py-2 text-dark">{{ inst.sequence }}</td>
                      <td class="py-2 text-dark">{{ inst.due_date }}</td>
                      <td class="py-2 text-dark">{{ inst.amount?.toLocaleString() }}</td>
                      <td class="py-2" :class="inst.paid_amount > 0 ? 'text-green-600' : 'text-gray-400'">{{ inst.paid_amount?.toLocaleString() }}</td>
                      <td class="py-2">
                        <span :class="inst.is_paid ? 'badge-success' : 'badge-warning'" class="text-xs">
                          {{ inst.is_paid ? 'مدفوع' : 'معلق' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Tab: المحتوى -->
      <div v-show="activeTab === 'content'">
        <div v-if="contentLoading" class="flex items-center justify-center py-12">
          <div class="w-7 h-7 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
        <template v-else>
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold text-dark">المحتوى ({{ contentAccess.length }})</h3>
            <button @click="showGrantContent = true" class="btn-primary text-sm">منح محتوى</button>
          </div>

          <div v-if="!contentAccess.length" class="bg-white rounded-xl border border-gray-100 p-8 text-center">
            <p class="text-gray-400">لا يوجد محتوى ممنوح</p>
          </div>

          <div v-else class="bg-white rounded-xl border border-gray-100 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-xs">
                  <th class="text-right p-3 font-medium">المحتوى</th>
                  <th class="text-right p-3 font-medium">النوع</th>
                  <th class="text-right p-3 font-medium">تاريخ المنح</th>
                  <th class="text-right p-3 font-medium">تاريخ الانتهاء</th>
                  <th class="text-right p-3 font-medium">الحالة</th>
                  <th class="text-right p-3 font-medium"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in contentAccess" :key="a.id" class="border-t border-gray-50">
                  <td class="p-3 text-dark font-medium">{{ a.content_name }}</td>
                  <td class="p-3 text-gray-500">{{ contentTypeLabel(a.content_type) }}</td>
                  <td class="p-3 text-dark">{{ a.granted_date }}</td>
                  <td class="p-3 text-dark">{{ a.expiry_date || '—' }}</td>
                  <td class="p-3">
                    <span :class="a.is_active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'" class="text-xs">
                      {{ a.is_active ? 'نشط' : 'ملغى' }}
                    </span>
                  </td>
                  <td class="p-3">
                    <button v-if="a.is_active" @click="revokeAccess(a.id)"
                            class="text-red-600 hover:text-red-800 text-xs">إلغاء</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>

      <!-- Tab: الحساب -->
      <div v-show="activeTab === 'account'">
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <h3 class="font-bold text-dark mb-4">حساب البوابة</h3>
          <template v-if="student.portal_user">
            <div class="space-y-3 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-gray-500">اسم المستخدم</span>
                <span class="font-mono text-dark">{{ student.portal_user.username }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">النوع</span>
                <span class="badge-info text-xs">{{ userTypeLabel(student.portal_user.user_type) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">الحالة</span>
                <span :class="student.portal_user.is_active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'">
                  {{ student.portal_user.is_active ? 'مفعل' : 'معطل' }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">آخر دخول</span>
                <span class="text-dark text-xs">{{ student.portal_user.last_login || '—' }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-500">عدد مرات الدخول</span>
                <span class="text-dark">{{ student.portal_user.login_count }}</span>
              </div>
            </div>
            <div class="flex gap-2 mt-4">
              <button @click="togglePortalUser(student.portal_user.id)"
                      :class="student.portal_user.is_active ? 'bg-red-50 text-red-700 hover:bg-red-100' : 'btn-primary'"
                      class="text-sm px-3 py-1.5 rounded-lg transition-colors">
                {{ student.portal_user.is_active ? 'تعطيل الحساب' : 'تفعيل الحساب' }}
              </button>
              <button @click="showResetPw = student.portal_user.id" class="btn-outline text-sm">تغيير كلمة المرور</button>
            </div>
          </template>
          <template v-else>
            <p class="text-gray-400 text-sm mb-3">لا يوجد حساب على البوابة</p>
            <button @click="showCreatePu = true" class="btn-primary text-sm">إنشاء حساب</button>
          </template>
        </div>
      </div>
    </template>

    <!-- Create Subscription Modal -->
    <div v-if="showCreateSub" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showCreateSub = false">
      <div class="bg-white rounded-2xl w-full max-w-lg p-5">
        <h3 class="font-bold text-dark mb-4">إضافة اشتراك</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">نوع الاشتراك</label>
            <select v-model="subForm.subscription_type_id" @change="onSubTypeChange" class="input-field text-sm w-full">
              <option value="">اختر نوع الاشتراك</option>
              <option v-for="st in subOptions.subscription_types" :key="st.id" :value="st.id">
                {{ st.name }} — {{ st.amount?.toLocaleString() }} ج.م
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">خطة الدفع</label>
            <select v-model="subForm.payment_plan_id" class="input-field text-sm w-full">
              <option value="">اختر خطة الدفع</option>
              <option v-for="pp in subOptions.payment_plans" :key="pp.id" :value="pp.id">
                {{ pp.name }} ({{ pp.installment_count }} قسط)
              </option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ البداية</label>
              <input v-model="subForm.start_date" type="date" class="input-field text-sm w-full" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">المبلغ</label>
              <input v-model.number="subForm.total_amount" type="number" class="input-field text-sm w-full" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الخصم</label>
              <input v-model.number="subForm.discount" type="number" class="input-field text-sm w-full" placeholder="0" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">الصافي</label>
              <p class="input-field text-sm w-full bg-gray-50 flex items-center">{{ ((subForm.total_amount || 0) - (subForm.discount || 0)).toLocaleString() }} ج.م</p>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">ملاحظات</label>
            <textarea v-model="subForm.notes" class="input-field text-sm w-full" rows="2"></textarea>
          </div>
          <p v-if="subError" class="text-red-600 text-sm">{{ subError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showCreateSub = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="createSubscription" :disabled="subSaving" class="btn-primary text-sm">إنشاء</button>
        </div>
      </div>
    </div>

    <!-- Grant Content Modal -->
    <div v-if="showGrantContent" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="showGrantContent = false">
      <div class="bg-white rounded-2xl w-full max-w-lg p-5">
        <h3 class="font-bold text-dark mb-4">منح محتوى</h3>
        <div class="space-y-3">
          <div class="max-h-64 overflow-y-auto space-y-2 border border-gray-100 rounded-lg p-3">
            <label v-for="ci in subOptions.content_items" :key="ci.id"
                   class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" :value="ci.id" v-model="grantForm.content_item_ids"
                     class="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary" />
              <div>
                <span class="text-sm text-dark">{{ ci.name }}</span>
                <span class="text-xs text-gray-400 mr-2">{{ contentTypeLabel(ci.content_type) }}</span>
              </div>
            </label>
            <p v-if="!subOptions.content_items?.length" class="text-gray-400 text-sm text-center py-2">لا يوجد محتوى متاح</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">تاريخ الانتهاء (اختياري)</label>
            <input v-model="grantForm.expiry_date" type="date" class="input-field text-sm w-full" />
          </div>
          <p v-if="grantError" class="text-red-600 text-sm">{{ grantError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showGrantContent = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="grantContent" :disabled="grantSaving" class="btn-primary text-sm">
            منح ({{ grantForm.content_item_ids.length }})
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
            <input v-model="puForm.username" type="text" class="input-field text-sm w-full" :placeholder="student.phone || 'رقم الهاتف'" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
            <input v-model="puForm.password" type="text" class="input-field text-sm w-full" placeholder="6 أحرف على الأقل" />
          </div>
          <p v-if="puError" class="text-red-600 text-sm">{{ puError }}</p>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button @click="showCreatePu = false" class="btn-outline text-sm">إلغاء</button>
          <button @click="createPortalUser('student')" :disabled="puSaving" class="btn-primary text-sm">إنشاء</button>
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
const student = ref({})
const loading = ref(true)
const actionMsg = ref('')
const activeTab = ref('info')

// Tabs
const tabs = [
  { key: 'info', label: 'البيانات' },
  { key: 'subscriptions', label: 'الاشتراكات' },
  { key: 'content', label: 'المحتوى' },
  { key: 'account', label: 'الحساب' },
]

// Subscriptions tab
const subscriptions = ref([])
const subsLoading = ref(false)
const subsLoaded = ref(false)

// Content tab
const contentAccess = ref([])
const contentLoading = ref(false)
const contentLoaded = ref(false)

// Subscription options (loaded on demand)
const subOptions = ref({ subscription_types: [], payment_plans: [], content_items: [] })
const optionsLoaded = ref(false)

// Create subscription modal
const showCreateSub = ref(false)
const subForm = ref({ subscription_type_id: '', payment_plan_id: '', start_date: '', total_amount: 0, discount: 0, notes: '' })
const subError = ref('')
const subSaving = ref(false)

// Grant content modal
const showGrantContent = ref(false)
const grantForm = ref({ content_item_ids: [], expiry_date: '' })
const grantError = ref('')
const grantSaving = ref(false)

// Portal user
const showCreatePu = ref(false)
const showResetPw = ref(null)
const newPassword = ref('')
const puForm = ref({ username: '', password: '' })
const puError = ref('')
const puSaving = ref(false)

// Labels
const stateLabels = { draft: 'مسودة', pending: 'معلق', enrolled: 'مسجل', suspended: 'موقوف', archived: 'مؤرشف' }
const stateClasses = { draft: 'badge-info', pending: 'badge-warning', enrolled: 'badge-success', suspended: 'bg-amber-50 text-amber-700 text-xs px-2 py-0.5 rounded-full', archived: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' }
function stateLabel(v) { return stateLabels[v] || v || '—' }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function genderLabel(v) { return v === 'male' ? 'ذكر' : v === 'female' ? 'أنثى' : '—' }
function periodLabel(v) { return { morning: 'صباحي', afternoon: 'مسائي', full_day: 'يوم كامل' }[v] || '—' }
function religionLabel(v) { return { islam: 'إسلام', christianity: 'مسيحي', other: 'أخرى' }[v] || '—' }
function userTypeLabel(v) { return { parent: 'ولي أمر', admin: 'مدير', teacher: 'معلم', student: 'طالب' }[v] || v }
function subStatusLabel(v) { return { draft: 'مسودة', active: 'نشط', expired: 'منتهي', cancelled: 'ملغى' }[v] || v }
function subStatusClass(v) { return { draft: 'badge-info', active: 'badge-success', expired: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full', cancelled: 'bg-gray-100 text-gray-500 text-xs px-2 py-0.5 rounded-full' }[v] || 'badge-info' }
function contentTypeLabel(v) { return { book: 'كتاب', game: 'لعبة', course: 'دورة', video: 'فيديو', kids_area: 'منطقة أطفال' }[v] || v || '—' }

// Lazy tab loading
watch(activeTab, async (tab) => {
  if (tab === 'subscriptions' && !subsLoaded.value) {
    await loadSubscriptions()
  }
  if (tab === 'content' && !contentLoaded.value) {
    await loadContentAccess()
  }
  if ((tab === 'subscriptions' || tab === 'content') && !optionsLoaded.value) {
    loadOptions()
  }
})

async function loadOptions() {
  try {
    const { data } = await adminApi.getSubscriptionOptions()
    subOptions.value = data
    optionsLoaded.value = true
  } catch (e) { console.error('Failed to load options:', e) }
}

async function loadSubscriptions() {
  subsLoading.value = true
  try {
    const { data } = await adminApi.getStudentSubscriptions(route.params.id)
    subscriptions.value = data.subscriptions
    subsLoaded.value = true
  } catch (e) { console.error('Failed:', e) }
  finally { subsLoading.value = false }
}

async function loadContentAccess() {
  contentLoading.value = true
  try {
    const { data } = await adminApi.getStudentContentAccess(route.params.id)
    contentAccess.value = data.content_access
    contentLoaded.value = true
  } catch (e) { console.error('Failed:', e) }
  finally { contentLoading.value = false }
}

async function fetchStudent() {
  loading.value = true
  try {
    const { data } = await adminApi.getStudent(route.params.id)
    student.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.studentAction(route.params.id, action)
    actionMsg.value = data.message
    student.value.state = data.state
    student.value.active = data.active
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

// Subscription creation
function onSubTypeChange() {
  const st = subOptions.value.subscription_types.find(s => s.id === subForm.value.subscription_type_id)
  if (st) {
    subForm.value.total_amount = st.amount
    if (st.payment_plan_id) subForm.value.payment_plan_id = st.payment_plan_id
  }
}

async function createSubscription() {
  if (!subForm.value.subscription_type_id || !subForm.value.payment_plan_id) {
    subError.value = 'نوع الاشتراك وخطة الدفع مطلوبان'
    return
  }
  subSaving.value = true
  subError.value = ''
  try {
    const { data } = await adminApi.createStudentSubscription(route.params.id, subForm.value)
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
    showCreateSub.value = false
    subForm.value = { subscription_type_id: '', payment_plan_id: '', start_date: '', total_amount: 0, discount: 0, notes: '' }
    subsLoaded.value = false
    await loadSubscriptions()
  } catch (e) {
    subError.value = e.response?.data?.error || 'حدث خطأ'
  } finally { subSaving.value = false }
}

// Content grant
async function grantContent() {
  if (!grantForm.value.content_item_ids.length) {
    grantError.value = 'اختر محتوى واحد على الأقل'
    return
  }
  grantSaving.value = true
  grantError.value = ''
  try {
    const { data } = await adminApi.grantContentToStudent(route.params.id, grantForm.value)
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
    showGrantContent.value = false
    grantForm.value = { content_item_ids: [], expiry_date: '' }
    contentLoaded.value = false
    await loadContentAccess()
  } catch (e) {
    grantError.value = e.response?.data?.error || 'حدث خطأ'
  } finally { grantSaving.value = false }
}

async function revokeAccess(accessId) {
  try {
    const { data } = await adminApi.revokeContentAccess(accessId)
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
    const item = contentAccess.value.find(a => a.id === accessId)
    if (item) item.is_active = false
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

// Portal user management
async function togglePortalUser(puId) {
  try {
    const { data } = await adminApi.togglePortalUser(puId)
    student.value.portal_user.is_active = data.is_active
    actionMsg.value = data.message
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

async function createPortalUser(userType) {
  if (!puForm.value.username || !puForm.value.password) {
    puError.value = 'جميع الحقول مطلوبة'
    return
  }
  puSaving.value = true
  puError.value = ''
  try {
    await adminApi.createPortalUser({
      partner_id: student.value.id,
      username: puForm.value.username,
      password: puForm.value.password,
      user_type: userType,
    })
    showCreatePu.value = false
    fetchStudent()
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

onMounted(fetchStudent)
</script>
