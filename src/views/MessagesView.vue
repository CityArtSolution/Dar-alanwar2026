<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">الرسائل والإعلانات</h1>

    <!-- Tab Navigation -->
    <div class="flex gap-1 mb-6 bg-white rounded-xl p-1 border border-gray-200">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap relative"
        :class="activeTab === tab.key ? 'bg-primary-500 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
      >
        {{ tab.label }}
        <span
          v-if="tab.key === 'messages' && unreadCount > 0"
          class="absolute -top-1 -left-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
        >
          {{ unreadCount }}
        </span>
      </button>
    </div>

    <!-- Announcements Tab -->
    <div v-if="activeTab === 'announcements'">
      <div v-if="announcementsLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
      </div>

      <div v-else-if="announcements.length === 0" class="card text-center py-16">
        <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/>
        </svg>
        <p class="text-gray-500 text-lg">لا توجد إعلانات</p>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="announcement in announcements"
          :key="announcement.id"
          class="card hover:shadow-md transition-shadow cursor-pointer"
          @click="toggleAnnouncement(announcement)"
        >
          <div class="flex items-start justify-between mb-2">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                   :class="priorityBgClass(announcement.priority)">
                <svg class="w-5 h-5" :class="priorityIconClass(announcement.priority)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-bold">{{ announcement.title }}</h3>
                <p class="text-xs text-gray-400 mt-1">{{ formatDate(announcement.created_at) }}</p>
              </div>
            </div>
            <span :class="priorityBadgeClass(announcement.priority)">
              {{ priorityLabel(announcement.priority) }}
            </span>
          </div>

          <p v-if="expandedAnnouncement !== announcement.id" class="text-sm text-gray-600 line-clamp-2">
            {{ announcement.content }}
          </p>
          <div v-else class="text-sm text-gray-600 leading-relaxed whitespace-pre-line mt-2">
            {{ announcement.content }}
          </div>

          <div class="flex items-center gap-1 mt-3 text-xs text-primary-500">
            <span>{{ expandedAnnouncement === announcement.id ? 'عرض أقل' : 'عرض المزيد' }}</span>
            <svg class="w-3 h-3 transition-transform" :class="expandedAnnouncement === announcement.id ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages Tab -->
    <div v-if="activeTab === 'messages'">
      <div v-if="messagesLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
      </div>

      <template v-else>
        <!-- Compose Button -->
        <div class="flex justify-end mb-4">
          <button @click="showComposeForm = !showComposeForm" class="btn-primary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            رسالة جديدة
          </button>
        </div>

        <!-- Compose Form -->
        <div v-if="showComposeForm" class="card mb-6">
          <h2 class="text-lg font-bold mb-4">إرسال رسالة جديدة</h2>
          <form @submit.prevent="sendMessage">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">الموضوع</label>
              <input
                v-model="composeForm.subject"
                type="text"
                class="input-field"
                placeholder="أدخل موضوع الرسالة"
                required
              />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">نوع الرسالة</label>
              <select v-model="composeForm.type" class="input-field">
                <option value="message">رسالة عامة</option>
                <option value="support">تذكرة دعم</option>
              </select>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">المحتوى</label>
              <textarea
                v-model="composeForm.body"
                class="input-field min-h-[120px] resize-y"
                placeholder="اكتب رسالتك هنا..."
                rows="4"
                required
              ></textarea>
            </div>

            <!-- Send Error -->
            <div v-if="sendError" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <p class="text-sm text-red-700">{{ sendError }}</p>
            </div>

            <div class="flex gap-3 justify-end">
              <button type="button" @click="showComposeForm = false" class="btn-secondary">إلغاء</button>
              <button type="submit" class="btn-primary" :disabled="sending">
                <span v-if="sending">جارٍ الإرسال...</span>
                <span v-else>{{ composeForm.type === 'support' ? 'إرسال تذكرة الدعم' : 'إرسال' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Messages List -->
        <div v-if="messages.length === 0 && !showComposeForm" class="card text-center py-16">
          <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
          </svg>
          <p class="text-gray-500 text-lg">لا توجد رسائل</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="message in messages"
            :key="message.id"
            @click="viewMessage(message)"
            class="card hover:shadow-md transition-shadow cursor-pointer"
            :class="{ 'border-r-4 border-r-primary-500': !message.is_read }"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-start gap-3 flex-1 min-w-0">
                <!-- Read/Unread Indicator -->
                <div class="w-2.5 h-2.5 rounded-full mt-2 flex-shrink-0"
                     :class="message.is_read ? 'bg-gray-300' : 'bg-primary-500'"></div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <h3 class="font-bold truncate" :class="{ 'text-gray-600': message.is_read }">
                      {{ message.subject }}
                    </h3>
                    <span v-if="message.type === 'support'" class="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-purple-700 flex-shrink-0">
                      دعم
                    </span>
                  </div>
                  <p class="text-sm text-gray-500 truncate">{{ message.preview || message.body?.substring(0, 100) }}</p>
                  <div class="flex items-center gap-3 mt-2 text-xs text-gray-400">
                    <span v-if="message.sender_name">{{ message.sender_name }}</span>
                    <span>{{ formatDate(message.created_at) }}</span>
                  </div>
                </div>
              </div>
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Message Detail Modal -->
    <div v-if="selectedMessage" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50" @click="selectedMessage = null"></div>
      <div class="relative bg-white rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div class="p-6">
          <!-- Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h2 class="text-xl font-bold">{{ selectedMessage.subject }}</h2>
                <span v-if="selectedMessage.type === 'support'" class="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-purple-700">
                  تذكرة دعم
                </span>
              </div>
              <div class="flex items-center gap-3 text-sm text-gray-500">
                <span v-if="selectedMessage.sender_name">من: {{ selectedMessage.sender_name }}</span>
                <span>{{ formatDate(selectedMessage.created_at) }}</span>
              </div>
            </div>
            <button @click="selectedMessage = null" class="p-2 rounded-lg hover:bg-gray-100">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <div class="text-gray-700 leading-relaxed whitespace-pre-line">
              {{ selectedMessage.body }}
            </div>
          </div>

          <!-- Attachments -->
          <div v-if="selectedMessage.attachments && selectedMessage.attachments.length > 0" class="mb-6">
            <h3 class="text-sm font-medium text-gray-700 mb-2">المرفقات</h3>
            <div class="space-y-2">
              <a
                v-for="att in selectedMessage.attachments"
                :key="att.id || att.url"
                :href="att.url"
                target="_blank"
                class="flex items-center gap-2 p-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-sm"
              >
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/>
                </svg>
                <span class="text-primary-600">{{ att.name || 'مرفق' }}</span>
              </a>
            </div>
          </div>

          <button @click="selectedMessage = null" class="btn-secondary w-full">إغلاق</button>
        </div>
      </div>
    </div>

    <!-- Support Ticket Section -->
    <div v-if="activeTab === 'support'">
      <div class="card">
        <h2 class="text-lg font-bold mb-4">إرسال تذكرة دعم</h2>
        <p class="text-sm text-gray-500 mb-6">هل لديك استفسار أو مشكلة؟ أرسل تذكرة دعم وسنقوم بالرد عليك في أقرب وقت ممكن.</p>

        <form @submit.prevent="submitSupportTicket">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">الموضوع</label>
            <input
              v-model="supportForm.subject"
              type="text"
              class="input-field"
              placeholder="موضوع التذكرة"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">التفاصيل</label>
            <textarea
              v-model="supportForm.body"
              class="input-field min-h-[150px] resize-y"
              placeholder="اشرح مشكلتك أو استفسارك بالتفصيل..."
              rows="5"
              required
            ></textarea>
          </div>

          <div v-if="supportSuccess" class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-green-700">تم إرسال تذكرة الدعم بنجاح. سنقوم بالرد عليك قريباً.</p>
          </div>
          <div v-if="supportError" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-red-700">{{ supportError }}</p>
          </div>

          <button type="submit" class="btn-primary w-full" :disabled="supportSending">
            <span v-if="supportSending">جارٍ الإرسال...</span>
            <span v-else>إرسال تذكرة الدعم</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { messagesApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const activeTab = ref('announcements')
const unreadCount = ref(0)

const tabs = [
  { key: 'announcements', label: 'الإعلانات' },
  { key: 'messages', label: 'الرسائل' },
  { key: 'support', label: 'الدعم الفني' },
]

// Announcements
const announcements = ref([])
const announcementsLoading = ref(false)
const expandedAnnouncement = ref(null)

// Messages
const messages = ref([])
const messagesLoading = ref(false)
const selectedMessage = ref(null)
const showComposeForm = ref(false)

// Compose
const composeForm = ref({ subject: '', body: '', type: 'message' })
const sending = ref(false)
const sendError = ref(null)

// Support
const supportForm = ref({ subject: '', body: '' })
const supportSending = ref(false)
const supportSuccess = ref(false)
const supportError = ref(null)

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diffMs = now - date
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) {
      return date.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })
    } else if (diffDays === 1) {
      return 'أمس'
    } else if (diffDays < 7) {
      return `منذ ${diffDays} أيام`
    }
    return date.toLocaleDateString('ar-SA')
  } catch {
    return dateStr
  }
}

function toggleAnnouncement(announcement) {
  expandedAnnouncement.value = expandedAnnouncement.value === announcement.id ? null : announcement.id
}

function priorityBgClass(priority) {
  switch (priority) {
    case 'high': case 'urgent': return 'bg-red-100'
    case 'medium': return 'bg-yellow-100'
    default: return 'bg-blue-100'
  }
}

function priorityIconClass(priority) {
  switch (priority) {
    case 'high': case 'urgent': return 'text-red-600'
    case 'medium': return 'text-yellow-600'
    default: return 'text-blue-600'
  }
}

function priorityBadgeClass(priority) {
  switch (priority) {
    case 'high': case 'urgent': return 'badge-danger'
    case 'medium': return 'badge-warning'
    default: return 'badge-success'
  }
}

function priorityLabel(priority) {
  const labels = { high: 'عاجل', urgent: 'عاجل جداً', medium: 'متوسط', low: 'عادي', normal: 'عادي' }
  return labels[priority] || 'عادي'
}

async function viewMessage(message) {
  selectedMessage.value = message

  // Mark as read if unread
  if (!message.is_read) {
    try {
      await messagesApi.markRead(message.id)
      message.is_read = true
      if (unreadCount.value > 0) unreadCount.value--
    } catch (err) {
      console.error('Failed to mark message as read:', err)
    }
  }
}

async function sendMessage() {
  if (!composeForm.value.subject.trim() || !composeForm.value.body.trim()) return

  sending.value = true
  sendError.value = null
  try {
    await messagesApi.send({
      subject: composeForm.value.subject,
      body: composeForm.value.body,
      type: composeForm.value.type,
    })
    // Reset form
    composeForm.value = { subject: '', body: '', type: 'message' }
    showComposeForm.value = false
    // Refresh messages
    fetchMessages()
  } catch (err) {
    sendError.value = err.response?.data?.message || 'حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى.'
    console.error('Failed to send message:', err)
  } finally {
    sending.value = false
  }
}

async function submitSupportTicket() {
  if (!supportForm.value.subject.trim() || !supportForm.value.body.trim()) return

  supportSending.value = true
  supportSuccess.value = false
  supportError.value = null
  try {
    await messagesApi.send({
      subject: supportForm.value.subject,
      body: supportForm.value.body,
      type: 'support',
    })
    supportSuccess.value = true
    supportForm.value = { subject: '', body: '' }
  } catch (err) {
    supportError.value = err.response?.data?.message || 'حدث خطأ أثناء إرسال تذكرة الدعم. يرجى المحاولة مرة أخرى.'
    console.error('Failed to submit support ticket:', err)
  } finally {
    supportSending.value = false
  }
}

async function fetchAnnouncements() {
  announcementsLoading.value = true
  try {
    const { data } = await messagesApi.getAll({ type: 'announcement' })
    announcements.value = data?.messages || data?.announcements || data || []
  } catch (err) {
    console.error('Failed to fetch announcements:', err)
  } finally {
    announcementsLoading.value = false
  }
}

async function fetchMessages() {
  messagesLoading.value = true
  try {
    const { data } = await messagesApi.getAll({ type: 'message,support' })
    messages.value = data?.messages || data || []
  } catch (err) {
    console.error('Failed to fetch messages:', err)
  } finally {
    messagesLoading.value = false
  }
}

async function fetchUnreadCount() {
  try {
    const { data } = await messagesApi.getUnreadCount()
    unreadCount.value = data?.unread_count || 0
  } catch (err) {
    console.error('Failed to fetch unread count:', err)
  }
}

// Fetch tab-specific data on tab change
watch(activeTab, (newTab) => {
  if (newTab === 'messages' && messages.value.length === 0) {
    fetchMessages()
  }
})

onMounted(() => {
  fetchAnnouncements()
  fetchMessages()
  fetchUnreadCount()
})
</script>
