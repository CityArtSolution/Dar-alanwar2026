<template>
  <div>
    <!-- Back + Header -->
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/admin/content" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-gray-500 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-dark">{{ item.name }}</h1>
        <p class="text-sm text-gray-500">{{ typeLabel(item.content_type) }}</p>
      </div>
      <span :class="item.active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'" class="text-sm">
        {{ item.active ? 'نشط' : 'معطل' }}
      </span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Actions Bar -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-2">
        <button v-if="!item.active" @click="doAction('activate')" class="btn-primary text-sm">تفعيل</button>
        <button v-if="item.active" @click="doAction('deactivate')"
                class="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm hover:bg-red-100 transition-colors">تعطيل</button>
      </div>

      <!-- Info -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
        <div class="bg-white rounded-xl border border-gray-100 p-5 lg:col-span-2">
          <h3 class="font-bold text-dark mb-4">بيانات المحتوى</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-6 text-sm">
            <div><span class="text-gray-500 block mb-0.5">الاسم</span><span class="text-dark font-medium">{{ item.name }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">التصنيف</span><span class="text-dark font-medium">{{ item.category || '—' }}</span></div>
            <div><span class="text-gray-500 block mb-0.5">النوع</span><span class="badge-info text-xs">{{ typeLabel(item.content_type) }}</span></div>
            <div>
              <span class="text-gray-500 block mb-0.5">الفئة العمرية</span>
              <span class="text-dark font-medium" v-if="item.target_age_min || item.target_age_max">
                {{ item.target_age_min || '?' }} - {{ item.target_age_max || '?' }} سنة
              </span>
              <span v-else class="text-dark font-medium">—</span>
            </div>
            <div>
              <span class="text-gray-500 block mb-0.5">الملف</span>
              <span v-if="item.has_file" class="text-green-600 font-medium">متوفر</span>
              <span v-else class="text-gray-400">غير متوفر</span>
            </div>
            <div v-if="item.file_name"><span class="text-gray-500 block mb-0.5">اسم الملف</span><span class="text-dark font-medium">{{ item.file_name }}</span></div>
            <div v-if="item.file_url"><span class="text-gray-500 block mb-0.5">رابط الملف</span><a :href="item.file_url" target="_blank" class="text-primary hover:underline text-xs">فتح الرابط</a></div>
            <div><span class="text-gray-500 block mb-0.5">حماية DRM</span><span class="text-dark font-medium">{{ item.is_drm_protected ? 'نعم' : 'لا' }}</span></div>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-gray-100 p-5 space-y-4">
          <h3 class="font-bold text-dark mb-2">إحصائيات</h3>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">عدد الوصول</span>
            <span class="font-bold text-dark text-lg">{{ item.access_count }}</span>
          </div>
          <div v-if="item.grade_levels?.length">
            <span class="text-gray-500 text-sm block mb-2">المراحل الدراسية</span>
            <div class="flex flex-wrap gap-1">
              <span v-for="g in item.grade_levels" :key="g.id" class="badge-info text-xs">{{ g.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Description -->
      <div v-if="item.description" class="bg-white rounded-xl border border-gray-100 p-5">
        <h3 class="font-bold text-dark mb-2">الوصف</h3>
        <p class="text-sm text-gray-600 whitespace-pre-wrap">{{ item.description }}</p>
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
const item = ref({})
const loading = ref(true)
const actionMsg = ref('')

const typeLabels = { book: 'كتاب', game: 'لعبة', course: 'دورة', video: 'فيديو', kids_area_activity: 'منطقة أطفال' }
function typeLabel(v) { return typeLabels[v] || v || '—' }

async function fetchData() {
  loading.value = true
  try {
    const { data } = await adminApi.getContentItem(route.params.id)
    item.value = data
  } catch (e) {
    console.error('Failed:', e)
  } finally {
    loading.value = false
  }
}

async function doAction(action) {
  try {
    const { data } = await adminApi.contentAction(route.params.id, action)
    actionMsg.value = data.message
    item.value.active = data.active
    setTimeout(() => actionMsg.value = '', 2500)
  } catch (e) {
    actionMsg.value = e.response?.data?.error || 'حدث خطأ'
    setTimeout(() => actionMsg.value = '', 2500)
  }
}

onMounted(fetchData)
</script>
