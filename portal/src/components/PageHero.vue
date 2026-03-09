<template>
  <section
    :class="[
      'relative overflow-hidden flex items-center justify-center text-white text-center',
      bgClass || 'bg-secondary'
    ]"
    :style="{ minHeight: height || '350px' }"
  >
    <!-- Background image overlay -->
    <div v-if="bgImage" class="absolute inset-0">
      <img :src="bgImage" alt="" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-black/40"></div>
    </div>

    <!-- Decorative circles -->
    <div class="absolute top-6 left-10 w-20 h-20 rounded-full border-2 border-white/20 hidden lg:block"></div>
    <div class="absolute bottom-10 right-16 w-14 h-14 rounded-full border-2 border-white/15 hidden lg:block"></div>
    <div class="absolute top-1/2 left-1/4 w-8 h-8 rounded-full bg-white/10 hidden lg:block"></div>

    <div class="relative z-10 px-4 py-16 max-w-3xl mx-auto">
      <h1 class="font-arabic font-bold text-[36px] sm:text-[48px] lg:text-[64px] leading-tight mb-4">
        {{ title }}
      </h1>
      <p v-if="subtitle" class="font-cairo text-[16px] sm:text-[18px] lg:text-[20px] text-white/90 leading-relaxed max-w-2xl mx-auto">
        {{ subtitle }}
      </p>
      <slot />
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  bgClass: { type: String, default: '' },
  bgImage: { type: String, default: '' },
  height: { type: String, default: '' },
})
</script>
