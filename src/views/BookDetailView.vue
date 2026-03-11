<template>
  <div>
    <PageHero title="المكتبة" subtitle="اكتشف مجموعتنا المتنوعة من الكتب التعليمية" bg-image="/images/heroes/books-hero.png" />

    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <!-- Book Detail -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 lg:p-10 mb-12">
        <div class="flex flex-col md:flex-row gap-8 items-start">
          <!-- Cover -->
          <div class="w-[220px] h-[300px] shrink-0 rounded-xl overflow-hidden mx-auto md:mx-0 shadow-md">
            <img :src="book.cover" :alt="book.title" class="w-full h-full object-cover" />
          </div>
          <!-- Info -->
          <div class="flex-1 text-right">
            <h2 class="font-arabic font-bold text-[28px] lg:text-[36px] text-dark mb-3">{{ book.title }}</h2>
            <p class="font-cairo text-[16px] text-secondary mb-1">{{ book.author }}</p>
            <span class="inline-block bg-secondary/10 text-secondary font-cairo text-sm font-bold px-4 py-1 rounded-full mb-5">{{ book.category }}</span>
            <div class="font-cairo text-[16px] text-muted leading-[1.9] space-y-3">
              <p>{{ book.description }}</p>
            </div>
            <button class="mt-6 bg-secondary text-white font-cairo font-bold px-8 py-3 rounded-xl hover:bg-secondary-dark transition-colors">
              اقرأ الكتاب
            </button>
          </div>
        </div>
      </div>

      <!-- Related Books -->
      <div>
        <h3 class="font-arabic font-bold text-[24px] text-dark mb-6 text-right">كتب ذات صلة</h3>
        <div class="flex gap-4 overflow-x-auto pb-4" dir="rtl">
          <router-link
            v-for="related in relatedBooks"
            :key="related.id"
            :to="`/books/${related.id}`"
            class="shrink-0 w-[180px] bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
          >
            <div class="h-[200px] overflow-hidden bg-gray-50">
              <img src="/images/books/book-cover-main.png" :alt="related.title" class="w-full h-full object-cover" />
            </div>
            <div class="p-3 text-right">
              <h4 class="font-cairo font-bold text-[14px] text-dark mb-1">{{ related.title }}</h4>
              <p class="font-cairo text-[12px] text-muted">{{ related.author }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PageHero from '@/components/PageHero.vue'

const route = useRoute()

const booksData = [
  { id: '1', title: 'القاعدة النورانية', author: 'الشيخ نور محمد حقاني', category: 'القرآن الكريم', cover: '/images/books/book-cover-main.png', description: 'كتاب تعليمي أساسي لتعلم قراءة القرآن الكريم بأحكام التجويد الصحيحة. يعد من أشهر الكتب المستخدمة في تعليم الأطفال أساسيات القراءة القرآنية من خلال منهجية تدريجية تبدأ من الحروف الهجائية وصولاً إلى قراءة الآيات القرآنية بطلاقة.' },
  { id: '2', title: 'تعلم العربية المبسطة', author: 'أ. سامية عبدالرحمن', category: 'اللغة العربية', cover: '/images/books/book-mascot.png', description: 'منهج متكامل لتعليم اللغة العربية للأطفال يشمل القراءة والكتابة والإملاء. يتميز الكتاب بأسلوبه المبسط والممتع مع تمارين تفاعلية وصور توضيحية تساعد الطفل على استيعاب قواعد اللغة العربية بسهولة.' },
]

const book = computed(() => {
  return booksData.find(b => b.id === route.params.id) || booksData[0]
})

const relatedBooks = [
  { id: '1', title: 'القاعدة النورانية', author: 'الشيخ نور محمد حقاني' },
  { id: '2', title: 'تعلم العربية المبسطة', author: 'أ. سامية عبدالرحمن' },
  { id: '3', title: 'أحكام التجويد المصورة', author: 'د. أيمن سويد' },
  { id: '4', title: 'قصص الأنبياء للأطفال', author: 'أ. ياسر عبدالتواب' },
  { id: '5', title: 'الأذكار اليومية للصغار', author: 'دار الأنوار' },
]
</script>
