<template>
  <div>
    <PageHero title="فريقنا التعليمي" subtitle="تعرف على معلمينا المتميزين" bg-image="/images/heroes/teachers-hero.png" />

    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <!-- Profile Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-10 mb-10">
        <div class="flex flex-col md:flex-row gap-8 items-start">
          <!-- Photo -->
          <div class="w-[180px] h-[180px] shrink-0 rounded-2xl overflow-hidden mx-auto md:mx-0">
            <img :src="teacher.image" :alt="teacher.name" class="w-full h-full object-cover" />
          </div>
          <!-- Info -->
          <div class="flex-1 text-right">
            <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-2">{{ teacher.name }}</h2>
            <p class="font-cairo text-secondary text-[16px] lg:text-[18px] mb-4">{{ teacher.department }}</p>
            <div class="space-y-2 font-cairo text-[15px] text-muted">
              <p class="flex items-center gap-2 justify-end">
                <span>{{ teacher.phone }}</span>
                <svg class="w-5 h-5 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
              </p>
              <p class="flex items-center gap-2 justify-end">
                <span>{{ teacher.subjects.join(' ، ') }}</span>
                <svg class="w-5 h-5 text-secondary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Bio Section -->
      <div class="mb-12 text-right">
        <h3 class="font-arabic font-bold text-[24px] text-dark mb-4">السيرة الذاتية والمؤهلات</h3>
        <div class="font-cairo text-[16px] text-muted leading-[1.8] space-y-3">
          <p>{{ teacher.bio }}</p>
          <p>{{ teacher.qualifications }}</p>
        </div>
      </div>

      <!-- Courses -->
      <div class="mb-12">
        <h3 class="font-arabic font-bold text-[24px] text-dark mb-6 text-right">الدورات والكتب</h3>
        <div class="flex gap-4 overflow-x-auto pb-4" dir="rtl">
          <div
            v-for="course in teacher.courses"
            :key="course.title"
            class="shrink-0 w-[200px] bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
          >
            <div class="h-[140px] bg-gradient-to-br from-primary/15 to-primary/5 flex items-center justify-center">
              <svg class="w-12 h-12 text-primary/30" fill="currentColor" viewBox="0 0 24 24"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <div class="p-3 text-right">
              <h4 class="font-cairo font-bold text-[14px] text-dark">{{ course.title }}</h4>
              <p class="font-cairo text-[12px] text-muted">{{ course.type }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Related Programs -->
      <div>
        <h3 class="font-arabic font-bold text-[24px] text-dark mb-6 text-right">البرامج ذات الصلة</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="program in teacher.programs"
            :key="program"
            class="bg-white rounded-xl p-5 shadow-sm border border-gray-100 text-right"
          >
            <span class="inline-block bg-secondary/10 text-secondary font-cairo text-xs font-bold px-3 py-1 rounded-full mb-2">{{ teacher.department }}</span>
            <h4 class="font-arabic font-bold text-[16px] text-dark">{{ program }}</h4>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PageHero from '@/components/PageHero.vue'

const route = useRoute()

const teachersData = [
  {
    id: '1', name: 'الشيخ أحمد محمود', department: 'القرآن الكريم', phone: '01012345678', image: '/images/teachers/teacher-1.png',
    subjects: ['تحفيظ القرآن', 'التجويد', 'القراءات'],
    bio: 'حافظ للقرآن الكريم برواية حفص عن عاصم، حاصل على إجازة في القراءات العشر من الأزهر الشريف. متخصص في علوم التجويد والقراءات مع خبرة تمتد لأكثر من 15 عاماً في تعليم القرآن الكريم للأطفال والكبار.',
    qualifications: 'ليسانس كلية القرآن الكريم - جامعة الأزهر. دبلوم خاص في طرق تدريس القرآن الكريم. إجازة في القراءات العشر الصغرى.',
    courses: [
      { title: 'أساسيات التجويد', type: 'دورة' },
      { title: 'حفظ جزء عم', type: 'دورة' },
      { title: 'القاعدة النورانية', type: 'كتاب' },
    ],
    programs: ['برنامج حفظ القرآن الكريم', 'برنامج التجويد المتقدم', 'حلقة المراجعة الأسبوعية'],
  },
  {
    id: '2', name: 'أ. فاطمة السيد', department: 'اللغة العربية', phone: '01098765432', image: '/images/teachers/teacher-2.png',
    subjects: ['القراءة', 'الكتابة', 'النحو'],
    bio: 'معلمة لغة عربية متميزة حاصلة على ماجستير في اللغويات العربية من جامعة القاهرة. تتمتع بخبرة 10 سنوات في تعليم اللغة العربية للأطفال باستخدام أساليب تفاعلية حديثة.',
    qualifications: 'ماجستير في اللغويات العربية - جامعة القاهرة. بكالوريوس تربية قسم اللغة العربية. شهادة في تعليم اللغة العربية لغير الناطقين بها.',
    courses: [
      { title: 'أساسيات القراءة', type: 'دورة' },
      { title: 'الكتابة الإبداعية', type: 'دورة' },
      { title: 'نحو مبسط', type: 'كتاب' },
    ],
    programs: ['تعليم اللغة العربية - المستوى الأول', 'النحو والصرف', 'الكتابة الإبداعية'],
  },
]

const teacher = computed(() => {
  return teachersData.find(t => t.id === route.params.id) || teachersData[0]
})
</script>
