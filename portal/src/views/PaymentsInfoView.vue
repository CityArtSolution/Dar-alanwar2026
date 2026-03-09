<template>
  <div>
    <PageHero
      title="المدفوعات"
      subtitle="كل ما تحتاج معرفته عن الرسوم وطرق الدفع والخصومات المتاحة"
      bg-image="/images/heroes/payments-hero.png"
    />

    <!-- Payment Methods -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16">
      <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark text-center mb-10">طرق الدفع المتاحة</h2>
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="method in paymentMethods" :key="method.title" class="bg-white rounded-xl p-6 text-center shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div class="w-16 h-16 rounded-full bg-secondary/10 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-secondary" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="method.icon"></svg>
          </div>
          <h3 class="font-arabic font-bold text-[16px] lg:text-[18px] text-dark">{{ method.title }}</h3>
        </div>
      </div>
    </section>

    <!-- Tuition Details -->
    <section class="bg-light py-16">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 text-right">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-6">تفاصيل الرسوم الدراسية</h2>
        <div class="font-cairo text-[16px] lg:text-[18px] text-muted leading-[1.9] space-y-4">
          <p>تحرص دار الأنوار على تقديم خدمات تعليمية متميزة بأسعار مناسبة تتناسب مع جميع الأسر. يتم تحديد الرسوم وفقاً للبرنامج المختار والمستوى الدراسي.</p>
          <p>يمكن سداد الرسوم على أقساط شهرية أو فصلية أو سنوية حسب رغبة ولي الأمر. جميع الرسوم شاملة للمواد التعليمية والأنشطة الأساسية.</p>
        </div>
      </div>
    </section>

    <!-- Discounts -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16">
      <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark text-center mb-10">الخصومات والعروض</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="discount in discounts" :key="discount.title" class="bg-white rounded-xl p-6 text-right shadow-sm border-2 border-dashed border-primary/30">
          <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
            <span class="text-primary font-bold text-xl">%</span>
          </div>
          <h3 class="font-arabic font-bold text-[17px] text-dark mb-2">{{ discount.title }}</h3>
          <p class="font-cairo text-[14px] text-muted">{{ discount.description }}</p>
        </div>
      </div>
    </section>

    <!-- Refund Policy -->
    <section class="bg-light py-16">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 text-right">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-6">سياسة استرداد الرسوم</h2>
        <ul class="space-y-4">
          <li v-for="(item, i) in refundPolicies" :key="i" class="flex items-start gap-3 justify-end">
            <span class="font-cairo text-[16px] text-muted">{{ item }}</span>
            <svg class="w-6 h-6 text-secondary shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
          </li>
        </ul>
      </div>
    </section>

    <!-- FAQ -->
    <section class="max-w-4xl mx-auto px-4 sm:px-6 py-16">
      <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark text-center mb-10">أسئلة شائعة عن المدفوعات</h2>
      <AccordionItem v-for="faq in faqs" :key="faq.q" :title="faq.q">
        {{ faq.a }}
      </AccordionItem>
    </section>

    <!-- CTA -->
    <section class="bg-gradient-to-l from-primary to-[#e08500] py-16 text-center text-white">
      <div class="max-w-3xl mx-auto px-4">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] mb-4">اشترك الآن</h2>
        <p class="font-cairo text-[16px] lg:text-[18px] mb-8 text-white/90">سجل أبناءك اليوم واستفد من عروضنا المميزة</p>
        <router-link to="/login" class="inline-block bg-white text-primary font-bold px-10 py-3 rounded-full hover:bg-gray-100 transition-colors font-cairo text-lg">
          سجل الآن
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import PageHero from '@/components/PageHero.vue'
import AccordionItem from '@/components/AccordionItem.vue'

const paymentMethods = [
  { title: 'الدفع الإلكتروني', icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z"/>' },
  { title: 'المحفظة الإلكترونية', icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 110 6h3.75A2.25 2.25 0 0021 13.5V12zm0 0V9.75A2.25 2.25 0 0018.75 7.5H5.25A2.25 2.25 0 003 9.75v4.5A2.25 2.25 0 005.25 16.5h13.5A2.25 2.25 0 0021 14.25V12z"/>' },
  { title: 'التحويل البنكي', icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z"/>' },
  { title: 'الدفع النقدي', icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"/>' },
]

const discounts = [
  { title: 'خصم الأشقاء', description: 'خصم 15% للأخ الثاني و25% للأخ الثالث فما فوق عند التسجيل في نفس الفترة.' },
  { title: 'خصم الدفع المبكر', description: 'خصم 10% عند سداد الرسوم الكاملة قبل بداية الفصل الدراسي بشهر.' },
  { title: 'منحة التفوق', description: 'منحة خاصة للطلاب المتفوقين في حفظ القرآن الكريم والتحصيل الدراسي.' },
  { title: 'عروض موسمية', description: 'عروض خاصة خلال شهر رمضان والعطلة الصيفية وبداية العام الدراسي.' },
]

const refundPolicies = [
  'يمكن استرداد الرسوم كاملة خلال أول أسبوع من بداية البرنامج.',
  'استرداد 75% من الرسوم خلال الأسبوعين الأولين.',
  'استرداد 50% خلال الشهر الأول من التسجيل.',
  'لا يمكن الاسترداد بعد مرور شهر من بداية البرنامج.',
  'رسوم التسجيل غير قابلة للاسترداد في جميع الحالات.',
]

const faqs = [
  { q: 'ما هي طرق الدفع المتاحة؟', a: 'نوفر عدة طرق للدفع تشمل الدفع الإلكتروني عبر البطاقات البنكية، المحفظة الإلكترونية، التحويل البنكي المباشر، والدفع النقدي في مقر المؤسسة.' },
  { q: 'هل يمكن تقسيط الرسوم الدراسية؟', a: 'نعم، يمكن تقسيط الرسوم على أقساط شهرية أو فصلية. يرجى التواصل مع إدارة الحسابات لمعرفة خطط التقسيط المتاحة.' },
  { q: 'هل يوجد خصم للأشقاء؟', a: 'نعم، نقدم خصم 15% للأخ الثاني و25% للأخ الثالث فما فوق عند تسجيلهم في نفس الفترة الدراسية.' },
  { q: 'ما هي سياسة الاسترداد في حالة الانسحاب؟', a: 'يمكن استرداد الرسوم كاملة خلال الأسبوع الأول، و75% خلال الأسبوعين الأولين، و50% خلال الشهر الأول. بعد ذلك لا يمكن الاسترداد.' },
]
</script>
