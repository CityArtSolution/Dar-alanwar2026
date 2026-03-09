<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">الدورات والفيديوهات</h1>

    <!-- Filters -->
    <div class="flex flex-col sm:flex-row gap-4 mb-6">
      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2 flex-1">
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

      <!-- Grade Filter -->
      <select
        v-model="selectedGrade"
        class="input-field w-full sm:w-48 flex-shrink-0"
      >
        <option :value="null">جميع المراحل</option>
        <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card text-center py-10">
      <p class="text-red-500 mb-4">{{ error }}</p>
      <button @click="fetchCourses" class="btn-primary">إعادة المحاولة</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredCourses.length === 0" class="card text-center py-16">
      <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
      </svg>
      <p class="text-gray-500 text-lg">لا توجد دورات متاحة حالياً</p>
    </div>

    <!-- Courses Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="course in filteredCourses"
        :key="course.id"
        @click="openCourse(course)"
        class="card p-0 overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group"
      >
        <!-- Thumbnail -->
        <div class="aspect-video bg-gray-100 relative overflow-hidden">
          <img
            v-if="course.thumbnail_url"
            :src="course.thumbnail_url"
            :alt="course.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-100 to-blue-200">
            <svg class="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
          </div>
          <!-- Play Icon Overlay -->
          <div class="absolute inset-0 flex items-center justify-center bg-black/0 group-hover:bg-black/20 transition-colors">
            <div class="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg">
              <svg class="w-6 h-6 text-primary-600 mr-[-2px]" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
          </div>
          <!-- Duration Badge -->
          <div v-if="course.duration" class="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
            {{ course.duration }}
          </div>
        </div>

        <!-- Info -->
        <div class="p-4">
          <h3 class="font-bold mb-1 line-clamp-2">{{ course.title }}</h3>
          <p v-if="course.description" class="text-sm text-gray-500 line-clamp-2 mb-3">{{ course.description }}</p>
          <div class="flex items-center justify-between text-xs text-gray-400">
            <span v-if="course.category?.name">{{ course.category.name }}</span>
            <span v-if="course.instructor">{{ course.instructor }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Course Detail Modal -->
    <div v-if="selectedCourse" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50" @click="closeCourse"></div>
      <div class="relative bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <button @click="closeCourse" class="absolute top-4 left-4 p-2 rounded-lg hover:bg-gray-100 z-10 bg-white/80">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Video Player -->
        <div class="aspect-video bg-black rounded-t-2xl overflow-hidden relative">
          <video
            v-if="isPlaying && (selectedCourse.video_url || selectedCourse.content_url)"
            ref="videoPlayer"
            :src="selectedCourse.video_url || selectedCourse.content_url"
            :poster="selectedCourse.thumbnail_url"
            controls
            controlsList="nodownload"
            class="w-full h-full"
            autoplay
          ></video>
          <template v-else>
            <img
              v-if="selectedCourse.thumbnail_url"
              :src="selectedCourse.thumbnail_url"
              :alt="selectedCourse.title"
              class="absolute inset-0 w-full h-full object-cover opacity-50"
            />
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-center">
                <button
                  v-if="selectedCourse.video_url || selectedCourse.content_url"
                  @click="isPlaying = true"
                  class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white/30 transition-colors mb-3"
                >
                  <svg class="w-10 h-10 text-white mr-[-4px]" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </button>
                <p v-else class="text-gray-400 text-sm">الفيديو غير متاح حالياً</p>
                <p v-if="selectedCourse.duration" class="text-white/70 text-sm">{{ selectedCourse.duration }}</p>
              </div>
            </div>
          </template>
        </div>

        <!-- Course Details -->
        <div class="p-6">
          <h2 class="text-xl font-bold mb-2">{{ selectedCourse.title }}</h2>

          <div class="flex flex-wrap gap-3 mb-4 text-sm text-gray-500">
            <span v-if="selectedCourse.instructor" class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              {{ selectedCourse.instructor }}
            </span>
            <span v-if="selectedCourse.category?.name" class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
              </svg>
              {{ selectedCourse.category.name }}
            </span>
            <span v-if="selectedCourse.duration" class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ selectedCourse.duration }}
            </span>
          </div>

          <p v-if="selectedCourse.description" class="text-gray-600 leading-relaxed mb-6">
            {{ selectedCourse.description }}
          </p>

          <!-- Lessons List (if available) -->
          <div v-if="selectedCourse.lessons && selectedCourse.lessons.length > 0" class="mb-6">
            <h3 class="font-bold mb-3">محتوى الدورة</h3>
            <div class="divide-y divide-gray-100 border border-gray-200 rounded-lg">
              <div v-for="(lesson, index) in selectedCourse.lessons" :key="lesson.id || index" class="flex items-center gap-3 p-3 hover:bg-gray-50">
                <span class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-sm font-medium text-primary-600 flex-shrink-0">
                  {{ index + 1 }}
                </span>
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-sm truncate">{{ lesson.title }}</p>
                  <p v-if="lesson.duration" class="text-xs text-gray-400">{{ lesson.duration }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex gap-3">
            <button @click="closeCourse" class="btn-secondary flex-1">إغلاق</button>
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
const courses = ref([])
const categories = ref([])
const grades = ref([])
const selectedCategory = ref(null)
const selectedGrade = ref(null)
const selectedCourse = ref(null)
const loading = ref(false)
const error = ref(null)

const filteredCourses = computed(() => {
  let result = courses.value
  if (selectedCategory.value) {
    result = result.filter((c) => c.category?.id === selectedCategory.value || c.category_id === selectedCategory.value)
  }
  if (selectedGrade.value) {
    result = result.filter((c) => c.grade === selectedGrade.value)
  }
  return result
})

const videoPlayer = ref(null)
const isPlaying = ref(false)

function openCourse(course) {
  selectedCourse.value = course
  isPlaying.value = false
  // Fetch full course details (e.g. lessons list)
  fetchCourseDetail(course.id)
}

function closeCourse() {
  selectedCourse.value = null
  isPlaying.value = false
}

async function fetchCourseDetail(id) {
  try {
    const { data } = await contentApi.getDetail(id)
    // Merge detail into selected course to get lessons, etc.
    selectedCourse.value = { ...selectedCourse.value, ...data }
  } catch (err) {
    console.error('Failed to fetch course detail:', err)
  }
}

async function fetchCourses() {
  loading.value = true
  error.value = null
  try {
    const [coursesRes, catsRes] = await Promise.all([
      contentApi.getItems({ type: 'course,video' }),
      contentApi.getCategories(),
    ])
    courses.value = coursesRes.data?.items || coursesRes.data || []
    categories.value = catsRes.data?.categories || catsRes.data || []

    // Extract unique grades from courses
    const gradeSet = new Set()
    courses.value.forEach((c) => {
      if (c.grade) gradeSet.add(c.grade)
    })
    grades.value = Array.from(gradeSet).sort()
  } catch (err) {
    error.value = 'حدث خطأ أثناء تحميل الدورات. يرجى المحاولة مرة أخرى.'
    console.error('Failed to fetch courses:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCourses()
})
</script>
