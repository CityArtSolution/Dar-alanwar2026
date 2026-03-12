<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">المحتوى</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} عنصر</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-4 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px]">
        <input v-model="search" type="text" placeholder="بحث بالاسم..."
               class="input-field text-sm w-full" />
      </div>
      <select v-model="filterType" class="input-field text-sm w-auto min-w-[140px]">
        <option value="">كل الأنواع</option>
        <option value="book">كتاب</option>
        <option value="game">لعبة</option>
        <option value="course">دورة</option>
        <option value="video">فيديو</option>
        <option value="kids_area">منطقة أطفال</option>
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
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الاسم</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">التصنيف</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">النوع</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الفئة العمرية</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الوصول</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">ملف</th>
              <th class="text-right py-3 px-4 text-gray-500 font-medium text-xs">الحالة</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!items.length">
              <td colspan="7" class="py-10 text-center text-gray-400 text-sm">لا توجد نتائج</td>
            </tr>
            <tr v-for="c in items" :key="c.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors cursor-pointer" @click="$router.push('/admin/content/' + c.id)">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-violet-50 rounded-lg flex items-center justify-center shrink-0">
                    <span class="text-xs font-bold text-violet-600">{{ typeIcon(c.content_type) }}</span>
                  </div>
                  <span class="font-medium text-dark">{{ c.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-600">{{ c.category || '—' }}</td>
              <td class="py-3 px-4">
                <span class="badge-info text-xs">{{ typeLabel(c.content_type) }}</span>
              </td>
              <td class="py-3 px-4 text-gray-500 text-xs">
                <span v-if="c.target_age_min || c.target_age_max">
                  {{ c.target_age_min || '?' }} - {{ c.target_age_max || '?' }} سنة
                </span>
                <span v-else>—</span>
              </td>
              <td class="py-3 px-4 text-dark font-medium">{{ c.access_count }}</td>
              <td class="py-3 px-4">
                <span v-if="c.has_file" class="text-green-600 text-xs">متوفر</span>
                <span v-else class="text-gray-400 text-xs">—</span>
              </td>
              <td class="py-3 px-4">
                <span :class="c.active ? 'badge-success' : 'bg-red-50 text-red-700 text-xs px-2 py-0.5 rounded-full'">
                  {{ c.active ? 'نشط' : 'معطل' }}
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
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { adminApi } from '@/services/adminApi'

const search = ref('')
const filterType = ref('')
const items = ref([])
const total = ref(0)
const page = ref(1)
const totalPages = ref(1)
const loading = ref(true)

let searchTimeout = null

const typeLabels = { book: 'كتاب', game: 'لعبة', course: 'دورة', video: 'فيديو', kids_area: 'منطقة أطفال' }
const typeIcons = { book: 'ك', game: 'ل', course: 'د', video: 'ف', kids_area: 'ط' }

function typeLabel(v) { return typeLabels[v] || v }
function typeIcon(v) { return typeIcons[v] || '؟' }

async function fetchContent() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (filterType.value) params.type = filterType.value
    const { data } = await adminApi.getContent(params)
    items.value = data.content || []
    total.value = data.total || 0
    totalPages.value = data.pages || 1
  } catch (e) {
    console.error('Failed to load content:', e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchContent()
}

watch(search, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchContent()
  }, 400)
})

watch(filterType, () => {
  page.value = 1
  fetchContent()
})

onMounted(fetchContent)
</script>
