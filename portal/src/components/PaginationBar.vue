<template>
  <nav v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-10 mb-6" dir="ltr">
    <!-- Previous -->
    <button
      @click="goTo(modelValue - 1)"
      :disabled="modelValue <= 1"
      class="w-10 h-10 rounded-full flex items-center justify-center border border-gray-300 text-gray-500 hover:bg-secondary hover:text-white hover:border-secondary transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
    </button>

    <!-- Page numbers -->
    <button
      v-for="page in visiblePages"
      :key="page"
      @click="goTo(page)"
      :class="[
        'w-10 h-10 rounded-full flex items-center justify-center font-cairo font-bold text-sm transition-colors',
        page === modelValue
          ? 'bg-secondary text-white'
          : 'border border-gray-300 text-gray-600 hover:bg-secondary/10'
      ]"
    >
      {{ page }}
    </button>

    <!-- Next -->
    <button
      @click="goTo(modelValue + 1)"
      :disabled="modelValue >= totalPages"
      class="w-10 h-10 rounded-full flex items-center justify-center border border-gray-300 text-gray-500 hover:bg-secondary hover:text-white hover:border-secondary transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 1 },
  totalPages: { type: Number, required: true },
})

const emit = defineEmits(['update:modelValue'])

const visiblePages = computed(() => {
  const pages = []
  const total = props.totalPages
  const current = props.modelValue
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 4)
  start = Math.max(1, end - 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function goTo(page) {
  if (page >= 1 && page <= props.totalPages) {
    emit('update:modelValue', page)
  }
}
</script>
