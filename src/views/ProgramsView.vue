<template>
  <div>
    <PageHero
      title="برامجنا التعليمية"
      subtitle="اكتشف مجموعة متنوعة من البرامج التعليمية المصممة لتناسب جميع الأعمار والمستويات"
      bg-image="/images/heroes/programs-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar Filter -->
        <aside class="lg:w-[280px] shrink-0 order-1 lg:order-2">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 sticky top-4">
            <h3 class="font-arabic font-bold text-[20px] text-dark mb-5">تصفية حسب القسم</h3>
            <div class="space-y-3">
              <label v-for="dept in departments" :key="dept" class="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  v-model="selectedDepts"
                  :value="dept"
                  class="w-4 h-4 rounded border-gray-300 text-secondary focus:ring-secondary"
                />
                <span class="font-cairo text-[15px] text-dark">{{ dept }}</span>
              </label>
            </div>
          </div>
        </aside>

        <!-- Programs Grid -->
        <div class="flex-1 order-2 lg:order-1">
          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            <div
              v-for="program in paginatedPrograms"
              :key="program.id"
              class="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div class="h-[200px] overflow-hidden">
                <img :src="program.image" :alt="program.title" class="w-full h-full object-cover" />
              </div>
              <div class="p-5 text-right">
                <span class="inline-block bg-secondary/10 text-secondary font-cairo text-xs font-bold px-3 py-1 rounded-full mb-3">
                  {{ program.department }}
                </span>
                <h3 class="font-arabic font-bold text-[18px] text-dark mb-2">{{ program.title }}</h3>
                <p class="font-cairo text-[14px] text-muted mb-4 line-clamp-2">{{ program.description }}</p>
                <div class="flex items-center justify-between text-[13px] font-cairo text-muted mb-4">
                  <span>{{ program.age }}</span>
                  <span>{{ program.duration }}</span>
                  <span class="text-primary font-bold">{{ program.price }}</span>
                </div>
                <button class="w-full bg-secondary text-white font-cairo font-bold py-2.5 rounded-lg hover:bg-secondary-dark transition-colors">
                  تفاصيل
                </button>
              </div>
            </div>
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

const departments = ['القرآن الكريم', 'اللغة العربية', 'الحضانة', 'تنمية المهارات', 'ما بعد المدرسة']
const selectedDepts = ref([])
const currentPage = ref(1)
const perPage = 6

const programs = [
  { id: 1, title: 'برنامج حفظ القرآن الكريم', department: 'القرآن الكريم', description: 'برنامج متكامل لحفظ القرآن الكريم مع التجويد والتلاوة الصحيحة تحت إشراف معلمين متخصصين.', age: '6-12 سنة', duration: '3 أشهر', price: '500 ج.م', image: '/images/programs/program-1.png' },
  { id: 2, title: 'تعليم اللغة العربية - المستوى الأول', department: 'اللغة العربية', description: 'تعلم أساسيات القراءة والكتابة بالعربية من خلال مناهج تفاعلية وممتعة.', age: '4-7 سنة', duration: '4 أشهر', price: '400 ج.م', image: '/images/programs/program-2.png' },
  { id: 3, title: 'الحضانة الصباحية', department: 'الحضانة', description: 'رعاية شاملة للأطفال مع أنشطة تعليمية وترفيهية في بيئة آمنة ومحفزة.', age: '3-5 سنة', duration: 'فصل دراسي', price: '600 ج.م', image: '/images/programs/program-3.png' },
  { id: 4, title: 'ورشة التفكير الإبداعي', department: 'تنمية المهارات', description: 'تنمية مهارات التفكير الإبداعي وحل المشكلات من خلال أنشطة عملية وورش تفاعلية.', age: '8-14 سنة', duration: '6 أسابيع', price: '350 ج.م', image: '/images/programs/program-4.png' },
  { id: 5, title: 'برنامج ما بعد المدرسة', department: 'ما بعد المدرسة', description: 'دعم أكاديمي وأنشطة ترفيهية بعد انتهاء اليوم الدراسي في بيئة محفزة.', age: '6-14 سنة', duration: 'شهري', price: '300 ج.م', image: '/images/programs/program-5.png' },
  { id: 6, title: 'برنامج التجويد المتقدم', department: 'القرآن الكريم', description: 'دراسة أحكام التجويد المتقدمة وإتقان قواعد التلاوة للطلاب المتقدمين.', age: '10-16 سنة', duration: '3 أشهر', price: '450 ج.م', image: '/images/programs/program-6.png' },
  { id: 7, title: 'النحو والصرف', department: 'اللغة العربية', description: 'دراسة قواعد النحو والصرف بأسلوب مبسط وتطبيقات عملية متنوعة.', age: '10-16 سنة', duration: '4 أشهر', price: '400 ج.م', image: '/images/programs/program-1.png' },
  { id: 8, title: 'مهارات القيادة للأطفال', department: 'تنمية المهارات', description: 'تطوير مهارات القيادة والعمل الجماعي والتواصل الفعال لدى الأطفال.', age: '8-14 سنة', duration: '8 أسابيع', price: '380 ج.م', image: '/images/programs/program-2.png' },
  { id: 9, title: 'الحضانة المسائية', department: 'الحضانة', description: 'رعاية مسائية شاملة مع أنشطة هادفة تجمع بين التعليم والمرح.', age: '3-6 سنة', duration: 'فصل دراسي', price: '550 ج.م', image: '/images/programs/program-3.png' },
]

const filteredPrograms = computed(() => {
  if (selectedDepts.value.length === 0) return programs
  return programs.filter(p => selectedDepts.value.includes(p.department))
})

const totalPages = computed(() => Math.ceil(filteredPrograms.value.length / perPage))

const paginatedPrograms = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredPrograms.value.slice(start, start + perPage)
})
</script>
