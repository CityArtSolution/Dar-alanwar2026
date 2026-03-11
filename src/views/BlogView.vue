<template>
  <div>
    <PageHero
      title="مدونة دار الأنوار"
      subtitle="آخر الأخبار والمقالات التعليمية والتربوية"
      bg-image="/images/heroes/blog-hero.png"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="article in paginatedArticles"
          :key="article.slug"
          :to="`/blog/${article.slug}`"
          class="bg-white rounded-xl overflow-hidden border-2 border-dashed border-secondary/30 hover:border-secondary transition-colors group"
        >
          <div class="h-[200px] overflow-hidden bg-gray-100">
            <img :src="article.image" :alt="article.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform" />
          </div>
          <div class="p-5 text-right">
            <span class="font-cairo text-[13px] text-muted">{{ article.date }}</span>
            <h3 class="font-arabic font-bold text-[18px] text-dark mt-2 mb-2 group-hover:text-secondary transition-colors">{{ article.title }}</h3>
            <p class="font-cairo text-[14px] text-muted line-clamp-2 mb-4">{{ article.excerpt }}</p>
            <span class="font-cairo text-secondary text-[14px] font-bold">اقرأ المزيد ←</span>
          </div>
        </router-link>
      </div>

      <PaginationBar v-model="currentPage" :total-pages="totalPages" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import PageHero from '@/components/PageHero.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const currentPage = ref(1)
const perPage = 6

const articles = [
  { slug: 'importance-of-quran-education', title: 'أهمية تعليم القرآن الكريم في سن مبكرة', date: '15 فبراير 2026', excerpt: 'يعد تعليم القرآن الكريم في سن مبكرة من أفضل ما يقدمه الوالدان لأبنائهم، حيث يساهم في بناء شخصية متوازنة ومتزنة.', image: '/images/services/quran-teaching.png' },
  { slug: 'arabic-language-tips', title: 'نصائح لتعلم اللغة العربية بطريقة ممتعة', date: '10 فبراير 2026', excerpt: 'تعلم اللغة العربية يمكن أن يكون ممتعاً ومشوقاً إذا تم استخدام الأساليب الصحيحة والأنشطة التفاعلية المناسبة.', image: '/images/services/arabic-calligraphy.png' },
  { slug: 'child-development-stages', title: 'مراحل نمو الطفل وأهمية التعليم المبكر', date: '5 فبراير 2026', excerpt: 'فهم مراحل نمو الطفل يساعد الوالدين والمعلمين على تقديم الدعم المناسب في كل مرحلة عمرية.', image: '/images/services/arabic-laptop.png' },
  { slug: 'creative-thinking-skills', title: 'تنمية مهارات التفكير الإبداعي عند الأطفال', date: '28 يناير 2026', excerpt: 'التفكير الإبداعي مهارة يمكن تنميتها وتطويرها من خلال أنشطة وتمارين مصممة خصيصاً للأطفال.', image: '/images/services/tajweed-family.png' },
  { slug: 'parenting-in-digital-age', title: 'التربية في العصر الرقمي: تحديات وحلول', date: '20 يناير 2026', excerpt: 'يواجه الآباء تحديات جديدة في ظل الثورة الرقمية، ونقدم لكم حلولاً عملية للتعامل مع هذه التحديات.', image: '/images/services/kids-classroom.png' },
  { slug: 'benefits-of-reading', title: 'فوائد القراءة للأطفال وكيفية تشجيعهم عليها', date: '15 يناير 2026', excerpt: 'القراءة تفتح آفاقاً واسعة أمام الأطفال وتنمي خيالهم ومفرداتهم اللغوية بشكل كبير.', image: '/images/services/quran-group.png' },
  { slug: 'summer-programs-guide', title: 'دليلك الشامل لبرامج الصيف في دار الأنوار', date: '10 يناير 2026', excerpt: 'تعرف على برامجنا الصيفية المتنوعة التي تجمع بين التعليم والترفيه في أجواء ممتعة.', image: '/images/services/quran-boy.png' },
  { slug: 'success-stories', title: 'قصص نجاح من طلاب دار الأنوار', date: '5 يناير 2026', excerpt: 'نحتفل بإنجازات طلابنا المتميزين الذين حققوا نجاحات كبيرة في مختلف المجالات.', image: '/images/services/cta-kids.png' },
]

const totalPages = computed(() => Math.ceil(articles.length / perPage))

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return articles.slice(start, start + perPage)
})
</script>
