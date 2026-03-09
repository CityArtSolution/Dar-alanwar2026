<template>
  <div>
    <PageHero :title="article.title" :subtitle="article.date" bg-image="/images/heroes/blog-hero.png" />

    <div class="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      <!-- Article Body -->
      <article class="text-right mb-16">
        <div class="font-cairo text-[16px] lg:text-[18px] text-dark leading-[2] space-y-6">
          <p>{{ article.body[0] }}</p>

          <div class="rounded-xl h-[300px] overflow-hidden my-8">
            <img src="/images/blog/article-quran.png" alt="" class="w-full h-full object-cover rounded-xl" />
          </div>

          <h2 class="font-arabic font-bold text-[24px] lg:text-[28px] text-dark">{{ article.subheading }}</h2>

          <p>{{ article.body[1] }}</p>
          <p>{{ article.body[2] }}</p>

          <blockquote class="border-r-4 border-secondary pr-6 py-3 bg-secondary/5 rounded-lg">
            <p class="font-arabic text-[18px] text-secondary italic">{{ article.quote }}</p>
          </blockquote>

          <p>{{ article.body[3] }}</p>
        </div>
      </article>

      <!-- Related Articles -->
      <div>
        <h3 class="font-arabic font-bold text-[24px] text-dark mb-6 text-right">مقالات ذات صلة</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <router-link
            v-for="related in relatedArticles"
            :key="related.slug"
            :to="`/blog/${related.slug}`"
            class="bg-white rounded-xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="h-[140px] overflow-hidden bg-gray-100">
              <img :src="related.image" :alt="related.title" class="w-full h-full object-cover" />
            </div>
            <div class="p-4 text-right">
              <span class="font-cairo text-[12px] text-muted">{{ related.date }}</span>
              <h4 class="font-arabic font-bold text-[15px] text-dark mt-1">{{ related.title }}</h4>
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

const articlesData = {
  'importance-of-quran-education': {
    title: 'أهمية تعليم القرآن الكريم في سن مبكرة',
    date: '15 فبراير 2026',
    subheading: 'فوائد حفظ القرآن للأطفال',
    quote: '« خيركم من تعلم القرآن وعلمه »',
    body: [
      'يعد تعليم القرآن الكريم في سن مبكرة من أفضل ما يقدمه الوالدان لأبنائهم. فالقرآن الكريم ليس مجرد كتاب يُحفظ، بل هو منهج حياة يبني شخصية الطفل ويرسخ القيم الإسلامية في نفسه منذ نعومة أظفاره. وقد أثبتت الدراسات الحديثة أن حفظ القرآن يقوي الذاكرة وينمي القدرات العقلية للأطفال.',
      'من أبرز فوائد تعليم القرآن الكريم للأطفال تنمية المهارات اللغوية وتقوية الذاكرة وبناء الشخصية المتوازنة. كما يساعد على تعزيز التركيز والانضباط الذاتي لدى الطفل، مما ينعكس إيجاباً على تحصيله الدراسي في جميع المواد.',
      'في دار الأنوار نحرص على توفير بيئة تعليمية محفزة تجعل حفظ القرآن تجربة ممتعة ومشوقة. نستخدم أساليب تعليمية متنوعة تشمل التلقين والتكرار والربط البصري والسمعي، مع مراعاة الفروق الفردية بين الطلاب.',
      'ندعو جميع أولياء الأمور لتسجيل أبنائهم في برامج تحفيظ القرآن الكريم في دار الأنوار، حيث يجد أبناؤكم البيئة المثالية للتعلم والنمو في أجواء إيمانية تربوية متميزة.',
    ],
  },
}

const defaultArticle = {
  title: 'مقال تعليمي من دار الأنوار',
  date: '2026',
  subheading: 'التعليم في دار الأنوار',
  quote: '« العلم نور والجهل ظلام »',
  body: [
    'في دار الأنوار نؤمن بأهمية التعليم الشامل الذي يجمع بين العلم الشرعي والمعرفة الحياتية. نسعى دائماً لتقديم أفضل البرامج التعليمية التي تناسب جميع الفئات العمرية.',
    'تتميز برامجنا بالتنوع والشمولية، حيث نقدم دورات في تحفيظ القرآن الكريم وتعليم اللغة العربية وتنمية المهارات الحياتية المختلفة.',
    'يشرف على برامجنا نخبة من المعلمين والمعلمات المتخصصين الذين يتمتعون بخبرة واسعة في مجال التعليم والتربية.',
    'سجل أبناءك الآن في دار الأنوار واستفد من عروضنا المميزة للفصل الدراسي الجديد.',
  ],
}

const article = computed(() => {
  return articlesData[route.params.slug] || defaultArticle
})

const relatedArticles = [
  { slug: 'arabic-language-tips', title: 'نصائح لتعلم اللغة العربية بطريقة ممتعة', date: '10 فبراير 2026', image: '/images/services/arabic-calligraphy.png' },
  { slug: 'child-development-stages', title: 'مراحل نمو الطفل وأهمية التعليم المبكر', date: '5 فبراير 2026', image: '/images/services/arabic-laptop.png' },
  { slug: 'creative-thinking-skills', title: 'تنمية مهارات التفكير الإبداعي عند الأطفال', date: '28 يناير 2026', image: '/images/services/tajweed-family.png' },
]
</script>
