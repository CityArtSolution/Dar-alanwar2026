<template>
  <div>
    <PageHero
      title="خدماتنا"
      subtitle="نقدم في دار الأنوار مجموعة متنوعة من الخدمات التعليمية المتميزة"
      bg-image="/images/heroes/services-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-16 space-y-20">
      <!-- Service 1: Quran -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="rounded-xl overflow-hidden order-2 lg:order-1">
          <img src="/images/services/quran-teaching.png" alt="تعليم القرآن الكريم" class="w-full h-[300px] lg:h-[380px] object-cover rounded-xl" />
        </div>
        <div class="text-right order-1 lg:order-2">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-4">التعليم الديني والقرآن الكريم</h2>
          <p class="font-cairo text-[16px] lg:text-[18px] text-muted leading-relaxed">
            نوفر بيئة تعليمية متميزة لتحفيظ القرآن الكريم وتعليم أحكام التجويد والتلاوة الصحيحة. يشرف على البرنامج نخبة من المعلمين المتخصصين في علوم القرآن، مع استخدام أحدث الأساليب التعليمية التي تناسب جميع الفئات العمرية. نهدف إلى غرس حب القرآن في نفوس الأطفال وتعزيز ارتباطهم بكتاب الله.
          </p>
        </div>
      </div>

      <!-- Service 2: Arabic -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="text-right">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-4">اللغة العربية</h2>
          <p class="font-cairo text-[16px] lg:text-[18px] text-muted leading-relaxed">
            برامج متخصصة في تعليم اللغة العربية تشمل القراءة والكتابة والنحو والصرف والبلاغة. نستخدم مناهج تفاعلية تجعل تعلم اللغة العربية ممتعاً ومشوقاً للأطفال. يتم تقسيم الطلاب إلى مستويات مختلفة لضمان تقدم كل طالب وفقاً لقدراته ومستواه اللغوي.
          </p>
        </div>
        <div class="rounded-xl overflow-hidden">
          <img src="/images/services/arabic-calligraphy.png" alt="اللغة العربية" class="w-full h-[300px] lg:h-[380px] object-cover rounded-xl" />
        </div>
      </div>

      <!-- Service 3: Nursery -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="rounded-xl overflow-hidden order-2 lg:order-1">
          <img src="/images/services/arabic-laptop.png" alt="قسم الحضانة" class="w-full h-[300px] lg:h-[380px] object-cover rounded-xl" />
        </div>
        <div class="text-right order-1 lg:order-2">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-4">قسم الحضانة</h2>
          <p class="font-cairo text-[16px] lg:text-[18px] text-muted leading-relaxed">
            حضانة متكاملة توفر رعاية شاملة للأطفال من سن مبكرة في بيئة آمنة ومحفزة. نقدم أنشطة تعليمية وترفيهية متنوعة تساعد على تنمية المهارات الحركية والإدراكية والاجتماعية. فريقنا مدرب على أحدث أساليب التعامل مع الأطفال لضمان نموهم السليم.
          </p>
        </div>
      </div>

      <!-- Service 4: Skills -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="text-right">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-4">برامج تنمية المهارات</h2>
          <p class="font-cairo text-[16px] lg:text-[18px] text-muted leading-relaxed">
            برامج متخصصة في تنمية مهارات الأطفال المختلفة تشمل التفكير الإبداعي وحل المشكلات والعمل الجماعي. نوفر ورش عمل تفاعلية وأنشطة عملية تساعد الأطفال على اكتشاف مواهبهم وتطوير قدراتهم في مختلف المجالات.
          </p>
        </div>
        <div class="rounded-xl overflow-hidden">
          <img src="/images/services/tajweed-family.png" alt="تنمية المهارات" class="w-full h-[300px] lg:h-[380px] object-cover rounded-xl" />
        </div>
      </div>

      <!-- Service 5: After-school -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
        <div class="rounded-xl overflow-hidden order-2 lg:order-1">
          <img src="/images/services/kids-classroom.png" alt="برامج ما بعد المدرسة" class="w-full h-[300px] lg:h-[380px] object-cover rounded-xl" />
        </div>
        <div class="text-right order-1 lg:order-2">
          <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-4">برامج ما بعد المدرسة</h2>
          <p class="font-cairo text-[16px] lg:text-[18px] text-muted leading-relaxed">
            برامج متكاملة تستقبل الأطفال بعد انتهاء اليوم الدراسي وتوفر لهم بيئة آمنة ومحفزة للتعلم والترفيه. تشمل البرامج مساعدة في الواجبات المدرسية وأنشطة رياضية وفنية ودورات تعليمية إضافية تكمل المنهج الدراسي.
          </p>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <section class="bg-gradient-to-l from-primary to-primary-dark py-16 text-center text-white">
      <div class="max-w-3xl mx-auto px-4">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] mb-4">سجل أبناءك الآن</h2>
        <p class="font-cairo text-[16px] lg:text-[18px] mb-8 text-white/90">انضم إلى عائلة دار الأنوار واستفد من جميع خدماتنا التعليمية المتميزة</p>
        <router-link to="/login" class="inline-block bg-white text-primary font-bold px-10 py-3 rounded-full hover:bg-gray-100 transition-colors font-cairo text-lg">
          سجل الآن
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import PageHero from '@/components/PageHero.vue'
</script>
