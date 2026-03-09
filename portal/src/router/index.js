import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Public pages (website)
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { public: true },
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('@/views/ServicesView.vue'),
    meta: { public: true },
  },
  {
    path: '/programs',
    name: 'Programs',
    component: () => import('@/views/ProgramsView.vue'),
    meta: { public: true },
  },
  {
    path: '/programs/:id',
    name: 'ProgramDetail',
    component: () => import('@/views/ProgramDetailView.vue'),
    meta: { public: true },
  },
  {
    path: '/programs/:id/units/:unitId',
    name: 'Unit',
    component: () => import('@/views/UnitView.vue'),
    meta: { public: true },
  },
  {
    path: '/programs/:id/units/:unitId/lessons/:lessonId',
    name: 'Lesson',
    component: () => import('@/views/LessonView.vue'),
    meta: { public: true },
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: () => import('@/views/TeachersView.vue'),
    meta: { public: true },
  },
  {
    path: '/teachers/:id',
    name: 'TeacherProfile',
    component: () => import('@/views/TeacherProfileView.vue'),
    meta: { public: true },
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('@/views/BlogView.vue'),
    meta: { public: true },
  },
  {
    path: '/blog/:slug',
    name: 'Article',
    component: () => import('@/views/ArticleView.vue'),
    meta: { public: true },
  },
  {
    path: '/payments',
    name: 'PaymentsInfo',
    component: () => import('@/views/PaymentsInfoView.vue'),
    meta: { public: true },
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('@/views/BooksView.vue'),
    meta: { public: true },
  },
  {
    path: '/books/:id',
    name: 'BookDetail',
    component: () => import('@/views/BookDetailView.vue'),
    meta: { public: true },
  },
  {
    path: '/games',
    name: 'Games',
    component: () => import('@/views/GamesView.vue'),
    meta: { public: true },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue'),
    meta: { public: true },
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/ContactView.vue'),
    meta: { public: true },
  },
  {
    path: '/faq',
    name: 'Faq',
    component: () => import('@/views/FaqView.vue'),
    meta: { public: true },
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('@/views/PrivacyView.vue'),
    meta: { public: true },
  },

  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/CartView.vue'),
    meta: { auth: true },
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('@/views/CheckoutView.vue'),
    meta: { auth: true },
  },

  // Guest pages (login/register)
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/ForgotPasswordView.vue'),
    meta: { guest: true },
  },

  // Authenticated pages (parent portal)
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { auth: true },
  },
  {
    path: '/children',
    name: 'Children',
    component: () => import('@/views/ChildrenView.vue'),
    meta: { auth: true },
  },
  {
    path: '/children/:id',
    name: 'ChildProfile',
    component: () => import('@/views/ChildProfileView.vue'),
    meta: { auth: true },
  },
  {
    path: '/my-payments',
    name: 'Payments',
    component: () => import('@/views/PaymentsView.vue'),
    meta: { auth: true },
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('@/views/CoursesView.vue'),
    meta: { auth: true },
  },
  {
    path: '/kids-area',
    name: 'KidsArea',
    component: () => import('@/views/KidsAreaView.vue'),
    meta: { auth: true },
  },
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('@/views/MessagesView.vue'),
    meta: { auth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.auth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
