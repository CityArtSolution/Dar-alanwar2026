<template>
  <div>
    <PageHero
      :title="unit.title"
      :subtitle="unit.subtitle"
      bg-image="/images/heroes/programs-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Main Content -->
        <div class="flex-1 order-2 lg:order-1">
          <!-- Unit Description -->
          <div class="mb-10">
            <h2 class="font-arabic font-bold text-[28px] text-dark mb-4">{{ unit.title }}</h2>
            <p class="font-cairo text-[16px] text-muted leading-[32px] mb-6">{{ unit.description }}</p>
            <!-- Featured Image -->
            <div class="rounded-xl overflow-hidden h-[250px] lg:h-[350px] mb-8">
              <img :src="unit.image" :alt="unit.title" class="w-full h-full object-cover" />
            </div>
          </div>

          <!-- Lessons List -->
          <div class="mb-10">
            <h2 class="font-arabic font-bold text-[24px] text-dark mb-6">الدروس</h2>
            <div class="space-y-4">
              <router-link
                v-for="(lesson, i) in unit.lessons" :key="lesson.id"
                :to="`/programs/${$route.params.id}/units/${$route.params.unitId}/lessons/${lesson.id}`"
                class="flex items-center gap-4 bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md hover:border-secondary/30 transition-all group"
              >
                <!-- Lesson Thumbnail -->
                <div class="w-[120px] h-[80px] rounded-lg overflow-hidden shrink-0 relative">
                  <img :src="lesson.thumbnail" :alt="lesson.title" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                </div>
                <!-- Lesson Info -->
                <div class="flex-1 text-right">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-cairo text-[12px] text-secondary font-bold">الدرس {{ i + 1 }}</span>
                    <span v-if="lesson.duration" class="font-cairo text-[12px] text-muted">{{ lesson.duration }}</span>
                  </div>
                  <h3 class="font-arabic font-bold text-[16px] text-dark group-hover:text-secondary transition-colors">{{ lesson.title }}</h3>
                  <p class="font-cairo text-[13px] text-muted line-clamp-1 mt-1">{{ lesson.description }}</p>
                </div>
                <!-- Arrow -->
                <svg class="w-5 h-5 text-muted rotate-180 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </router-link>
            </div>
          </div>

          <!-- Unit Materials -->
          <div v-if="unit.materials && unit.materials.length">
            <h2 class="font-arabic font-bold text-[24px] text-dark mb-6">المواد المساعدة</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="material in unit.materials" :key="material.id"
                   class="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div class="h-[140px] overflow-hidden">
                  <img :src="material.image" :alt="material.title" class="w-full h-full object-cover" />
                </div>
                <div class="p-4 text-right">
                  <h3 class="font-cairo font-bold text-[14px] text-dark mb-1">{{ material.title }}</h3>
                  <p class="font-cairo text-[12px] text-muted">{{ material.type }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="lg:w-[300px] shrink-0 order-1 lg:order-2">
          <!-- Navigation -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 sticky top-4 mb-6">
            <div class="flex items-center justify-between mb-4">
              <router-link :to="`/programs/${$route.params.id}`" class="font-cairo text-[14px] text-secondary hover:underline flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                العودة للبرنامج
              </router-link>
            </div>
            <h3 class="font-arabic font-bold text-[18px] text-dark mb-4">الوحدات</h3>
            <div class="space-y-2">
              <router-link
                v-for="(u, i) in allUnits" :key="u.id"
                :to="`/programs/${$route.params.id}/units/${u.id}`"
                class="flex items-center gap-3 p-3 rounded-lg transition-colors"
                :class="u.id == $route.params.unitId ? 'bg-secondary/10 text-secondary' : 'hover:bg-light text-dark'"
              >
                <span class="w-7 h-7 rounded-full flex items-center justify-center font-cairo font-bold text-[12px] shrink-0"
                      :class="u.id == $route.params.unitId ? 'bg-secondary text-white' : 'bg-gray-200 text-dark'">{{ i + 1 }}</span>
                <span class="font-cairo text-[13px] font-bold">{{ u.title }}</span>
              </router-link>
            </div>
          </div>

          <!-- Unit Progress -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 class="font-arabic font-bold text-[18px] text-dark mb-4">التقدم</h3>
            <div class="mb-4">
              <div class="flex items-center justify-between font-cairo text-[13px] mb-2">
                <span class="text-muted">الدروس المكتملة</span>
                <span class="text-dark font-bold">{{ unit.completedLessons }} / {{ unit.lessons.length }}</span>
              </div>
              <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-secondary rounded-full transition-all" :style="{ width: progressPercent + '%' }"></div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import PageHero from '@/components/PageHero.vue'

const route = useRoute()

const unit = ref({
  id: route.params.unitId,
  title: 'الوحدة الأولى: أساسيات الحروف',
  subtitle: 'في هذه الوحدة سنتعلم الحروف الأبجدية وأشكالها المختلفة',
  description: 'تعتبر هذه الوحدة الأساس في تعلم اللغة العربية، حيث يتعرف الطالب على الحروف الأبجدية بأشكالها المختلفة (أول - وسط - آخر الكلمة) مع التشكيل الصحيح والنطق السليم.',
  image: '/images/programs/unit-cover.png',
  completedLessons: 4,
  lessons: [
    { id: 1, title: 'مقدمة عن الحروف العربية', description: 'تعرف على الحروف الأبجدية العربية وترتيبها', duration: '15 دقيقة', thumbnail: '/images/lessons/lesson-1.png' },
    { id: 2, title: 'حروف المد', description: 'تعلم حروف المد الثلاثة: الألف والواو والياء', duration: '20 دقيقة', thumbnail: '/images/lessons/lesson-2.png' },
    { id: 3, title: 'أشكال الحروف', description: 'الحروف في أول ووسط وآخر الكلمة', duration: '25 دقيقة', thumbnail: '/images/lessons/lesson-3.png' },
    { id: 4, title: 'التشكيل: الفتحة والضمة والكسرة', description: 'تعرف على الحركات الأساسية وكيفية نطقها', duration: '20 دقيقة', thumbnail: '/images/lessons/lesson-4.png' },
    { id: 5, title: 'السكون والشدة', description: 'تعلم السكون والشدة واستخدامهما في الكلمات', duration: '18 دقيقة', thumbnail: '/images/lessons/lesson-5.png' },
    { id: 6, title: 'تطبيقات عملية', description: 'تمارين وتطبيقات على ما تعلمته في هذه الوحدة', duration: '30 دقيقة', thumbnail: '/images/lessons/lesson-6.png' },
  ],
  materials: [
    { id: 1, title: 'سلم القراءة', type: 'كتاب تفاعلي', image: '/images/books/book-1.png' },
    { id: 2, title: 'سلم القراءة 2', type: 'كتاب تفاعلي', image: '/images/books/book-2.png' },
    { id: 3, title: 'سلم القراءة 3', type: 'كتاب تفاعلي', image: '/images/books/book-3.png' },
  ],
})

const allUnits = ref([
  { id: 1, title: 'أساسيات الحروف' },
  { id: 2, title: 'تشكيل الكلمات' },
  { id: 3, title: 'الجمل البسيطة' },
  { id: 4, title: 'القراءة المستقلة' },
  { id: 5, title: 'الإملاء' },
])

const progressPercent = computed(() => {
  if (!unit.value.lessons.length) return 0
  return Math.round((unit.value.completedLessons / unit.value.lessons.length) * 100)
})
</script>
