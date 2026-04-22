import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView from '@/views/HomeView.vue'
import NotFoundView from '@/views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }

    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true },
      alias: '/login',
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/babies',
      name: 'babies',
      component: () => import('../views/BabiesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/baby/:babyId',
      name: 'baby',
      component: () => import('../views/BabyDetailsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/babies/new',
      name: 'baby-create',
      component: () => import('../views/BabyFormView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/babies/:babyId',
      name: 'baby-details',
      component: () => import('../views/BabyDetailsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/babies/:babyId/edit',
      name: 'baby-edit',
      component: () => import('../views/BabyFormView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: () => import('../views/AppointmentView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' })
    return
  }

  if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
