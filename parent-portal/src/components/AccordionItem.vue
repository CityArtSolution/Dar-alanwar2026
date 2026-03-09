<template>
  <div class="border border-gray-200 rounded-xl overflow-hidden mb-3">
    <button
      @click="isOpen = !isOpen"
      class="w-full flex items-center justify-between px-6 py-4 text-right bg-white hover:bg-gray-50 transition-colors"
    >
      <span class="font-cairo font-bold text-[16px] lg:text-[18px] text-dark">{{ title }}</span>
      <svg
        :class="['w-5 h-5 text-secondary shrink-0 transition-transform duration-300', isOpen && 'rotate-180']"
        fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="max-h-0 opacity-0"
      enter-to-class="max-h-96 opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="max-h-96 opacity-100"
      leave-to-class="max-h-0 opacity-0"
    >
      <div v-show="isOpen" class="overflow-hidden">
        <div class="px-6 pb-5 pt-1 text-right font-cairo text-[14px] lg:text-[16px] text-muted leading-relaxed">
          <slot />
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  title: { type: String, required: true },
})

const isOpen = ref(false)
</script>
