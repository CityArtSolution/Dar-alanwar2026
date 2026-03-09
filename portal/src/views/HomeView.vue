<template>
  <div>
    <!-- ===== HERO (969px height) ===== -->
    <section class="relative min-h-[500px] lg:min-h-[969px] flex items-center justify-center overflow-hidden">
      <!-- Background with Figma gradient overlays -->
      <div class="absolute inset-0 bg-cover bg-center"
           style="background-image: linear-gradient(0deg, rgba(0,0,0,0.2), rgba(0,0,0,0.2)), linear-gradient(180deg, rgba(255,149,0,0) 0%, rgba(255,149,0,0.35) 100%), linear-gradient(0deg, rgba(0,190,174,0.1), rgba(0,190,174,0.1)), url('/images/hero-bg.jpg');
                  background-color: #4a7c6f;"></div>

      <div class="relative z-10 flex flex-col items-center text-center px-4">
        <!-- Logo 348x348 -->
        <div class="w-[180px] h-[180px] lg:w-[348px] lg:h-[348px] mb-3">
          <img src="/logo.png" alt="دار الأنوار" class="w-full h-full object-contain" />
        </div>
        <!-- Subtitle: Cairo 40px bold -->
        <p class="text-white text-[20px] sm:text-[28px] lg:text-[40px] font-bold font-cairo" style="line-height: 100px;">
          تعليم إسلامي متميز في بيئة تربوية محفزة
        </p>
        <!-- Main heading: Tajawal 128px bold -->
        <h1 class="text-[36px] sm:text-[64px] lg:text-[128px] font-bold text-white font-arabic" style="line-height: 1.17;">
          دار الأنوار لتعليم القرآن الكريم<br/>واللغه العربية
        </h1>
        <!-- Two buttons: 430.5px each, 65px tall, rounded 30px -->
        <div class="flex flex-col sm:flex-row items-center gap-[11px] mt-6">
          <div class="relative w-full sm:w-[300px] lg:w-[430px]">
            <router-link to="/login" class="block w-full bg-primary hover:bg-primary-dark text-white text-center py-4 lg:py-[18px] rounded-[30px] font-bold font-cairo text-[16px] lg:text-[20px] transition-colors" style="height: 65px; line-height: 29px; display: flex; align-items: center; justify-content: center;">سجل الآن</router-link>
            <div class="absolute left-[4px] top-1/2 -translate-y-1/2 w-[44px] h-[44px] lg:w-[58px] lg:h-[58px] bg-white rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 lg:w-7 lg:h-7 text-primary" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            </div>
          </div>
          <router-link to="/about" class="w-full sm:w-[300px] lg:w-[430px] text-center border border-white text-white rounded-[30px] font-bold font-cairo text-[16px] lg:text-[20px] hover:bg-white/10 transition-colors flex items-center justify-center" style="height: 65px;">تعرف علينا</router-link>
        </div>
      </div>

      <!-- Scroll-up teal circle button (bottom left in LTR, bottom right in RTL) -->
      <button class="absolute bottom-6 left-6 lg:bottom-10 lg:left-10 w-[60px] h-[60px] lg:w-[120px] lg:h-[120px] bg-secondary rounded-full flex items-center justify-center text-white shadow-[0_2px_4px_rgba(0,0,0,0.25)] z-10">
        <svg class="w-6 h-6 lg:w-10 lg:h-10" fill="currentColor" viewBox="0 0 24 24"><path d="M7 14l5-5 5 5z"/></svg>
      </button>
    </section>

    <!-- ===== ABOUT STRIP (Orange, 236px) ===== -->
    <section class="bg-primary">
      <div class="flex flex-col lg:flex-row items-center justify-between px-6 lg:px-[86px] py-8 lg:py-[30px] gap-6 lg:gap-10 max-w-[1920px] mx-auto" style="min-height: 236px;">
        <div class="shrink-0 order-2 lg:order-1">
          <router-link to="/about" class="flex items-center gap-[10px] bg-white rounded-[44px] px-[41px] py-3 hover:bg-gray-50 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 20 20"><path d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" fill="#FF9500" transform="rotate(180 10 10)"/></svg>
            <span class="font-cairo font-bold text-[16px] lg:text-[18px] text-primary" style="line-height: 59px;">اعرف المزيد</span>
          </router-link>
        </div>
        <div class="flex-1 text-right order-1 lg:order-2">
          <h2 class="text-[32px] lg:text-[55px] font-bold text-white font-arabic" style="line-height: 70px;">عن دار الأنوار</h2>
          <p class="text-[16px] lg:text-[20px] font-semibold font-cairo" style="color: #EBEBEB; line-height: 32px;">
            دار الأنوار هي مؤسسة تعليمية متخصصة في تعليم القرآن الكريم واللغة العربية للأطفال والكبار، تأسست عام 2006 بهدف تقديم تعليم إسلامي متميز في بيئة تربوية محفزة
          </p>
        </div>
      </div>
    </section>

    <!-- ===== SERVICES (خدماتنا التعليمية) ===== -->
    <section class="bg-white py-12 lg:py-[80px]">
      <div class="max-w-[1289px] mx-auto px-4 lg:px-0">
        <div class="text-center">
          <h2 class="text-[32px] lg:text-[55px] font-bold text-primary font-arabic" style="line-height: 70px;">خدماتنا التعليمية</h2>
        </div>
        <!-- 3 service cards: 401-405px wide, 255px tall -->
        <div class="flex flex-col sm:flex-row items-start justify-center gap-6 lg:gap-[42px] mt-8 lg:mt-[40px]">
          <div v-for="service in services" :key="service.title"
               class="w-full sm:w-[401px] bg-white rounded-[20px] flex flex-col items-center justify-center py-6 lg:py-8"
               style="filter: drop-shadow(0px 4px 26.5px rgba(0,0,0,0.1)); min-height: 255px;">
            <div class="mb-4 lg:mb-8">
              <div class="w-[80px] h-[80px] lg:w-[112px] lg:h-[112px] flex items-center justify-center">
                <svg class="w-[60px] h-[60px] lg:w-[80px] lg:h-[80px] text-secondary" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" :d="service.icon"/></svg>
              </div>
            </div>
            <h3 class="font-cairo font-bold text-[18px] lg:text-[24px] text-center" style="color: #4D5756;">{{ service.title }}</h3>
          </div>
        </div>
        <!-- Teal button -->
        <div class="mt-8 lg:mt-[48px]" style="filter: drop-shadow(0px 2px 2px rgba(0,0,0,0.35));">
          <button class="w-full h-[50px] lg:h-[64px] bg-secondary text-white rounded-[44px] font-cairo font-bold text-[16px] lg:text-[18px] flex items-center justify-center gap-[10px] hover:bg-secondary-dark transition-colors">
            <svg class="w-5 h-5 rotate-180" fill="currentColor" viewBox="0 0 20 20"><path d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"/></svg>
            عرض جميع الخدمات
          </button>
        </div>
      </div>
    </section>

    <!-- ===== PROGRAMS (برامجنا التعليمية) ===== -->
    <section>
      <div class="text-center py-8 lg:py-[35px] px-4 lg:px-[86px]">
        <h2 class="text-[32px] lg:text-[55px] font-bold text-dark font-arabic" style="line-height: 70px;">برامجنا التعليمية</h2>
        <p class="text-dark text-[16px] lg:text-[20px] font-semibold font-cairo mt-4 lg:mt-[24px] max-w-[696px] mx-auto" style="line-height: 32px;">
          في دار الأنوار نحرص على تقديم برامج تعليمية وترفيهية متنوعه لبناء طفل يمتلك قدر عالي من المهارات التي تساعده في بناء شخصيته
        </p>
      </div>
      <!-- Top row: 3 program blocks -->
      <div class="flex">
        <button v-for="tab in programTabs" :key="tab.id" @click="activeTab = tab.id"
                class="flex-1 flex items-center justify-center h-[120px] sm:h-[180px] lg:h-[268px] transition-colors"
                :class="activeTab === tab.id ? 'bg-primary' : 'bg-light'"
                style="border: 2px solid #FFFFFF;">
          <span class="font-cairo text-[18px] sm:text-[24px] lg:text-[32px] font-normal"
                :style="{ color: activeTab === tab.id ? '#F8F9F9' : '#353C3B' }">{{ tab.label }}</span>
        </button>
      </div>
      <!-- Bottom row: 3 program blocks -->
      <div class="flex">
        <div v-for="program in bottomPrograms" :key="program.label"
             class="flex-1 flex items-center justify-center h-[120px] sm:h-[180px] lg:h-[268px] bg-light"
             style="border: 2px solid #FFFFFF;">
          <span class="font-cairo text-[18px] sm:text-[24px] lg:text-[32px] font-normal text-dark">{{ program.label }}</span>
        </div>
      </div>
    </section>

    <!-- ===== STATS (حقائق عنا — 607px) ===== -->
    <section>
      <div class="text-center py-8 lg:py-[40px]">
        <h2 class="text-[32px] lg:text-[55px] font-bold text-dark font-arabic" style="line-height: 70px;">حقائق عنا</h2>
      </div>
      <div class="flex flex-col lg:flex-row">
        <!-- Left: Photo -->
        <div class="lg:flex-1 h-[300px] lg:h-[607px] bg-cover bg-center"
             style="background-image: url('/images/stats-bg.jpg'); background-color: #7ba89e;"></div>
        <!-- Right: 2x2 stats grid -->
        <div class="lg:flex-1">
          <div class="grid grid-cols-2 h-full">
            <div v-for="stat in stats" :key="stat.label" class="flex flex-col items-center justify-center gap-[14px] py-8 lg:py-0" style="border: 3px solid #F8F9F9;">
              <!-- Outer ring 97px, inner circle 78px -->
              <div class="relative w-[70px] h-[70px] lg:w-[97px] lg:h-[97px] flex items-center justify-center">
                <div class="w-[56px] h-[56px] lg:w-[78px] lg:h-[78px] bg-dark rounded-full flex items-center justify-center">
                  <svg class="w-[28px] h-[28px] lg:w-[38px] lg:h-[38px] text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="stat.icon"/></svg>
                </div>
                <div class="absolute inset-0 rounded-full" style="border: 3px solid #353C3B;"></div>
              </div>
              <!-- Epilogue 39px number -->
              <p class="text-[24px] lg:text-[39px] font-bold text-dark" style="font-family: 'Epilogue', sans-serif;">{{ stat.value }}</p>
              <!-- Cairo 24px label -->
              <p class="text-dark text-[16px] lg:text-[24px] font-bold font-cairo" style="line-height: 44px;">{{ stat.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== TESTIMONIALS (ماذا قالو عنا) ===== -->
    <section class="py-12 lg:py-[80px]" style="background-color: #F8F9F9;">
      <div class="max-w-[1733px] mx-auto px-4">
        <div class="text-center mb-8 lg:mb-[48px]">
          <h2 class="text-[32px] lg:text-[55px] font-bold text-dark font-arabic" style="line-height: 70px;">ماذا قالو عنا</h2>
          <p class="text-dark text-[16px] lg:text-[20px] font-semibold font-cairo mt-4 lg:mt-[40px] max-w-[589px] mx-auto" style="line-height: 32px;">
            يسعدنا ان نشارككم بعض من اراء اولياء امور طلابنا في دار الأنوار والاساليب العلمية والتربوية المتسخدمه في بناء الطفل
          </p>
        </div>
        <div class="flex items-center gap-4 lg:gap-[48px]">
          <!-- Left arrow -->
          <button class="shrink-0 w-[36px] h-[36px] lg:w-[46px] lg:h-[46px] bg-primary rounded-full flex items-center justify-center text-white hidden md:flex" style="transform: rotate(180deg);">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/></svg>
          </button>
          <!-- 3 testimonial cards: 2px dashed #FF9500, border-radius 5px, min-height 328px -->
          <div class="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-[48px]">
            <div v-for="review in testimonials" :key="review.name"
                 class="flex flex-col justify-center px-4 lg:px-[18px] py-6 lg:py-[39px]"
                 style="border: 2px dashed #FF9500; border-radius: 5px; min-height: 328px;">
              <div class="text-primary text-[14px] mb-[15px]">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
              <p class="text-dark text-[14px] lg:text-[16px] font-bold font-cairo text-right mb-[9px]" style="line-height: 32px;">{{ review.text }}</p>
              <div class="flex items-center gap-[14px] self-end">
                <div class="text-right">
                  <p class="font-cairo font-bold text-[15px] lg:text-[17px] text-dark" style="line-height: 19px;">{{ review.name }}</p>
                  <p class="font-cairo text-[13px] text-dark" style="line-height: 32px;">{{ review.role }}</p>
                </div>
                <img src="/images/testimonial-photo.jpg" alt="" class="w-[50px] h-[50px] rounded-full object-cover shrink-0" />
              </div>
            </div>
          </div>
          <!-- Right arrow -->
          <button class="shrink-0 w-[36px] h-[36px] lg:w-[46px] lg:h-[46px] bg-primary rounded-full flex items-center justify-center text-white hidden md:flex">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/></svg>
          </button>
        </div>
      </div>
    </section>

    <!-- ===== NEWS (اخر الأخبار والفاعليات) ===== -->
    <section class="bg-white py-12 lg:py-[80px]">
      <div class="max-w-[1770px] mx-auto px-4">
        <h2 class="text-[32px] lg:text-[55px] font-bold text-dark text-center font-arabic mb-8 lg:mb-[64px]" style="line-height: 70px;">اخر الأخبار والفاعليات</h2>
        <!-- 4 news cards: 2px dashed #00BEAE, border-radius 5px 44px 5px 5px -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-[48px] mb-8 lg:mb-[48px]">
          <div v-for="article in news" :key="article.id"
               class="bg-white flex flex-col items-center p-5 lg:p-[32px_42px] gap-4 lg:gap-[37px]"
               style="border: 2px dashed #00BEAE; border-radius: 5px 44px 5px 5px;">
            <!-- Image: 322x187, border 1px solid #FF9500, rounded 10px -->
            <div class="w-full h-[150px] lg:h-[187px] bg-cover bg-center rounded-[10px] shrink-0"
                 :style="{ border: '1px solid #FF9500', backgroundImage: `url(${article.image})`, backgroundColor: '#d4e5e2' }"></div>
            <div class="w-full text-right flex-1">
              <h3 class="font-cairo font-bold text-[18px] lg:text-[24px] text-primary text-right" style="line-height: 28px;">{{ article.title }}</h3>
              <p class="font-cairo font-medium text-[14px] lg:text-[16px] text-dark text-right mt-[10px]" style="line-height: 28px;">{{ article.desc }}</p>
            </div>
            <div class="w-full relative shrink-0">
              <button class="w-full h-[50px] lg:h-[65px] bg-primary text-white rounded-[30px] font-cairo font-bold text-[16px] lg:text-[20px] hover:bg-primary-dark transition-colors">إنتقل الى المقالة</button>
              <div class="absolute left-[4px] top-1/2 -translate-y-1/2 w-[44px] h-[44px] lg:w-[58px] lg:h-[58px] bg-white rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 lg:w-7 lg:h-7 text-primary" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </div>
            </div>
          </div>
        </div>
        <button class="w-full h-[50px] lg:h-[64px] bg-secondary text-white rounded-[44px] font-cairo font-bold text-[16px] lg:text-[18px] flex items-center justify-center gap-[10px] hover:bg-secondary-dark transition-colors">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" style="transform: matrix(0,1,1,0,0,0);"><path d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"/></svg>
          اعرف المزيد
        </button>
      </div>
    </section>

    <!-- ===== CTA (Teal rotated rectangles) ===== -->
    <section class="relative py-16 lg:py-24 overflow-hidden">
      <!-- Rotated teal rectangles background -->
      <div class="absolute inset-0">
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:-75px;top:0;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:432px;top:0;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:939px;top:0;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:1446px;top:0;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:-70px;top:200px;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:437px;top:200px;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:944px;top:200px;transform:rotate(-6.28deg);"></div>
        <div class="absolute w-[508px] h-[358px] bg-secondary rounded-lg" style="left:1451px;top:200px;transform:rotate(-6.28deg);"></div>
      </div>
      <!-- White star decorations -->
      <div class="absolute w-[65px] h-[74px] bg-white/50 rounded" style="right:100px;top:30px;"></div>
      <div class="absolute w-[65px] h-[74px] bg-white/50 rounded" style="right:200px;bottom:40px;"></div>
      <div class="absolute w-[65px] h-[74px] bg-white/50 rounded" style="left:510px;bottom:60px;"></div>
      <div class="absolute w-[65px] h-[74px] bg-white/50 rounded" style="left:297px;top:50px;"></div>
      <div class="absolute w-[45px] h-[48px] bg-white/50 rounded" style="left:94px;top:120px;"></div>
      <!-- Content -->
      <div class="relative z-10 text-center px-4 max-w-[880px] mx-auto">
        <h2 class="text-[28px] lg:text-[55px] font-bold text-white font-arabic" style="line-height: 100px;">اشترك الآن في منصة دار الانوار</h2>
        <p class="text-white text-[18px] lg:text-[32px] font-medium font-cairo" style="line-height: 52px;">خصومات حصرية لباقات الاشتراك</p>
        <div class="relative inline-block mt-6 lg:mt-10">
          <router-link to="/login" class="block w-[240px] lg:w-[300px] h-[50px] lg:h-[61px] bg-primary text-white rounded-[30px] font-cairo font-bold text-[16px] lg:text-[20px] leading-[59px] text-center hover:bg-primary-dark transition-colors">اشترك الان</router-link>
          <div class="absolute left-[3px] top-1/2 -translate-y-1/2 w-[44px] h-[44px] lg:w-[55px] lg:h-[55px] bg-white rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 lg:w-7 lg:h-7" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#FFBB00"/></svg>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== GALLERY (معرض صور دار الأنوار) ===== -->
    <section class="relative">
      <div class="text-center py-8">
        <h2 class="text-[32px] lg:text-[55px] font-bold text-dark font-arabic" style="line-height: 70px;">معرض صور دار الأنوار</h2>
      </div>
      <!-- 3 top images -->
      <div class="grid grid-cols-3">
        <div v-for="(img, i) in galleryImages.slice(0,3)" :key="'t'+i"
             class="aspect-[643/552] bg-cover bg-center"
             :style="{ backgroundImage: `url(${img})`, backgroundColor: '#8cb5ad' }"></div>
      </div>
      <!-- 2 bottom images -->
      <div class="grid grid-cols-2">
        <div v-for="(img, i) in galleryImages.slice(3,5)" :key="'b'+i"
             class="aspect-[643/552] bg-cover bg-center"
             :style="{ backgroundImage: `url(${img})`, backgroundColor: '#8cb5ad' }"></div>
      </div>
      <!-- Dark gradient overlay -->
      <div class="absolute inset-0 pointer-events-none" style="background:linear-gradient(180.04deg,rgba(53,60,59,0.25) 0.03%,#353C3B 122.19%);"></div>
      <!-- "عرض المزيد" button -->
      <div class="absolute bottom-6 left-6 lg:bottom-10 lg:left-[37px] z-10">
        <button class="flex items-center justify-center gap-[10px] bg-secondary text-white rounded-[75px] px-6 lg:px-[45px] py-4 lg:py-[41px] font-cairo font-bold text-[16px] lg:text-[20px]" style="box-shadow:0px 2px 4px rgba(0,0,0,0.25);">
          عرض المزيد من الصور
          <svg class="w-8 h-8 lg:w-[60px] lg:h-[60px]" fill="currentColor" viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const services = [
  { title: 'القرآن الكريم وعلومه', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
  { title: 'قسم الحضانة', icon: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z' },
  { title: 'التعليم عن بعد', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
]

const programTabs = [
  { id: 'kids', label: 'برامج الأطفال' },
  { id: 'youth', label: 'برامج الناشئة' },
  { id: 'adults', label: 'برامج اليافعين' },
]
const activeTab = ref('kids')

const bottomPrograms = [
  { label: 'برامج الكبار' },
  { label: 'القران الكريم' },
  { label: 'اللغة العربية' },
]

const stats = [
  { value: '+19', label: 'عام من الخبرة', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
  { value: '+25', label: 'برنامج تعليمي', icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
  { value: '+50', label: 'معلم ومعلمة', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z' },
  { value: '+1500', label: 'طالب وطالبة', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' },
]

const testimonials = [
  { name: 'أم أحمد', role: 'ولي امر طالب', text: 'معلمين محترفين ويجيدون التعامل مع الاطفال وطريقة التعليم الممتعه بالالعاب هي طريقه رائعه ساعدت طفلي كثيرا في فهم الحروف والارقام شكرا لكم' },
  { name: 'محمد العلي', role: 'ولي امر طالب', text: 'معلمين محترفين ويجيدون التعامل مع الاطفال وطريقة التعليم الممتعه بالالعاب هي طريقه رائعه ساعدت طفلي كثيرا في فهم الحروف والارقام شكرا لكم' },
  { name: 'سارة محمود', role: 'ولي امر طالب', text: 'معلمين محترفين ويجيدون التعامل مع الاطفال وطريقة التعليم الممتعه بالالعاب هي طريقه رائعه ساعدت طفلي كثيرا في فهم الحروف والارقام شكرا لكم' },
]

const news = [
  { id: 1, title: 'فتح باب التقدم لدورات جديدة', desc: 'يسعد دار الأنوار ان تعلن عن فتح باب التقدم لدورات جديدة تشمل الرسم والفنون لبناء مواهب اطفالكم وتنمية مهاراتهم', image: '/images/news-card-img.jpg' },
  { id: 2, title: 'فتح باب التقدم لدورات جديدة', desc: 'يسعد دار الأنوار ان تعلن عن فتح باب التقدم لدورات جديدة تشمل الرسم والفنون لبناء مواهب اطفالكم وتنمية مهاراتهم', image: '/images/news-card-img.jpg' },
  { id: 3, title: 'فتح باب التقدم لدورات جديدة', desc: 'يسعد دار الأنوار ان تعلن عن فتح باب التقدم لدورات جديدة تشمل الرسم والفنون لبناء مواهب اطفالكم وتنمية مهاراتهم', image: '/images/news-card-img.jpg' },
  { id: 4, title: 'فتح باب التقدم لدورات جديدة', desc: 'يسعد دار الأنوار ان تعلن عن فتح باب التقدم لدورات جديدة تشمل الرسم والفنون لبناء مواهب اطفالكم وتنمية مهاراتهم', image: '/images/news-card-img.jpg' },
]

const galleryImages = [
  '/images/gallery-1.jpg',
  '/images/gallery-2.jpg',
  '/images/gallery-3.jpg',
  '/images/gallery-4.jpg',
  '/images/gallery-5.jpg',
]
</script>
