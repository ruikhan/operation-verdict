import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/register',     component: () => import('@/views/RegisterView.vue'),     meta: { guest: true } },
  { path: '/login',        component: () => import('@/views/LoginView.vue'),        meta: { guest: true } },
  { path: '/terms',        component: () => import('@/views/TermsView.vue'),        meta: { auth: true } },
  { path: '/briefing',     component: () => import('@/views/CinematicView.vue'),    meta: { auth: true } },
  { path: '/dashboard',    component: () => import('@/views/DashboardView.vue'),    meta: { auth: true, game: true } },
  { path: '/evidence',     component: () => import('@/views/EvidenceBoardView.vue'),meta: { auth: true, game: true } },
  { path: '/suspect',      component: () => import('@/views/SuspectProfileView.vue'),meta:{ auth: true, game: true } },
  { path: '/timeline',     component: () => import('@/views/TimelineView.vue'),     meta: { auth: true, game: true } },
  { path: '/interrogation',component: () => import('@/views/InterrogationView.vue'),meta: { auth: true, game: true } },
  { path: '/leaderboard',  component: () => import('@/views/LeaderboardView.vue'),  meta: { auth: true, game: true } },
  { path: '/tips',         component: () => import('@/views/TipInboxView.vue'),     meta: { auth: true, game: true } },
  { path: '/verdict',      component: () => import('@/views/CourtRoomView.vue'),    meta: { auth: true, game: true } },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.guest && auth.isLoggedIn) {
    if (!auth.termsAccepted) return '/terms'
    if (!auth.cinematicViewed) return '/briefing'
    return '/dashboard'
  }
  if ((to.meta.auth || to.meta.game) && !auth.isLoggedIn) return '/login'
  if (auth.isLoggedIn) {
    if (!auth.termsAccepted && to.path !== '/terms') return '/terms'
    if (auth.termsAccepted && !auth.cinematicViewed && to.path !== '/briefing') return '/briefing'
  }
})

export default router
