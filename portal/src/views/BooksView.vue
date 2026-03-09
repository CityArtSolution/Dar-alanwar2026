<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">المكتبة الرقمية</h1>

    <!-- Category Filter -->
    <div class="flex flex-wrap gap-2 mb-6">
      <button
        @click="selectedCategory = null"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="!selectedCategory ? 'bg-primary-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
      >
        الكل
      </button>
      <button
        v-for="cat in categories"
        :key="cat.id"
        @click="selectedCategory = cat.id"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="selectedCategory === cat.id ? 'bg-primary-500 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchBooks" class="btn-primary">إعادة المحاولة</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredBooks.length === 0" class="card text-center py-16">
      <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
      </svg>
      <p class="text-gray-500 text-lg">لا توجد كتب متاحة حالياً</p>
    </div>

    <!-- Books Grid -->
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
      <div
        v-for="book in filteredBooks"
        :key="book.id"
        @click="openBook(book)"
        class="card p-0 overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group"
      >
        <!-- Thumbnail -->
        <div class="aspect-[3/4] bg-gray-100 relative overflow-hidden">
          <img
            v-if="book.thumbnail_url"
            :src="book.thumbnail_url"
            :alt="book.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-100 to-primary-200">
            <svg class="w-12 h-12 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
          </div>
          <!-- DRM Badge -->
          <div v-if="book.is_protected" class="absolute top-2 left-2">
            <span class="bg-gray-900/70 text-white text-xs px-2 py-1 rounded-full flex items-center gap-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              محمي
            </span>
          </div>
        </div>
        <!-- Info -->
        <div class="p-3">
          <h3 class="font-bold text-sm truncate mb-1">{{ book.title }}</h3>
          <p v-if="book.category?.name" class="text-xs text-gray-500">{{ book.category.name }}</p>
          <p v-if="book.author" class="text-xs text-gray-400 mt-1">{{ book.author }}</p>
        </div>
      </div>
    </div>

    <!-- Book Detail Modal -->
    <div v-if="selectedBook" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/50" @click="selectedBook = null"></div>
      <!-- Modal Content -->
      <div class="relative bg-white rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <button @click="selectedBook = null" class="absolute top-4 left-4 p-2 rounded-lg hover:bg-gray-100 z-10">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Book Cover -->
        <div class="aspect-[3/4] max-h-64 bg-gray-100 rounded-t-2xl overflow-hidden">
          <img
            v-if="selectedBook.thumbnail_url"
            :src="selectedBook.thumbnail_url"
            :alt="selectedBook.title"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-100 to-primary-200">
            <svg class="w-16 h-16 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
          </div>
        </div>

        <div class="p-6">
          <h2 class="text-xl font-bold mb-2">{{ selectedBook.title }}</h2>
          <p v-if="selectedBook.author" class="text-gray-500 mb-1">المؤلف: {{ selectedBook.author }}</p>
          <p v-if="selectedBook.category?.name" class="text-sm text-gray-400 mb-4">التصنيف: {{ selectedBook.category.name }}</p>

          <p v-if="selectedBook.description" class="text-gray-600 text-sm leading-relaxed mb-6">
            {{ selectedBook.description }}
          </p>

          <!-- DRM Notice -->
          <div v-if="selectedBook.is_protected" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <div>
                <p class="font-medium text-yellow-800 text-sm">محتوى محمي بحقوق النشر</p>
                <p class="text-xs text-yellow-700 mt-1">هذا الكتاب محمي بنظام إدارة الحقوق الرقمية (DRM). يمكن قراءته فقط من خلال التطبيق ولا يمكن نسخه أو مشاركته.</p>
              </div>
            </div>
          </div>

          <div class="flex gap-3">
            <button v-if="selectedBook.content_url" @click="readBook(selectedBook)" class="btn-primary flex-1">
              قراءة الكتاب
            </button>
            <button @click="selectedBook = null" class="btn-secondary flex-1">
              إغلاق
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { contentApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const books = ref([])
const categories = ref([])
const selectedCategory = ref(null)
const selectedBook = ref(null)
const loading = ref(false)
const error = ref(null)

const filteredBooks = computed(() => {
  if (!selectedCategory.value) return books.value
  return books.value.filter((b) => b.category?.id === selectedCategory.value || b.category_id === selectedCategory.value)
})

function openBook(book) {
  selectedBook.value = book
}

function readBook(book) {
  if (book.content_url) {
    window.open(book.content_url, '_blank')
  }
}

async function fetchBooks() {
  loading.value = true
  error.value = null
  try {
    const [booksRes, catsRes] = await Promise.all([
      contentApi.getItems({ type: 'book' }),
      contentApi.getCategories(),
    ])
    books.value = booksRes.data?.items || booksRes.data || []
    categories.value = catsRes.data?.categories || catsRes.data || []
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل المكتبة. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch books:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBooks()
})
</script>
