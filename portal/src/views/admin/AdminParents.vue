<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-xl font-bold text-dark">أولياء الأمور</h1>
        <p class="text-sm text-gray-500 mt-1">{{ total }} ولي أمر</p>
      </div>
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
            <tr v-for="p in parents" :key="p.id" class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors">
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

const relationLabels = {
  father: 'أب',
  mother: 'أم',
  guardian: 'ولي أمر',
  other: 'أخرى',
}
function relationLabel(val) {
  return relationLabels[val] || val
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
