<template>
  <div>
    <PageHero title="الدفـــع" />

    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-10">
      <!-- Back Button -->
      <div class="mb-6">
        <router-link to="/cart" class="inline-flex items-center gap-2 px-6 py-2.5 border border-primary text-primary rounded-lg font-cairo font-bold text-[14px] hover:bg-primary/5 transition-colors">
          العودة لوحة التحكم
        </router-link>
      </div>

      <!-- Step Progress -->
      <div class="flex items-center justify-center gap-0 mb-10">
        <div class="flex items-center gap-0">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-cairo font-bold text-[16px]">1</div>
          <div class="w-[120px] lg:w-[200px] h-1 bg-primary"></div>
        </div>
        <div class="flex items-center gap-0">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-cairo font-bold text-[16px]">2</div>
          <div class="w-[120px] lg:w-[200px] h-1 bg-gray-300"></div>
        </div>
        <div class="w-10 h-10 rounded-full bg-gray-300 text-white flex items-center justify-center font-cairo font-bold text-[16px]">3</div>
      </div>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Payment Form (Right in RTL) -->
        <div class="flex-1 order-2 lg:order-1">
          <!-- Order Summary -->
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
            <h2 class="font-arabic font-bold text-[22px] text-primary mb-6">تفاصيل الطلب</h2>
            <div class="space-y-3">
              <div class="flex items-center justify-between font-cairo text-[15px]">
                <span class="text-dark font-bold">المنتج</span>
                <span class="text-dark font-bold">التكلفة</span>
              </div>
              <hr />
              <div v-for="item in orderItems" :key="item.name" class="flex items-center justify-between font-cairo text-[14px]">
                <span class="text-dark">{{ item.name }}</span>
                <span class="text-muted">{{ item.price }} ريال</span>
              </div>
              <hr />
              <div class="flex items-center justify-between font-cairo text-[15px]">
                <span class="text-dark font-bold">مجموع</span>
                <span class="text-dark font-bold">{{ subtotal }} ريال</span>
              </div>
              <div class="flex items-center justify-between font-cairo text-[15px]">
                <span class="text-dark font-bold">خصم</span>
                <span class="text-muted">0 ريال</span>
              </div>
              <hr />
              <div class="flex items-center justify-between font-cairo text-[18px] font-bold">
                <span class="text-dark">التكلفة النهائية</span>
                <span class="text-primary">{{ subtotal }} ريال</span>
              </div>
            </div>

            <button @click="submitPayment" :disabled="processing"
                    class="w-full mt-6 bg-primary text-white font-cairo font-bold py-4 rounded-[30px] text-[18px] hover:bg-primary-dark transition-colors flex items-center justify-center gap-3 disabled:opacity-70">
              <span v-if="!processing">الدفع</span>
              <span v-else>جاري المعالجة...</span>
              <svg v-if="!processing" class="w-5 h-5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </div>

        <!-- Payment Method (Left in RTL) -->
        <div class="flex-1 order-1 lg:order-2">
          <!-- Payment Methods Selection -->
          <div class="space-y-4 mb-8">
            <label v-for="method in paymentMethods" :key="method.id"
                   class="flex items-center gap-4 p-4 rounded-xl border-2 cursor-pointer transition-colors"
                   :class="selectedMethod === method.id ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-gray-300'">
              <input type="radio" name="payment" :value="method.id" v-model="selectedMethod" class="hidden" />
              <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0"
                   :class="selectedMethod === method.id ? 'border-primary' : 'border-gray-300'">
                <div v-if="selectedMethod === method.id" class="w-3 h-3 rounded-full bg-primary"></div>
              </div>
              <span class="font-cairo font-bold text-[15px] text-dark flex-1">{{ method.name }}</span>
              <img :src="method.icon" :alt="method.name" class="h-6 object-contain" />
            </label>
          </div>

          <!-- Card Form (shown for mada/credit/express) -->
          <div v-if="selectedMethod !== 'bank'" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 class="font-arabic font-bold text-[18px] text-dark mb-5">الدفع</h3>
            <div class="space-y-4">
              <div>
                <label class="font-cairo text-[14px] text-dark font-bold mb-1 block">رقم البطاقة</label>
                <input v-model="cardForm.number" type="text" placeholder="1234 5678 9101 1121"
                       class="w-full border border-gray-300 rounded-lg px-4 py-3 font-cairo text-[14px] focus:outline-none focus:border-primary text-left" dir="ltr" />
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="font-cairo text-[14px] text-dark font-bold mb-1 block">CVV</label>
                  <input v-model="cardForm.cvv" type="text" placeholder="123" maxlength="4"
                         class="w-full border border-gray-300 rounded-lg px-4 py-3 font-cairo text-[14px] focus:outline-none focus:border-primary text-left" dir="ltr" />
                </div>
                <div>
                  <label class="font-cairo text-[14px] text-dark font-bold mb-1 block">تاريخ الانتهاء</label>
                  <input v-model="cardForm.expiry" type="text" placeholder="MM/YY"
                         class="w-full border border-gray-300 rounded-lg px-4 py-3 font-cairo text-[14px] focus:outline-none focus:border-primary text-left" dir="ltr" />
                </div>
              </div>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" v-model="saveCard" class="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary" />
                <span class="font-cairo text-[13px] text-muted">حفظ في الحساب</span>
              </label>
              <button class="w-full bg-primary text-white font-cairo font-bold py-3 rounded-lg hover:bg-primary-dark transition-colors">
                حفظ البطاقة
              </button>
              <p class="font-cairo text-[12px] text-muted text-center leading-[20px]">
                سيتم استخدام بياناتك الشخصية لمعالجة طلبك ودعم تجربتك عبر هذا الموقع وفقاً لسياسة الخصوصية الخاصة بنا
              </p>
            </div>
          </div>

          <!-- Bank Transfer Info -->
          <div v-else class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 class="font-arabic font-bold text-[18px] text-dark mb-4">تحويل بنكي</h3>
            <p class="font-cairo text-[14px] text-muted leading-[28px] mb-4">
              قم بالتحويل إلى الحساب البنكي التالي وأرسل إيصال التحويل عبر البريد الإلكتروني
            </p>
            <div class="space-y-3 bg-light rounded-lg p-4">
              <div class="flex justify-between font-cairo text-[14px]">
                <span class="text-muted">اسم البنك</span>
                <span class="text-dark font-bold">بنك الراجحي</span>
              </div>
              <div class="flex justify-between font-cairo text-[14px]">
                <span class="text-muted">رقم الحساب</span>
                <span class="text-dark font-bold" dir="ltr">SA1234567890123456</span>
              </div>
              <div class="flex justify-between font-cairo text-[14px]">
                <span class="text-muted">اسم المستفيد</span>
                <span class="text-dark font-bold">دار الأنوار</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageHero from '@/components/PageHero.vue'

const router = useRouter()
const processing = ref(false)
const saveCard = ref(false)
const selectedMethod = ref('mada')

const cardForm = ref({
  number: '',
  cvv: '',
  expiry: '',
})

const paymentMethods = [
  { id: 'mada', name: 'بطاقة مدى البنكية', icon: '/images/payment/mada.png' },
  { id: 'credit', name: 'بطاقة إئتمانية', icon: '/images/payment/visa-master.png' },
  { id: 'express', name: 'بطاقة إكسبريس', icon: '/images/payment/express.png' },
  { id: 'bank', name: 'تحويل بنكي', icon: '/images/payment/bank.png' },
]

const orderItems = ref([
  { name: 'كتاب اقرأبطلاقه', price: 40 },
  { name: 'دورة النحاء', price: 200 },
  { name: 'دورة اللغة العربية', price: 300 },
])

const subtotal = computed(() => orderItems.value.reduce((sum, item) => sum + item.price, 0))

function submitPayment() {
  processing.value = true
  setTimeout(() => {
    processing.value = false
    alert('تم الدفع بنجاح!')
    router.push('/dashboard')
  }, 2000)
}
</script>
