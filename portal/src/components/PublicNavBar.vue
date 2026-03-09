<template>
  <!-- Top Social Bar — ORANGE 50px -->
  <div class="bg-primary text-white text-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-[50px]">
      <!-- Language Selector (right side in RTL) -->
      <div class="flex items-center gap-2">
        <img src="/images/lang-flag.jpg" alt="" class="w-[17px] h-[17px] rounded-full object-cover" />
        <span style="font-family: 'El Messiri', sans-serif;" class="text-[15px] text-white">العربيه</span>
        <svg class="w-[9px] h-[7px]" fill="currentColor" viewBox="0 0 9 7"><path d="M4.5 7L0 0h9L4.5 7z"/></svg>
      </div>
      <!-- Social Icons (left side in RTL) -->
      <div class="flex items-center gap-3">
        <a href="#" class="hover:text-white/80 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/></svg></a>
        <a href="#" class="hover:text-white/80 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
        <a href="#" class="hover:text-white/80 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
        <a href="#" class="hover:text-white/80 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
      </div>
    </div>
  </div>

  <!-- Main Navbar — WHITE 77px with orange right-side accent -->
  <nav class="bg-white sticky top-0 z-40 relative">
    <!-- Orange accent line on right -->
    <div class="absolute top-0 bottom-0 right-[15px] w-1 bg-primary"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-[77px]">
        <!-- Desktop Nav Links -->
        <div class="hidden xl:flex items-center gap-7 flex-1">
          <router-link v-for="link in navLinks" :key="link.to" :to="link.to"
                       class="text-[16px] font-semibold text-black hover:text-secondary transition-colors font-cairo whitespace-nowrap"
                       active-class="!text-secondary">
            {{ link.label }}
          </router-link>
        </div>

        <!-- Right Actions -->
        <div class="flex items-center gap-4">
          <!-- Search circle (52x52) -->
          <button class="w-[52px] h-[52px] rounded-full border border-gray-300 bg-white flex items-center justify-center hover:border-secondary transition-colors hidden sm:flex">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
          <!-- Notification circle (52x52) -->
          <button class="w-[52px] h-[52px] rounded-full border border-gray-300 bg-white flex items-center justify-center hover:border-secondary transition-colors hidden sm:flex">
            <svg class="w-[22px] h-[22px] text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 22c1.1 0 2-.9 2-2h-4a2 2 0 002 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
          </button>
          <!-- "سجل الآن" teal button (151x40) — Figma: bg=#00BEAE, Cairo 16px bold -->
          <router-link to="/login" class="bg-secondary text-white rounded-[20px] px-5 py-2.5 text-[16px] font-bold font-cairo hover:bg-secondary-dark transition-colors hidden sm:block">
            سجل الآن
          </router-link>
          <!-- Login button (128x40) — Figma: border teal, Cairo 12px semibold -->
          <router-link to="/login" class="border border-secondary text-secondary rounded-[60px] px-5 py-2 text-[12px] font-semibold font-cairo hidden sm:flex items-center gap-2 hover:bg-secondary/5 transition-colors">
            <svg class="w-[14px] h-[14px]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            تسجيل الدخول
          </router-link>

          <!-- Mobile Hamburger -->
          <button @click="mobileOpen = !mobileOpen" class="xl:hidden p-2 rounded-lg hover:bg-gray-100 text-gray-600">
            <svg v-if="!mobileOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Logo (far right in RTL, 126x86 in Figma) -->
        <router-link to="/" class="shrink-0 flex items-center gap-2 mr-4">
          <img src="/logo.png" alt="دار الأنوار" class="w-[86px] h-[60px] lg:w-[126px] lg:h-[86px] object-contain" />
        </router-link>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div v-if="mobileOpen" class="xl:hidden border-t border-gray-100 bg-white pb-4 max-h-[70vh] overflow-y-auto">
        <div class="space-y-1 px-4 pt-3">
          <router-link v-for="link in navLinks" :key="link.to" :to="link.to"
                       class="block px-4 py-2.5 text-sm text-dark hover:bg-secondary/5 hover:text-secondary rounded-lg transition-colors font-cairo font-semibold"
                       active-class="!text-secondary !bg-secondary/5"
                       @click="mobileOpen = false">
            {{ link.label }}
          </router-link>
          <div class="border-t border-gray-100 pt-3 mt-2 space-y-2">
            <router-link to="/login" class="block px-4 py-2.5 text-sm text-secondary font-semibold font-cairo rounded-lg" @click="mobileOpen = false">
              تسجيل الدخول
            </router-link>
          </div>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const mobileOpen = ref(false)

const navLinks = [
  { to: '/', label: 'الصفحة الرئيسيه' },
  { to: '/services', label: 'خدماتنا' },
  { to: '/programs', label: 'برامجنا' },
  { to: '/teachers', label: 'المعلمين' },
  { to: '/blog', label: 'المدونه' },
  { to: '/payments', label: 'المدفوعات' },
  { to: '/books', label: 'المكتبة' },
  { to: '/games', label: 'الالعاب' },
  { to: '/about', label: 'من نحن' },
  { to: '/contact', label: 'تواصل معنا' },
]
</script>
