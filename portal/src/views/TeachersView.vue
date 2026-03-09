<template>
  <div>
    <PageHero
      title="فريقنا التعليمي"
      subtitle="نخبة من المعلمين والمعلمات المتخصصين في مختلف المجالات التعليمية"
      bg-image="/images/heroes/teachers-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar Filter -->
        <aside class="lg:w-[260px] shrink-0 order-1 lg:order-2">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 sticky top-4">
            <h3 class="font-arabic font-bold text-[20px] text-dark mb-5">تصفية حسب القسم</h3>
            <div class="space-y-3">
              <label v-for="dept in departments" :key="dept" class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="selectedDepts" :value="dept" class="w-4 h-4 rounded border-gray-300 text-secondary focus:ring-secondary" />
                <span class="font-cairo text-[15px] text-dark">{{ dept }}</span>
              </label>
            </div>
          </div>
        </aside>

        <!-- Teachers Grid -->
        <div class="flex-1 order-2 lg:order-1">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <router-link
              v-for="teacher in paginatedTeachers"
              :key="teacher.id"
              :to="`/teachers/${teacher.id}`"
              class="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-shadow text-center group"
            >
              <div class="h-[200px] overflow-hidden bg-gray-100">
                <img :src="teacher.image" :alt="teacher.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform" />
              </div>
              <div class="p-4">
                <h3 class="font-arabic font-bold text-[17px] text-dark mb-1">{{ teacher.name }}</h3>
                <p class="font-cairo text-[13px] text-secondary mb-2">{{ teacher.department }}</p>
                <p class="font-cairo text-[13px] text-muted line-clamp-2">{{ teacher.bio }}</p>
              </div>
            </router-link>
          </div>

          <PaginationBar v-model="currentPage" :total-pages="totalPages" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import PageHero from '@/components/PageHero.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const departments = ['القرآن الكريم', 'اللغة العربية', 'الحضانة', 'تنمية المهارات']
const selectedDepts = ref([])
const currentPage = ref(1)
const perPage = 8

const teachers = [
  { id: 1, name: 'الشيخ أحمد محمود', department: 'القرآن الكريم', bio: 'حافظ للقرآن الكريم ومتخصص في علوم التجويد والقراءات، خبرة 15 عاماً في التعليم.', image: '/images/teachers/teacher-1.png' },
  { id: 2, name: 'أ. فاطمة السيد', department: 'اللغة العربية', bio: 'معلمة لغة عربية حاصلة على ماجستير في اللغويات، خبرة 10 سنوات في تعليم الأطفال.', image: '/images/teachers/teacher-2.png' },
  { id: 3, name: 'أ. مريم عبدالله', department: 'الحضانة', bio: 'متخصصة في تربية الطفولة المبكرة مع خبرة واسعة في رعاية وتعليم الأطفال.', image: '/images/teachers/teacher-3.png' },
  { id: 4, name: 'أ. خالد إبراهيم', department: 'تنمية المهارات', bio: 'مدرب معتمد في تنمية المهارات الحياتية والتفكير الإبداعي للأطفال والناشئين.', image: '/images/teachers/teacher-4.png' },
  { id: 5, name: 'الشيخ عمر حسن', department: 'القرآن الكريم', bio: 'إجازة في القراءات العشر، متخصص في تعليم القرآن الكريم للفئات العمرية المختلفة.', image: '/images/teachers/teacher-5.png' },
  { id: 6, name: 'أ. نورا أحمد', department: 'اللغة العربية', bio: 'متخصصة في تعليم اللغة العربية للأطفال باستخدام أساليب تفاعلية حديثة.', image: '/images/teachers/teacher-6.png' },
  { id: 7, name: 'أ. سارة محمد', department: 'الحضانة', bio: 'حاصلة على دبلوم تربوي في الطفولة المبكرة مع خبرة 8 سنوات.', image: '/images/teachers/teacher-7.png' },
  { id: 8, name: 'أ. يوسف علي', department: 'تنمية المهارات', bio: 'مدرب مهارات حياتية متخصص في بناء الشخصية والقيادة للأطفال.', image: '/images/teachers/teacher-8.png' },
  { id: 9, name: 'أ. هدى إبراهيم', department: 'القرآن الكريم', bio: 'حافظة للقرآن الكريم ومعلمة تجويد بخبرة 12 عاماً في تحفيظ الأطفال.', image: '/images/teachers/teacher-9.png' },
  { id: 10, name: 'أ. عبدالرحمن سعيد', department: 'اللغة العربية', bio: 'معلم لغة عربية متميز، حاصل على بكالوريوس آداب قسم اللغة العربية.', image: '/images/teachers/teacher-10.png' },
]

const filteredTeachers = computed(() => {
  if (selectedDepts.value.length === 0) return teachers
  return teachers.filter(t => selectedDepts.value.includes(t.department))
})

const totalPages = computed(() => Math.ceil(filteredTeachers.value.length / perPage))

const paginatedTeachers = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredTeachers.value.slice(start, start + perPage)
})
</script>
