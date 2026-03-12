<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/messages" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">{{ msg.subject }}</h1>
        <p class="text-sm text-gray-500">{{ msg.name }}</p>
      </div>
      <span :class="stateClass(msg.state)" class="text-sm">{{ stateLabel(msg.state) }}</span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="msg.state === 'draft' || msg.state === 'scheduled'" @click="doAction('send')" class="btn-primary text-sm">إرسال الآن</button>
        <button v-if="msg.state !== 'cancelled' && msg.state !== 'sent'" @click="doAction('cancel')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">إلغاء</button>
        <button v-if="msg.state === 'cancelled'" @click="doAction('draft')" class="btn-outline text-sm">إرجاع لمسودة</button>
      </div>

      <!-- Info + Stats -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
        <!-- Message Info -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
          <h3 class="font-bold text-dark mb-4">بيانات الرسالة</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">الرقم</span><span class="text-dark font-medium font-mono">{{ msg.name || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">الموضوع</span><span class="text-dark font-medium">{{ msg.subject }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">نوع المستلم</span><span class="badge-info text-xs">{{ recipientLabel(msg.recipient_type) }}</span></div>
            <div v-if="msg.department"><span class="text-gray-500 block mb-0.5">القسم</span><span class="text-dark font-medium">{{ msg.department }}</span></div>
            <div v-if="msg.class_name"><span class="text-gray-500 block mb-0.5">الفصل</span><span class="text-dark font-medium">{{ msg.class_name }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">المرسل</span><span class="text-dark font-medium">{{ msg.created_by || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الجدولة</span><span class="text-dark font-medium">{{ formatDate(msg.scheduled_date) }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">تاريخ الإرسال</span><span class="text-dark font-medium">{{ formatDate(msg.sent_date) }}</span></div>
          </div>
        </div>

        <!-- Stats -->
        <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
          <h3 class="font-bold text-dark mb-2">إحصائيات</h3>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">عدد المستلمين</span>
            <span class="font-bold text-dark text-lg">{{ msg.recipient_count }}</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">تم الإرسال</span>
            <span class="font-bold text-green-600">{{ msg.sent_count }}</span>
          </div>
          <div v-if="msg.failed_count" class="flex items-center justify-between text-sm">
            <span class="text-gray-500">فشل الإرسال</span>
            <span class="font-bold text-red-600">{{ msg.failed_count }}</span>
          </div>
          <div v-if="msg.sent_count && msg.recipient_count" class="mt-2">
            <div class="w-full h-2 bg-gray-100 rounded-full">
              <div class="h-full bg-green-500 rounded-full" :style="{ width: Math.round(msg.sent_count / msg.recipient_count * 100) + '%' }"></div>
            </div>
            <p class="text-xs text-gray-400 mt-1 text-center">{{ Math.round(msg.sent_count / msg.recipient_count * 100) }}%</p>
          </div>
        </div>
      </div>

      <!-- Message Body -->
      <div class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-3">محتوى الرسالة</h3>
        <div class="text-sm text-gray-700 prose prose-sm max-w-none" v-html="msg.body"></div>
      </div>

      <!-- Recipients (individual) -->
      <div v-if="msg.recipients?.length" class="bg-white rounded-xl border border-gray-100 p-5 mb-4">
        <h3 class="font-bold text-dark mb-3">المستلمون</h3>
        <div class="flex flex-wrap gap-2">
          <router-link v-for="r in msg.recipients" :key="r.id" :to="'/admin/students/' + r.id"
                       class="badge-info text-xs hover:bg-blue-100 transition-colors">{{ r.name }}</router-link>
        </div>
      </div>

      <!-- Logs -->
      <div v-if="msg.logs?.length" class="bg-white rounded-xl border border-gray-100 overflow-hidden">
        <div class="p-4 border-b border-gray-100">
          <h3 class="font-bold text-dark">سجل الإرسال ({{ msg.logs.length }})</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50/80">
              <tr>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">المستلم</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
                <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">تاريخ الإرسال</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lg in msg.logs" :key="lg.id" class="border-t border-gray-50">
                <td class="py-2 px-4 text-dark">{{ lg.recipient || '—' }}</td>
                <td class="py-2 px-4">
                  <span :class="lg.status === 'sent' ? 'badge-success' : lg.status === 'failed' ? 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' : 'badge-info'">
                    {{ logStatusLabel(lg.status) }}
                  </span>
                </td>
                <td class="py-2 px-4 text-gray-500 text-xs">{{ formatDate(lg.sent_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

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
const msg = ref({})
const loading = ref(true)
const actionMsg = ref('')

const stateLabels = { draft: 'مسودة', scheduled: 'مجدولة', sent: 'مرسلة', cancelled: 'ملغية' }
const stateClasses = { draft: 'badge-info', scheduled: 'badge-warning', sent: 'badge-success', cancelled: 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full' }
const recipientLabels = { all: 'الكل', department: 'قسم', class: 'فصل', individual: 'فردي' }
const logStatusLabels = { sent: 'تم الإرسال', failed: 'فشل', pending: 'في الانتظار' }

function stateLabel(v) { return stateLabels[v] || v || '—' }
function stateClass(v) { return stateClasses[v] || 'badge-info' }
function recipientLabel(v) { return recipientLabels[v] || v || '—' }
function logStatusLabel(v) { return logStatusLabels[v] || v || '—' }

function formatDate(dt) {
  if (!dt) return '—'
  return dt.replace('T', ' ').slice(0, 16)
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getMessage(route.params.id)
    msg.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.messageAction(route.params.id, action)
    actionMsg.value = data.message
    msg.value.state = data.state
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

onMounted(fetchData)
</script>
