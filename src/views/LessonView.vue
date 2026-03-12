<template>
  <div>
    <!-- Top Bar -->
    <div class="bg-secondary text-white py-3 px-4 lg:px-8">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <router-link :to="`/programs/${$route.params.id}/units/${$route.params.unitId}`"
                     class="flex items-center gap-2 font-cairo text-[14px] hover:text-white/80 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          العودة للوحدة
        </router-link>
        <h1 class="font-arabic font-bold text-[18px]">الدرس {{ currentLessonIndex + 1 }} من {{ lessons.length }}</h1>
        <div class="flex items-center gap-2">
          <button @click="prevLesson" :disabled="currentLessonIndex === 0"
                  class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center disabled:opacity-30 hover:bg-white/30 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
          <button @click="nextLesson" :disabled="currentLessonIndex === lessons.length - 1"
                  class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center disabled:opacity-30 hover:bg-white/30 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Video Player Area -->
        <div class="flex-1 order-1">
          <!-- Video Player -->
          <div class="relative rounded-xl overflow-hidden bg-black aspect-video mb-6">
            <video
              v-if="currentLesson.videoUrl"
              ref="videoRef"
              :src="currentLesson.videoUrl"
              controls
              controlslist="nodownload"
              class="w-full h-full object-contain"
              :poster="currentLesson.thumbnail"
            ></video>
            <div v-else class="absolute inset-0 flex items-center justify-center bg-dark">
              <img :src="currentLesson.thumbnail" :alt="currentLesson.title" class="w-full h-full object-cover opacity-60" />
              <button class="absolute w-[70px] h-[70px] bg-primary rounded-full flex items-center justify-center text-white shadow-lg hover:bg-primary-dark transition-colors">
                <svg class="w-8 h-8 mr-[-2px]" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </button>
            </div>
          </div>

          <!-- Video Controls -->
          <div class="flex items-center justify-center gap-3 mb-8">
            <button class="w-10 h-10 rounded-full bg-light flex items-center justify-center text-dark hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.066 11.2a1 1 0 000 1.6l5.334 4A1 1 0 0019 16V8a1 1 0 00-1.6-.8l-5.333 4zM4.066 11.2a1 1 0 000 1.6l5.334 4A1 1 0 0011 16V8a1 1 0 00-1.6-.8l-5.334 4z"/></svg>
            </button>
            <button class="w-12 h-12 rounded-full bg-secondary flex items-center justify-center text-white hover:bg-secondary-dark transition-colors">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            </button>
            <button class="w-10 h-10 rounded-full bg-light flex items-center justify-center text-dark hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.933 12.8a1 1 0 000-1.6L6.6 7.2A1 1 0 005 8v8a1 1 0 001.6.8l5.333-4zM19.933 12.8a1 1 0 000-1.6l-5.333-4A1 1 0 0013 8v8a1 1 0 001.6.8l5.333-4z"/></svg>
            </button>
          </div>

          <!-- Lesson Info -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
            <h2 class="font-arabic font-bold text-[24px] text-dark mb-3">{{ currentLesson.title }}</h2>
            <p class="font-cairo text-[15px] text-muted leading-[28px]">{{ currentLesson.description }}</p>
          </div>
        </div>

        <!-- Lessons Sidebar -->
        <aside class="lg:w-[350px] shrink-0 order-2">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 sticky top-4">
            <div class="p-4 border-b border-gray-100">
              <h3 class="font-arabic font-bold text-[18px] text-dark">{{ unitTitle }}</h3>
              <p class="font-cairo text-[13px] text-muted mt-1">{{ lessons.length }} دروس</p>
            </div>
            <div class="max-h-[60vh] overflow-y-auto">
              <button
                v-for="(lesson, i) in lessons" :key="lesson.id"
                @click="goToLesson(lesson.id)"
                class="w-full flex items-center gap-3 p-4 border-b border-gray-50 text-right transition-colors"
                :class="lesson.id == $route.params.lessonId ? 'bg-secondary/5 border-r-4 border-r-secondary' : 'hover:bg-light'"
              >
                <!-- Thumbnail -->
                <div class="w-[80px] h-[55px] rounded-lg overflow-hidden shrink-0 relative">
                  <img :src="lesson.thumbnail" :alt="lesson.title" class="w-full h-full object-cover" />
                  <div v-if="lesson.id == $route.params.lessonId" class="absolute inset-0 bg-secondary/30 flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
                <!-- Info -->
                <div class="flex-1">
                  <p class="font-cairo text-[11px] text-secondary font-bold mb-0.5">الدرس {{ i + 1 }}</p>
                  <p class="font-cairo font-bold text-[13px] line-clamp-2"
                     :class="lesson.id == $route.params.lessonId ? 'text-secondary' : 'text-dark'">{{ lesson.title }}</p>
                  <p v-if="lesson.duration" class="font-cairo text-[11px] text-muted mt-0.5">{{ lesson.duration }}</p>
                </div>
              </button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const videoRef = ref(null)

const unitTitle = ref('أساسيات اللغة العربية')

const lessons = ref([
  { id: 1, title: 'مقدمة عن الحروف العربية', description: 'في هذا الدرس سنتعرف على الحروف الأبجدية العربية وترتيبها وأصواتها الأساسية. سنبدأ بالتعرف على كل حرف وشكله ونطقه الصحيح مع أمثلة متنوعة.', duration: '15 دقيقة', thumbnail: '/images/lessons/lesson-1.png', videoUrl: '' },
  { id: 2, title: 'حروف المد', description: 'تعلم حروف المد الثلاثة: الألف والواو والياء، وكيفية نطقها بشكل صحيح في الكلمات المختلفة.', duration: '20 دقيقة', thumbnail: '/images/lessons/lesson-2.png', videoUrl: '' },
  { id: 3, title: 'أشكال الحروف في الكلمة', description: 'الحروف العربية تتغير شكلها حسب موقعها في الكلمة. سنتعلم شكل كل حرف في أول ووسط وآخر الكلمة.', duration: '25 دقيقة', thumbnail: '/images/lessons/lesson-3.png', videoUrl: '' },
  { id: 4, title: 'التشكيل: الفتحة والضمة والكسرة', description: 'تعرف على الحركات الأساسية في اللغة العربية وكيفية تأثيرها على نطق الحروف والكلمات.', duration: '20 دقيقة', thumbnail: '/images/lessons/lesson-4.png', videoUrl: '' },
  { id: 5, title: 'السكون والشدة', description: 'تعلم السكون والشدة واستخدامهما في الكلمات العربية مع تمارين تطبيقية متنوعة.', duration: '18 دقيقة', thumbnail: '/images/lessons/lesson-5.png', videoUrl: '' },
  { id: 6, title: 'تطبيقات عملية على الوحدة', description: 'مراجعة شاملة لكل ما تعلمته في هذه الوحدة مع تمارين تطبيقية وأنشطة تفاعلية لتثبيت المعلومات.', duration: '30 دقيقة', thumbnail: '/images/lessons/lesson-6.png', videoUrl: '' },
  { id: 7, title: 'اختبار الوحدة الأولى', description: 'اختبار شامل لتقييم مستوى فهمك واستيعابك لمحتوى الوحدة الأولى.', duration: '15 دقيقة', thumbnail: '/images/lessons/lesson-7.png', videoUrl: '' },
  { id: 8, title: 'مراجعة ونتائج', description: 'مراجعة النتائج والتعرف على نقاط القوة ومجالات التحسين مع توصيات للتطوير.', duration: '10 دقيقة', thumbnail: '/images/lessons/lesson-8.png', videoUrl: '' },
])

const currentLessonIndex = computed(() => {
  const idx = lessons.value.findIndex(l => l.id == route.params.lessonId)
  return idx >= 0 ? idx : 0
})

const currentLesson = computed(() => lessons.value[currentLessonIndex.value] || lessons.value[0])

function goToLesson(lessonId) {
  router.push(`/programs/${route.params.id}/units/${route.params.unitId}/lessons/${lessonId}`)
}

function prevLesson() {
  if (currentLessonIndex.value > 0) {
    goToLesson(lessons.value[currentLessonIndex.value - 1].id)
  }
}

function nextLesson() {
  if (currentLessonIndex.value < lessons.value.length - 1) {
    goToLesson(lessons.value[currentLessonIndex.value + 1].id)
  }
}
</script>
