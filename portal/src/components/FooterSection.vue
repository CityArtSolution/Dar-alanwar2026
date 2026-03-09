<template>
  <footer class="bg-secondary text-white">
    <!-- Main footer (458px height in Figma) -->
    <div class="max-w-[1139px] mx-auto px-4 sm:px-6 py-[100px]">
      <div class="flex flex-col md:flex-row justify-center items-start gap-8 lg:gap-[48px]">
        <!-- Logo & Social (278x258) -->
        <div class="shrink-0">
          <img src="/logo.png" alt="دار الأنوار" class="w-[200px] lg:w-[278px] h-auto object-contain mb-3" />
          <div class="flex items-center justify-center gap-5 mt-2">
            <a href="#" class="text-white hover:text-white/80"><svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/></svg></a>
            <a href="#" class="text-white hover:text-white/80"><svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
            <a href="#" class="text-white hover:text-white/80"><svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          </div>
        </div>

        <!-- Quick Links: Cairo 26px title, 20px links -->
        <div class="text-right">
          <h4 class="font-cairo font-bold text-[20px] lg:text-[26px] mb-6 lg:mb-[32px]" style="line-height: 49px;">روابط سريعة</h4>
          <ul class="space-y-3 lg:space-y-[32px]">
            <li><router-link to="/privacy" class="text-white font-cairo text-[16px] lg:text-[20px] hover:text-white/80" style="line-height: 37px;">سياسة الخصوصية</router-link></li>
            <li><router-link to="/faq" class="text-white font-cairo text-[16px] lg:text-[20px] hover:text-white/80" style="line-height: 37px;">أسئلة شائعة</router-link></li>
            <li><router-link to="/contact" class="text-white font-cairo text-[16px] lg:text-[20px] hover:text-white/80" style="line-height: 37px;">الدعم الفني</router-link></li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div class="text-right">
          <h4 class="font-cairo font-bold text-[20px] lg:text-[26px] mb-6 lg:mb-[32px]" style="line-height: 49px;">معلومات الاتصال</h4>
          <ul class="space-y-4 lg:space-y-[32px]">
            <li class="flex items-center gap-3 justify-end">
              <span class="text-white font-cairo text-[16px] lg:text-[20px]" dir="ltr" style="line-height: 37px;">01093300193</span>
              <svg class="w-6 h-6 shrink-0 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
            </li>
            <li class="flex items-center gap-3 justify-end">
              <span class="text-white font-cairo text-[16px] lg:text-[20px]" dir="ltr" style="line-height: 37px;">0504880186</span>
              <svg class="w-6 h-6 shrink-0 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2 22l4.832-1.438A9.955 9.955 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2z"/></svg>
            </li>
            <li class="flex items-center gap-3 justify-end">
              <span class="text-white font-cairo text-[16px] lg:text-[20px]" style="line-height: 37px;">خلف شركة الدقهلية للدواجن</span>
              <svg class="w-6 h-6 shrink-0 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
            </li>
          </ul>
        </div>

        <!-- Newsletter -->
        <div class="text-right">
          <h4 class="font-cairo font-bold text-[20px] lg:text-[26px] mb-4" style="line-height: 49px;">النشرة الاخبارية</h4>
          <p class="text-white font-cairo text-[16px] lg:text-[20px] mb-6" style="line-height: 37px;">اشترك الآن ليصلك احدث المقالات</p>
          <!-- White button with orange border (Figma: bg white, border 1px #FF9500, rounded 25px) -->
          <button class="bg-white text-primary font-bold text-[16px] lg:text-[18px] px-[72px] py-[15px] rounded-[25px] hover:bg-gray-50 transition-colors" style="font-family: 'Almarai', sans-serif; border: 1px solid #FF9500; box-shadow: 0px 1px 4px rgba(0,0,0,0.25);">
            اشترك الآن
          </button>
        </div>
      </div>
    </div>

    <!-- Copyright bar (border-top white, Sora 17px) -->
    <div style="border-top: 1px solid #FFFFFF;">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 py-4 text-center">
        <span class="font-sora text-[15px] lg:text-[17px] text-white" style="line-height: 32px;">Copyright &copy; {{ new Date().getFullYear() }} </span>
        <span class="font-sora text-[15px] lg:text-[17px] font-bold" style="color: #2FC7A1; line-height: 32px;">edunity</span>
        <span class="font-sora text-[15px] lg:text-[17px] text-white" style="line-height: 32px;"> || All Rights Reserved</span>
      </div>
    </div>
  </footer>
</template>
