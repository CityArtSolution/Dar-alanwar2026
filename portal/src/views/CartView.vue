<template>
  <div>
    <PageHero title="السلة" />

    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-10">
      <!-- Back Button -->
      <div class="mb-6">
        <router-link to="/dashboard" class="inline-flex items-center gap-2 px-6 py-2.5 border border-primary text-primary rounded-lg font-cairo font-bold text-[14px] hover:bg-primary/5 transition-colors">
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
          <div class="w-10 h-10 rounded-full bg-gray-300 text-white flex items-center justify-center font-cairo font-bold text-[16px]">2</div>
          <div class="w-[120px] lg:w-[200px] h-1 bg-gray-300"></div>
        </div>
        <div class="w-10 h-10 rounded-full bg-gray-300 text-white flex items-center justify-center font-cairo font-bold text-[16px]">3</div>
      </div>

      <!-- Cart Table -->
      <div v-if="cartItems.length" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">مسح</th>
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">الصور</th>
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">الاسم</th>
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">السعر</th>
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">الكمية</th>
                <th class="px-4 py-4 text-right font-cairo font-bold text-[14px] text-dark">الاجمالي</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in cartItems" :key="item.id" class="border-b border-gray-50">
                <td class="px-4 py-4">
                  <button @click="removeItem(item.id)" class="text-muted hover:text-red-500 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  </button>
                </td>
                <td class="px-4 py-4">
                  <img :src="item.image" :alt="item.name" class="w-[60px] h-[60px] rounded-lg object-cover" />
                </td>
                <td class="px-4 py-4 font-cairo font-bold text-[14px] text-dark">{{ item.name }}</td>
                <td class="px-4 py-4 font-cairo text-[14px] text-muted">{{ item.price }} ر.س</td>
                <td class="px-4 py-4">
                  <div class="flex items-center gap-2">
                    <button @click="updateQty(item.id, -1)" class="w-7 h-7 rounded border border-gray-300 flex items-center justify-center text-dark hover:bg-gray-100">-</button>
                    <span class="w-10 text-center font-cairo text-[14px] text-dark">{{ item.qty }}</span>
                    <button @click="updateQty(item.id, 1)" class="w-7 h-7 rounded border border-gray-300 flex items-center justify-center text-dark hover:bg-gray-100">+</button>
                  </div>
                </td>
                <td class="px-4 py-4 font-cairo font-bold text-[14px] text-dark">{{ item.price * item.qty }} ر.س</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty Cart -->
      <div v-else class="text-center py-16">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
        <p class="font-cairo text-[18px] text-muted">السلة فارغة</p>
        <router-link to="/books" class="inline-block mt-4 bg-primary text-white font-cairo font-bold py-3 px-8 rounded-[30px] hover:bg-primary-dark transition-colors">تصفح المنتجات</router-link>
      </div>

      <!-- Summary Row -->
      <div v-if="cartItems.length" class="flex flex-col lg:flex-row gap-8 items-start">
        <!-- Coupon -->
        <div class="flex-1">
          <h3 class="font-arabic font-bold text-[18px] text-dark mb-3">اضف كوبون الخصم</h3>
          <div class="flex gap-2">
            <input v-model="couponCode" type="text" placeholder="كود الخصم"
                   class="flex-1 border border-gray-300 rounded-lg px-4 py-3 font-cairo text-[14px] focus:outline-none focus:border-secondary" />
            <button @click="applyCoupon" class="bg-primary text-white font-cairo font-bold px-6 py-3 rounded-lg hover:bg-primary-dark transition-colors">تفعيل</button>
          </div>
        </div>

        <!-- Cart Total -->
        <div class="lg:w-[350px]">
          <h3 class="font-arabic font-bold text-[18px] text-dark mb-3">اجمالي السلة</h3>
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div class="flex items-center justify-between font-cairo text-[15px] mb-3">
              <span class="text-muted">المبلغ الكلي</span>
              <span class="text-dark font-bold">{{ cartTotal }} ر.س</span>
            </div>
            <div v-if="discount" class="flex items-center justify-between font-cairo text-[15px] mb-3 text-green-600">
              <span>خصم</span>
              <span class="font-bold">-{{ discount }} ر.س</span>
            </div>
            <hr class="my-3" />
            <div class="flex items-center justify-between font-cairo text-[18px] font-bold">
              <span class="text-dark">الاجمالي</span>
              <span class="text-primary">{{ cartTotal - discount }} ر.س</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div v-if="cartItems.length" class="flex flex-col sm:flex-row gap-4 mt-8">
        <router-link to="/checkout" class="flex-1 bg-primary text-white font-cairo font-bold py-4 rounded-[30px] text-center text-[18px] hover:bg-primary-dark transition-colors">
          اتمام الشراء
        </router-link>
        <router-link to="/" class="flex-1 border-2 border-primary text-primary font-cairo font-bold py-4 rounded-[30px] text-center text-[18px] hover:bg-primary/5 transition-colors">
          العودة للقائمة الرئيسية
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import PageHero from '@/components/PageHero.vue'

const couponCode = ref('')
const discount = ref(0)

const cartItems = ref([
  { id: 1, name: 'اقرأ بطلاقه', price: 40, qty: 1, image: '/images/books/book-1.png' },
  { id: 2, name: 'اقرأ بطلاقه', price: 40, qty: 1, image: '/images/books/book-2.png' },
  { id: 3, name: 'اقرأ بطلاقه', price: 40, qty: 1, image: '/images/books/book-3.png' },
  { id: 4, name: 'اقرأ بطلاقه', price: 40, qty: 1, image: '/images/books/book-4.png' },
])

const cartTotal = computed(() => cartItems.value.reduce((sum, item) => sum + item.price * item.qty, 0))

function removeItem(id) {
  cartItems.value = cartItems.value.filter(item => item.id !== id)
}

function updateQty(id, delta) {
  const item = cartItems.value.find(i => i.id === id)
  if (item) {
    item.qty = Math.max(1, item.qty + delta)
  }
}

function applyCoupon() {
  if (couponCode.value.trim()) {
    discount.value = 20
  }
}
</script>
