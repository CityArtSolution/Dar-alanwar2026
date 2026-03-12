<template>
  <div>
    <PageHero
      title="قصة دار الأنوار"
      subtitle="رحلتنا في بناء جيل واعٍ ومتعلم"
      bg-class="bg-primary"
      bg-image="/images/heroes/about-hero.png"
    />

    <!-- Story Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="text-right">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-6">من نحن</h2>
          <div class="font-cairo text-[16px] lg:text-[18px] text-muted leading-[1.9] space-y-4">
            <p>تأسست دار الأنوار عام 2015 بهدف توفير بيئة تعليمية إسلامية متميزة تجمع بين الأصالة والمعاصرة. بدأنا بفصل واحد لتحفيظ القرآن الكريم، واليوم نفتخر بخدمة مئات الطلاب في مختلف البرامج التعليمية.</p>
            <p>نؤمن بأن كل طفل يحمل في داخله بذور التميز والإبداع، ومهمتنا هي رعاية هذه البذور وتنميتها في بيئة آمنة ومحفزة تحت إشراف نخبة من المعلمين المتخصصين.</p>
          </div>
        </div>
        <div class="rounded-2xl h-[350px] overflow-hidden">
          <img src="/images/about/founder.png" alt="المؤسس" class="w-full h-full object-cover rounded-2xl" />
        </div>
      </div>
    </section>

    <!-- Vision & Mission -->
    <section class="bg-light py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="bg-white rounded-2xl p-8 text-right border-r-4 border-secondary shadow-sm">
            <h3 class="font-arabic font-bold text-[24px] text-secondary mb-4">رؤيتنا</h3>
            <p class="font-cairo text-[16px] text-muted leading-relaxed">
              أن نكون المؤسسة التعليمية الرائدة في تقديم تعليم إسلامي شامل ومتميز يجمع بين العلم الشرعي والمعرفة العصرية، لبناء جيل مؤمن واعٍ قادر على المساهمة الفعالة في مجتمعه.
            </p>
          </div>
          <div class="bg-white rounded-2xl p-8 text-right border-r-4 border-primary shadow-sm">
            <h3 class="font-arabic font-bold text-[24px] text-primary mb-4">رسالتنا</h3>
            <p class="font-cairo text-[16px] text-muted leading-relaxed">
              توفير بيئة تعليمية آمنة ومحفزة تعمل على تنمية الجوانب الروحية والعقلية والاجتماعية للطفل، من خلال برامج تعليمية متنوعة يشرف عليها كوادر مؤهلة ومتخصصة.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16">
      <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark text-center mb-10">فريقنا المتميز</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="member in teamMembers" :key="member.name" class="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 text-center">
          <div class="h-[180px] overflow-hidden">
            <img :src="member.image" :alt="member.name" class="w-full h-full object-cover" />
          </div>
          <div class="p-4">
            <h3 class="font-arabic font-bold text-[17px] text-dark">{{ member.name }}</h3>
            <p class="font-cairo text-[14px] text-secondary">{{ member.role }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Partners -->
    <section class="bg-light py-12">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 text-center">
        <h2 class="font-arabic font-bold text-[28px] text-dark mb-8">شركاؤنا</h2>
        <div class="flex flex-wrap items-center justify-center gap-8">
          <img src="/images/about/partners.png" alt="شركاؤنا" class="max-w-full h-auto" />
        </div>
      </div>
    </section>

    <!-- Achievements Accordion -->
    <section class="max-w-4xl mx-auto px-4 sm:px-6 py-16">
      <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark text-center mb-10">إنجازاتنا ومحطاتنا</h2>
      <div class="space-y-3">
        <div
          v-for="milestone in milestones"
          :key="milestone.year"
          @click="milestone.open = !milestone.open"
          class="bg-gradient-to-l from-primary to-primary-dark rounded-xl overflow-hidden cursor-pointer"
        >
          <div class="flex items-center justify-between px-6 py-4 text-white">
            <svg :class="['w-5 h-5 transition-transform duration-300', milestone.open && 'rotate-180']" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
            <div class="text-right">
              <span class="font-arabic font-bold text-[18px]">{{ milestone.year }}</span>
              <span class="mx-3">-</span>
              <span class="font-cairo text-[16px]">{{ milestone.title }}</span>
            </div>
          </div>
          <Transition
            enter-active-class="transition-all duration-300"
            enter-from-class="max-h-0 opacity-0"
            enter-to-class="max-h-40 opacity-100"
            leave-active-class="transition-all duration-200"
            leave-from-class="max-h-40 opacity-100"
            leave-to-class="max-h-0 opacity-0"
          >
            <div v-show="milestone.open" class="overflow-hidden">
              <p class="px-6 pb-4 text-right font-cairo text-[14px] text-white/80">{{ milestone.description }}</p>
            </div>
          </Transition>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="relative py-20 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary to-secondary-dark"></div>
      <div class="relative z-10 max-w-3xl mx-auto px-4 text-center text-white">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] mb-4">انضم إلى عائلة دار الأنوار</h2>
        <p class="font-cairo text-[16px] lg:text-[18px] mb-8 text-white/90">سجل أبناءك الآن وامنحهم فرصة التعلم في بيئة إسلامية متميزة</p>
        <router-link to="/login" class="inline-block bg-white text-secondary font-bold px-10 py-3 rounded-full hover:bg-gray-100 transition-colors font-cairo text-lg">
          سجل الآن
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import PageHero from '@/components/PageHero.vue'

const teamMembers = [
  { name: 'أ. محمد عبدالله', role: 'المدير العام', image: '/images/about/team-1.png' },
  { name: 'أ. أحمد محمود', role: 'مدير البرامج التعليمية', image: '/images/about/team-2.png' },
  { name: 'أ. فاطمة السيد', role: 'مديرة قسم الحضانة', image: '/images/about/team-3.png' },
  { name: 'أ. خالد إبراهيم', role: 'منسق الأنشطة', image: '/images/about/team-4.png' },
]

const milestones = reactive([
  { year: '2015', title: 'تأسيس دار الأنوار', description: 'انطلقنا بفصل واحد لتحفيظ القرآن الكريم مع 20 طالباً و3 معلمين متخصصين.', open: false },
  { year: '2017', title: 'إضافة قسم اللغة العربية', description: 'توسعنا بإضافة برامج تعليم اللغة العربية للأطفال بمناهج تفاعلية حديثة.', open: false },
  { year: '2019', title: 'افتتاح قسم الحضانة', description: 'افتتحنا قسم الحضانة لاستقبال الأطفال من سن 3 سنوات في بيئة آمنة ومحفزة.', open: false },
  { year: '2021', title: 'إطلاق برامج تنمية المهارات', description: 'أضفنا برامج متخصصة في تنمية المهارات الحياتية والتفكير الإبداعي.', open: false },
  { year: '2024', title: 'إطلاق المنصة الإلكترونية', description: 'أطلقنا منصتنا الرقمية لتسهيل التواصل مع أولياء الأمور ومتابعة تقدم الطلاب.', open: false },
])
</script>
