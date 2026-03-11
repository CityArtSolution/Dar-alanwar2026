<template>
  <div>
    <PageHero
      :title="program.title"
      subtitle="برامج متنوعة تلبي احتياجات الطلاب من مختلف الأعمار والمستويات"
      bg-image="/images/heroes/programs-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Main Content (Right in RTL) -->
        <div class="flex-1 order-2 lg:order-1">
          <!-- Program Description -->
          <div class="mb-10">
            <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-6">وصف البرنامج</h2>
            <div class="space-y-4">
              <p class="font-cairo text-[16px] text-muted leading-[32px]">
                {{ program.description }}
              </p>
              <p class="font-cairo text-[16px] text-muted leading-[32px]">
                {{ program.longDescription }}
              </p>
            </div>
            <!-- Program Image -->
            <div class="mt-8 rounded-xl overflow-hidden h-[300px] lg:h-[400px]">
              <img :src="program.image" :alt="program.title" class="w-full h-full object-cover" />
            </div>
          </div>

          <!-- Supporting Teachers -->
          <div class="mb-10">
            <h2 class="font-arabic font-bold text-[28px] lg:text-[32px] text-dark mb-6">المعلمين المساندين</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="teacher in program.teachers" :key="teacher.id"
                   class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
                <img :src="teacher.image" :alt="teacher.name"
                     class="w-[100px] h-[100px] rounded-full object-cover mx-auto mb-4" />
                <h3 class="font-arabic font-bold text-[18px] text-dark mb-1">{{ teacher.name }}</h3>
                <p class="font-cairo text-[14px] text-secondary mb-3">{{ teacher.title }}</p>
                <p class="font-cairo text-[13px] text-muted leading-[24px]">{{ teacher.bio }}</p>
              </div>
            </div>
          </div>

          <!-- Units Progress -->
          <div class="mb-10">
            <div class="flex items-center gap-2 overflow-x-auto pb-2">
              <router-link
                v-for="(unit, i) in program.units" :key="unit.id"
                :to="`/programs/${program.id}/units/${unit.id}`"
                class="shrink-0 flex items-center gap-2 px-5 py-3 rounded-full font-cairo font-bold text-[14px] transition-colors"
                :class="i === 0 ? 'bg-primary text-white' : 'bg-light text-dark hover:bg-primary/10'"
              >
                <span class="w-6 h-6 rounded-full flex items-center justify-center text-[12px]"
                      :class="i === 0 ? 'bg-white text-primary' : 'bg-secondary text-white'">{{ i + 1 }}</span>
                {{ unit.title }}
              </router-link>
            </div>
          </div>

          <!-- Related Programs -->
          <div>
            <h2 class="font-arabic font-bold text-[28px] lg:text-[32px] text-dark mb-6">برامج ذات صلة</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
              <div v-for="rp in relatedPrograms" :key="rp.id"
                   class="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div class="h-[180px] overflow-hidden">
                  <img :src="rp.image" :alt="rp.title" class="w-full h-full object-cover" />
                </div>
                <div class="p-5 text-right">
                  <span class="inline-block bg-secondary/10 text-secondary font-cairo text-xs font-bold px-3 py-1 rounded-full mb-3">
                    {{ rp.department }}
                  </span>
                  <h3 class="font-arabic font-bold text-[18px] text-dark mb-2">{{ rp.title }}</h3>
                  <p class="font-cairo text-[14px] text-muted mb-4 line-clamp-2">{{ rp.description }}</p>
                  <div class="flex items-center justify-between text-[13px] font-cairo text-muted mb-4">
                    <span>{{ rp.age }}</span>
                    <span>{{ rp.duration }}</span>
                    <span class="text-primary font-bold">{{ rp.price }}</span>
                  </div>
                  <router-link :to="`/programs/${rp.id}`"
                    class="block w-full bg-secondary text-white font-cairo font-bold py-2.5 rounded-lg hover:bg-secondary-dark transition-colors text-center">
                    تفاصيل
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar (Left in RTL) -->
        <aside class="lg:w-[320px] shrink-0 order-1 lg:order-2">
          <!-- Program Info Card -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 sticky top-4 mb-6">
            <h3 class="font-arabic font-bold text-[20px] text-dark mb-5">{{ program.title }}</h3>
            <div class="space-y-4 mb-6">
              <div class="flex items-center justify-between font-cairo text-[14px]">
                <span class="text-muted">المدة</span>
                <span class="text-dark font-bold">{{ program.duration }}</span>
              </div>
              <div class="flex items-center justify-between font-cairo text-[14px]">
                <span class="text-muted">الفئة العمرية</span>
                <span class="text-dark font-bold">{{ program.age }}</span>
              </div>
              <div class="flex items-center justify-between font-cairo text-[14px]">
                <span class="text-muted">القسم</span>
                <span class="text-dark font-bold">{{ program.department }}</span>
              </div>
              <div class="flex items-center justify-between font-cairo text-[14px]">
                <span class="text-muted">السعر</span>
                <span class="text-primary font-bold text-[18px]">{{ program.price }}</span>
              </div>
            </div>
            <button class="w-full bg-primary text-white font-cairo font-bold py-3 rounded-[30px] hover:bg-primary-dark transition-colors flex items-center justify-center gap-2">
              <span>سجل الآن</span>
              <div class="w-[32px] h-[32px] bg-white rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-primary" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </div>
            </button>
          </div>

          <!-- Program Content -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 class="font-arabic font-bold text-[20px] text-dark mb-5">محتوى البرنامج</h3>
            <div class="space-y-3">
              <router-link
                v-for="(unit, i) in program.units" :key="unit.id"
                :to="`/programs/${program.id}/units/${unit.id}`"
                class="flex items-center gap-3 p-3 rounded-lg hover:bg-light transition-colors group"
              >
                <span class="w-8 h-8 rounded-full bg-secondary text-white flex items-center justify-center font-cairo font-bold text-[13px] shrink-0">{{ i + 1 }}</span>
                <div class="flex-1 text-right">
                  <p class="font-cairo font-bold text-[14px] text-dark group-hover:text-secondary transition-colors">{{ unit.title }}</p>
                  <p class="font-cairo text-[12px] text-muted">{{ unit.lessonsCount }} دروس</p>
                </div>
                <svg class="w-4 h-4 text-muted rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </router-link>
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

const program = ref({
  id: route.params.id,
  title: 'برنامج تأسيس اللغة العربية للأطفال',
  department: 'اللغة العربية',
  description: 'يعتبر برنامج تأسيس اللغة العربية من أهم البرامج التعليمية في دار الأنوار، حيث يهدف إلى بناء قاعدة لغوية متينة للطفل تمكنه من القراءة والكتابة والتعبير بشكل سليم.',
  longDescription: 'يتضمن البرنامج مجموعة من الوحدات التعليمية المتدرجة التي تبدأ من تعلم الحروف الأبجدية وأشكالها، مروراً بالكلمات والجمل البسيطة، وصولاً إلى القراءة المستقلة والإملاء. يستخدم البرنامج أساليب تعليمية متنوعة تشمل الألعاب التفاعلية والقصص المصورة والأناشيد التعليمية لضمان استمتاع الطفل بعملية التعلم.',
  age: '4-7 سنة',
  duration: '4 أشهر',
  price: '400 ج.م',
  image: '/images/programs/program-2.png',
  teachers: [
    { id: 1, name: 'أحمد خالد أشرف', title: 'معلم اللغة العربية', bio: 'خبرة 10 سنوات في تعليم اللغة العربية للأطفال بأساليب حديثة ومبتكرة', image: '/images/teachers/teacher-1.png' },
    { id: 2, name: 'محمد أحمد', title: 'معلم اللغة العربية', bio: 'متخصص في تعليم القراءة والكتابة للمراحل الأولى', image: '/images/teachers/teacher-2.png' },
  ],
  units: [
    { id: 1, title: 'الوحدة الأولى: أساسيات الحروف', lessonsCount: 12 },
    { id: 2, title: 'الوحدة الثانية: تشكيل الكلمات', lessonsCount: 10 },
    { id: 3, title: 'الوحدة الثالثة: الجمل البسيطة', lessonsCount: 8 },
    { id: 4, title: 'الوحدة الرابعة: القراءة المستقلة', lessonsCount: 10 },
    { id: 5, title: 'الوحدة الخامسة: الإملاء', lessonsCount: 8 },
  ],
})

const relatedPrograms = ref([
  { id: 1, title: 'أساسيات اللغة العربية', department: 'اللغة العربية', description: 'تعلم أساسيات القراءة والكتابة بالعربية من خلال مناهج تفاعلية وممتعة.', age: '4-7 سنة', duration: '4 أشهر', price: '400 ج.م', image: '/images/programs/program-1.png' },
  { id: 6, title: 'أساسيات اللغة العربية', department: 'اللغة العربية', description: 'دراسة قواعد النحو والصرف بأسلوب مبسط وتطبيقات عملية متنوعة.', age: '10-16 سنة', duration: '4 أشهر', price: '400 ج.م', image: '/images/programs/program-2.png' },
  { id: 7, title: 'أساسيات اللغة العربية', department: 'اللغة العربية', description: 'برنامج متكامل لتعليم مهارات الكتابة الإبداعية والتعبير.', age: '8-14 سنة', duration: '3 أشهر', price: '350 ج.م', image: '/images/programs/program-3.png' },
])
</script>
