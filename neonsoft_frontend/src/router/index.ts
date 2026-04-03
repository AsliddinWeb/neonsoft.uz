import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    // ─── Public ───────────────────────────────────────────────────────────
    {
      path: '/',
      component: () => import('@/layouts/PublicLayout.vue'),
      children: [
        { path: '', name: 'home', component: () => import('@/views/public/HomePage.vue') },
        { path: 'services', name: 'services', component: () => import('@/views/public/ServicesPage.vue') },
        { path: 'projects', name: 'projects', component: () => import('@/views/public/ProjectsPage.vue') },
        { path: 'team', name: 'team', component: () => import('@/views/public/TeamPage.vue') },
        { path: 'blog', name: 'blog', component: () => import('@/views/public/BlogPage.vue') },
        { path: 'blog/:slug', name: 'blog-detail', component: () => import('@/views/public/BlogDetailPage.vue') },
        { path: 'services/request', name: 'service-request', component: () => import('@/views/public/ServiceRequestPage.vue') },
        { path: 'contact', name: 'contact', component: () => import('@/views/public/ContactPage.vue') },
        { path: ':pathMatch(.*)*', name: 'not-found', component: () => import('@/views/public/NotFoundPage.vue') },
      ],
    },

    // ─── Admin login (no layout) ──────────────────────────────────────────
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('@/views/admin/LoginPage.vue'),
    },

    // ─── Admin (AdminLayout + auth guard) ────────────────────────────────
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/admin/dashboard' },
        { path: 'dashboard', name: 'dashboard', component: () => import('@/views/admin/DashboardPage.vue') },
        { path: 'services', name: 'admin-services', component: () => import('@/views/admin/ServicesPage.vue') },
        { path: 'projects', name: 'admin-projects', component: () => import('@/views/admin/ProjectsPage.vue') },
        { path: 'team', name: 'admin-team', component: () => import('@/views/admin/TeamPage.vue') },
        { path: 'blog', name: 'admin-blog', component: () => import('@/views/admin/BlogPage.vue') },
        { path: 'contacts', name: 'admin-contacts', component: () => import('@/views/admin/ContactsPage.vue') },
        { path: 'about', name: 'admin-about', component: () => import('@/views/admin/AboutPage.vue') },
        { path: 'partners', name: 'admin-partners', component: () => import('@/views/admin/PartnersPage.vue') },
        { path: 'settings', name: 'admin-settings', component: () => import('@/views/admin/SettingsPage.vue') },
        { path: 'users', name: 'admin-users', component: () => import('@/views/admin/UsersPage.vue') },
      ],
    },
  ],
})

// ─── Navigation guard ─────────────────────────────────────────────────────────
router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) return '/admin/login'
    if (!auth.user) {
      await auth.fetchMe()
      if (!auth.user) return '/admin/login'
    }
  }
})

export default router
