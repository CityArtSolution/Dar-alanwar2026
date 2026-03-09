<template>
  <div>
    <PageHero
      title="تواصل معنا"
      subtitle="نسعد بتواصلكم معنا والإجابة على جميع استفساراتكم"
      bg-image="/images/heroes/contact-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-16">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <!-- Contact Form (Right in RTL) -->
        <div class="bg-white rounded-2xl p-6 lg:p-8 shadow-sm border border-gray-100 order-1">
          <h2 class="font-arabic font-bold text-[24px] text-dark mb-6 text-right">أرسل لنا رسالة</h2>
          <form @submit.prevent class="space-y-5" dir="rtl">
            <div>
              <label class="block font-cairo text-[14px] text-dark mb-2">الاسم الكامل</label>
              <input type="text" placeholder="أدخل اسمك الكامل" class="input-field" />
            </div>
            <div>
              <label class="block font-cairo text-[14px] text-dark mb-2">البريد الإلكتروني</label>
              <input type="email" placeholder="أدخل بريدك الإلكتروني" class="input-field" dir="ltr" style="text-align: right;" />
            </div>
            <div>
              <label class="block font-cairo text-[14px] text-dark mb-2">رقم الهاتف</label>
              <input type="tel" placeholder="أدخل رقم هاتفك" class="input-field" dir="ltr" style="text-align: right;" />
            </div>
            <div>
              <label class="block font-cairo text-[14px] text-dark mb-2">الموضوع</label>
              <select class="input-field">
                <option value="">اختر الموضوع</option>
                <option>استفسار عام</option>
                <option>التسجيل والقبول</option>
                <option>الرسوم والمدفوعات</option>
                <option>البرامج التعليمية</option>
                <option>شكوى أو اقتراح</option>
              </select>
            </div>
            <div>
              <label class="block font-cairo text-[14px] text-dark mb-2">الرسالة</label>
              <textarea rows="5" placeholder="اكتب رسالتك هنا..." class="input-field resize-none"></textarea>
            </div>
            <button type="submit" class="w-full bg-secondary text-white font-cairo font-bold py-3 rounded-xl hover:bg-secondary-dark transition-colors text-[16px]">
              إرسال
            </button>
          </form>
        </div>

        <!-- Contact Info (Left in RTL) -->
        <div class="space-y-6 order-2">
          <div v-for="info in contactInfo" :key="info.label" class="bg-white rounded-xl p-5 shadow-sm border border-gray-100 flex items-start gap-4 justify-end text-right">
            <div class="flex-1">
              <h3 class="font-arabic font-bold text-[17px] text-dark mb-1">{{ info.label }}</h3>
              <p class="font-cairo text-[15px] text-muted" :dir="info.ltr ? 'ltr' : 'rtl'" :style="info.ltr ? 'text-align: right' : ''">{{ info.value }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-secondary/10 flex items-center justify-center shrink-0">
              <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="info.icon"></svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Map Section -->
    <section class="bg-light py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center">
        <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-8">موقعنا على الخريطة</h2>
        <div class="rounded-2xl h-[400px] overflow-hidden">
          <img src="/images/contact/map.png" alt="موقعنا على الخريطة" class="w-full h-full object-cover rounded-2xl" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import PageHero from '@/components/PageHero.vue'

const contactInfo = [
  {
    label: 'العنوان',
    value: 'خلف شركة الدقهلية للدواجن',
    ltr: false,
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>',
  },
  {
    label: 'الهاتف',
    value: '01093300193 - 0504880186',
    ltr: true,
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/>',
  },
  {
    label: 'البريد الإلكتروني',
    value: 'info@dar-alanwar.com',
    ltr: true,
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/>',
  },
  {
    label: 'ساعات العمل',
    value: 'السبت - الخميس: 8:00 صباحاً - 8:00 مساءً',
    ltr: false,
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/>',
  },
]
</script>
