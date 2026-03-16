<template>
  <div class="game-layout">
    <div class="noise-layer"/>
    <div class="scanline-layer"/>

    <!-- Desktop Sidebar -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-top">
        <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">{{ sidebarCollapsed ? '▶' : '◀' }}</button>
        <div class="brand" v-if="!sidebarCollapsed">
          <p class="brand-eyebrow">OPERATION</p>
          <h1 class="brand-title">VERDICT</h1>
        </div>
      </div>
      <div class="timer-block" :class="timerUrgency">
        <p class="timer-label">{{ sidebarCollapsed ? '⏱' : 'TIME REMAINING' }}</p>
        <p class="timer-value" v-if="!sidebarCollapsed">{{ formattedTime }}</p>
        <div class="timer-bar"><div class="timer-fill" :style="{ width: timerPct + '%' }" :class="timerUrgency"/></div>
      </div>
      <nav class="nav-links">
        <RouterLink v-for="item in navItems" :key="item.path" :to="item.path" class="nav-item" :class="{ active: $route.path === item.path }">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label" v-if="!sidebarCollapsed">{{ item.label }}</span>
          <span class="nav-badge" v-if="item.badge && !sidebarCollapsed">{{ item.badge }}</span>
        </RouterLink>
      </nav>
      <div class="conviction-block" v-if="!sidebarCollapsed">
        <p class="conv-label">CONVICTION</p>
        <div class="conv-track"><div class="conv-fill" :style="{ width: game.convictionPercent + '%' }" :class="convClass"/></div>
        <div class="conv-nums">
          <span class="conv-pct" :class="convClass">{{ game.convictionPercent }}%</span>
          <span class="conv-sub">{{ game.filesReviewed }}/{{ game.totalFiles }}</span>
        </div>
      </div>
      <div class="score-block" v-if="!sidebarCollapsed">
        <p class="score-label">SCORE</p>
        <p class="score-val">{{ game.score.toLocaleString() }}</p>
      </div>
      <div class="sidebar-footer" v-if="!sidebarCollapsed">
        <p class="inv-name">{{ auth.displayName }}</p>
        <button class="logout-btn" @click="logout">SIGN OUT</button>
      </div>
    </aside>

    <!-- Main -->
    <main class="main-area">
      <!-- Mobile top bar -->
      <div class="mobile-topbar">
        <span class="mtb-title">⚖ VERDICT</span>
        <div class="mtb-right">
          <span class="mtb-timer" :class="timerUrgency">{{ formattedTime }}</span>
          <span class="mtb-conv" :class="convClass">{{ game.convictionPercent }}%</span>
        </div>
      </div>
      <slot />
      <div class="mobile-bottom-spacer"/>
    </main>

    <!-- Mobile bottom nav -->
    <nav class="bottom-nav">
      <template v-for="item in mobileNavItems" :key="item.path">
        <button v-if="item.path === '#more'" class="bnav-item" :class="{ active: moreMenuOpen }" @click="moreMenuOpen = !moreMenuOpen">
          <span class="bnav-icon">{{ item.icon }}</span>
          <span class="bnav-label">MORE</span>
          <span class="bnav-dot" v-if="item.badge"/>
        </button>
        <RouterLink v-else :to="item.path" class="bnav-item" :class="{ active: $route.path === item.path }">
          <span class="bnav-icon">{{ item.icon }}</span>
          <span class="bnav-label">{{ item.label }}</span>
          <span class="bnav-dot" v-if="item.badge"/>
        </RouterLink>
      </template>
    </nav>

    <!-- More menu -->
    <Transition name="slide-up">
      <div class="more-overlay" v-if="moreMenuOpen" @click.self="moreMenuOpen = false">
        <div class="more-menu">
          <div class="more-handle"/>
          <p class="more-title">MORE SCREENS</p>
          <RouterLink v-for="item in extraNavItems" :key="item.path" :to="item.path" class="more-item" @click="moreMenuOpen = false">
            <span class="more-icon">{{ item.icon }}</span>
            <span class="more-label">{{ item.label }}</span>
            <span class="more-badge" v-if="item.badge">{{ item.badge }}</span>
          </RouterLink>
          <div class="more-stats">
            <div class="ms-row"><span>Investigator</span><span class="ms-gold">{{ auth.displayName }}</span></div>
            <div class="ms-row"><span>Score</span><span class="ms-gold">{{ game.score.toLocaleString() }} pts</span></div>
            <div class="ms-row"><span>Files reviewed</span><span>{{ game.filesReviewed }}/{{ game.totalFiles }}</span></div>
          </div>
          <button class="more-logout" @click="logout">SIGN OUT</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useGameStore } from '@/stores/game'

const router = useRouter()
const auth   = useAuthStore()
const game   = useGameStore()
const sidebarCollapsed = ref(false)
const moreMenuOpen     = ref(false)

const navItems = computed(() => [
  { path:'/dashboard',     icon:'📁', label:'CASE FILES',    badge:null },
  { path:'/evidence',      icon:'🔗', label:'EVIDENCE BOARD',badge:null },
  { path:'/suspect',       icon:'🎯', label:'SUSPECT FILE',  badge:null },
  { path:'/interrogation', icon:'💬', label:'INTERROGATION', badge:null },
  { path:'/timeline',      icon:'📅', label:'TIMELINE',      badge:null },
  { path:'/tips',          icon:'📨', label:'TIP INBOX',     badge: game.unreadTips > 0 ? game.unreadTips : null },
  { path:'/leaderboard',   icon:'🏆', label:'LEADERBOARD',   badge:null },
  { path:'/verdict',       icon:'⚖️', label:'VERDICT ROOM',  badge: game.verdictReached ? '!' : null },
])

const mobileNavItems = computed(() => [
  { path:'/dashboard',     icon:'📁', label:'FILES',   badge:null },
  { path:'/interrogation', icon:'💬', label:'CHAT',    badge:null },
  { path:'/evidence',      icon:'🔗', label:'BOARD',   badge:null },
  { path:'/verdict',       icon:'⚖️', label:'VERDICT', badge: game.verdictReached ? '!' : null },
  { path:'#more',          icon:'⋯',  label:'MORE',    badge: game.unreadTips > 0 ? true : null },
])

const extraNavItems = computed(() => [
  { path:'/suspect',    icon:'🎯', label:'SUSPECT PROFILE', badge:null },
  { path:'/timeline',   icon:'📅', label:'CASE TIMELINE',   badge:null },
  { path:'/tips',       icon:'📨', label:'TIP INBOX',       badge: game.unreadTips > 0 ? game.unreadTips : null },
  { path:'/leaderboard',icon:'🏆', label:'LEADERBOARD',     badge:null },
])

const formattedTime = computed(() => {
  const s = game.timeRemaining
  const h = Math.floor(s/3600), m = Math.floor((s%3600)/60), sec = s%60
  return h > 0 ? `${h}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}` : `${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`
})
const timerPct     = computed(() => (game.timeRemaining/7200)*100)
const timerUrgency = computed(() => game.timeRemaining < 600 ? 'critical' : game.timeRemaining < 1800 ? 'warning' : 'normal')
const convClass    = computed(() => game.convictionPercent >= 75 ? 'strong' : game.convictionPercent >= 40 ? 'mid' : 'weak')

function logout() { game.stopTimer(); game.syncTimer(); auth.logout(); router.push('/login') }

onMounted(() => game.startTimer())
onUnmounted(() => game.stopTimer())
</script>

<style scoped>
.game-layout { display:flex; min-height:100vh; background:#050508; }

/* Sidebar */
.sidebar { width:240px;flex-shrink:0;background:rgba(8,8,14,0.97);border-right:1px solid rgba(201,162,39,0.15);display:flex;flex-direction:column;transition:width 0.3s;position:relative;z-index:10; }
.sidebar.collapsed { width:56px; }
.sidebar-top { display:flex;align-items:center;gap:0.75rem;padding:1.25rem 1rem 1rem;border-bottom:1px solid rgba(201,162,39,0.08); }
.collapse-btn { background:transparent;border:1px solid rgba(201,162,39,0.2);color:#4a4a5a;font-size:0.6rem;width:24px;height:24px;cursor:pointer;flex-shrink:0;transition:all 0.2s; }
.collapse-btn:hover { color:#c9a227;border-color:rgba(201,162,39,0.5); }
.brand-eyebrow { font-size:0.55rem;letter-spacing:0.3em;color:#c9a227; }
.brand-title { font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:900;color:#f0e6d3;line-height:1; }
.timer-block { padding:0.85rem 1rem;border-bottom:1px solid rgba(201,162,39,0.06); }
.timer-label { font-size:0.55rem;letter-spacing:0.2em;color:#4a4a5a;margin-bottom:0.3rem; }
.timer-value { font-family:'Courier Prime',monospace;font-size:1.3rem;font-weight:700;color:#f0e6d3;margin-bottom:0.4rem; }
.timer-block.warning .timer-value { color:#c9a227; }
.timer-block.critical .timer-value { color:#c0392b; }
.timer-bar { height:2px;background:rgba(255,255,255,0.04); }
.timer-fill { height:100%;transition:width 1s linear; }
.timer-fill.normal{background:#c9a227}.timer-fill.warning{background:#e67e22}.timer-fill.critical{background:#c0392b}
.nav-links { display:flex;flex-direction:column;padding:0.5rem 0;flex:1;overflow-y:auto; }
.nav-item { display:flex;align-items:center;gap:0.65rem;padding:0.65rem 1rem;text-decoration:none;color:#4a4a5a;font-size:0.65rem;letter-spacing:0.12em;transition:all 0.2s;border-left:2px solid transparent; }
.nav-item:hover { color:#c9a227;background:rgba(201,162,39,0.04); }
.nav-item.active { color:#c9a227;border-left-color:#c9a227;background:rgba(201,162,39,0.06); }
.nav-icon { font-size:0.9rem;flex-shrink:0; }
.nav-label { flex:1;white-space:nowrap;overflow:hidden; }
.nav-badge { background:#c0392b;color:#fff;font-size:0.55rem;padding:0.1rem 0.4rem;border-radius:2px;font-weight:700; }
.conviction-block { padding:0.85rem 1rem;border-top:1px solid rgba(201,162,39,0.06); }
.conv-label { font-size:0.55rem;letter-spacing:0.2em;color:#4a4a5a;margin-bottom:0.4rem; }
.conv-track { height:3px;background:rgba(255,255,255,0.04);margin-bottom:0.4rem; }
.conv-fill { height:100%;transition:width 0.8s ease; }
.conv-fill.strong{background:#4a9a5a}.conv-fill.mid{background:#c9a227}.conv-fill.weak{background:#c0392b}
.conv-nums { display:flex;justify-content:space-between;align-items:baseline; }
.conv-pct { font-size:1.1rem;font-weight:700; }
.conv-pct.strong{color:#4a9a5a}.conv-pct.mid{color:#c9a227}.conv-pct.weak{color:#c0392b}
.conv-sub { font-size:0.6rem;color:#2a2a3a; }
.score-block { padding:0.5rem 1rem 0.85rem; }
.score-label { font-size:0.55rem;letter-spacing:0.2em;color:#2a2a3a; }
.score-val { font-size:1rem;font-weight:700;color:#c9a227;font-family:'Courier Prime',monospace; }
.sidebar-footer { padding:0.85rem 1rem;border-top:1px solid rgba(201,162,39,0.06);margin-top:auto; }
.inv-name { font-size:0.7rem;color:#4a4a5a;margin-bottom:0.5rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis; }
.logout-btn { width:100%;background:transparent;border:1px solid rgba(255,255,255,0.05);color:#2a2a3a;font-family:'Courier Prime',monospace;font-size:0.6rem;letter-spacing:0.15em;padding:0.45rem;cursor:pointer;transition:all 0.2s; }
.logout-btn:hover { border-color:rgba(192,57,43,0.4);color:#c0392b; }

/* Main */
.main-area { flex:1;overflow-y:auto;position:relative;z-index:1; }
.mobile-topbar { display:none;align-items:center;justify-content:space-between;padding:0.75rem 1rem 0.75rem calc(1rem + env(safe-area-inset-left));padding-top:calc(0.75rem + env(safe-area-inset-top));background:rgba(6,6,10,0.98);border-bottom:1px solid rgba(201,162,39,0.12);position:sticky;top:0;z-index:20; }
.mtb-title { font-family:'Playfair Display',serif;font-size:1rem;font-weight:900;color:#f0e6d3;letter-spacing:0.08em; }
.mtb-right { display:flex;align-items:center;gap:0.6rem; }
.mtb-timer { font-family:'Courier Prime',monospace;font-size:0.82rem;font-weight:700;color:#f0e6d3; }
.mtb-timer.warning{color:#c9a227}.mtb-timer.critical{color:#c0392b}
.mtb-conv { font-size:0.72rem;font-weight:700;border:1px solid;padding:0.15rem 0.45rem;border-radius:2px; }
.mtb-conv.strong{color:#4a9a5a;border-color:rgba(74,154,90,0.3)}.mtb-conv.mid{color:#c9a227;border-color:rgba(201,162,39,0.3)}.mtb-conv.weak{color:#c0392b;border-color:rgba(192,57,43,0.3)}
.mobile-bottom-spacer { height:0; }

/* Bottom nav */
.bottom-nav { display:none;position:fixed;bottom:0;left:0;right:0;z-index:50;background:rgba(6,6,10,0.98);border-top:1px solid rgba(201,162,39,0.15);padding-bottom:env(safe-area-inset-bottom); }
.bnav-item { display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;padding:0.55rem 0.25rem;text-decoration:none;color:#3a3a4a;font-size:0.5rem;letter-spacing:0.08em;transition:color 0.2s;position:relative;min-height:54px;background:transparent;border:none;cursor:pointer; }
.bnav-item.active { color:#c9a227; }
.bnav-item:active { opacity:0.6; }
.bnav-icon { font-size:1.15rem;margin-bottom:0.18rem;line-height:1; }
.bnav-label { white-space:nowrap;font-family:'Courier Prime',monospace; }
.bnav-dot { position:absolute;top:7px;right:calc(50% - 14px);width:6px;height:6px;border-radius:50%;background:#c0392b; }

/* More overlay */
.more-overlay { position:fixed;inset:0;z-index:49;background:rgba(5,5,8,0.75);display:flex;align-items:flex-end; }
.more-menu { width:100%;background:rgba(8,8,16,0.99);border-top:1px solid rgba(201,162,39,0.2);padding:0 1rem calc(1rem + env(safe-area-inset-bottom));padding-bottom:calc(60px + env(safe-area-inset-bottom) + 0.5rem); }
.more-handle { width:36px;height:3px;background:rgba(201,162,39,0.25);border-radius:2px;margin:0.75rem auto 1rem; }
.more-title { font-size:0.58rem;letter-spacing:0.25em;color:#4a4a5a;margin-bottom:0.5rem; }
.more-item { display:flex;align-items:center;gap:0.85rem;padding:0.85rem 0;text-decoration:none;color:#8a8a9a;font-size:0.82rem;border-bottom:1px solid rgba(255,255,255,0.04); }
.more-icon { font-size:1rem;width:24px;text-align:center; }
.more-label { flex:1; }
.more-badge { background:#c0392b;color:#fff;font-size:0.55rem;padding:0.1rem 0.4rem;border-radius:2px;font-weight:700; }
.more-stats { padding:0.75rem 0;margin-top:0.25rem;border-top:1px solid rgba(201,162,39,0.08); }
.ms-row { display:flex;justify-content:space-between;font-size:0.72rem;color:#4a4a5a;padding:0.3rem 0; }
.ms-gold { color:#c9a227;font-weight:700; }
.more-logout { width:100%;margin-top:0.75rem;background:transparent;border:1px solid rgba(192,57,43,0.2);color:#4a4a5a;font-family:'Courier Prime',monospace;font-size:0.65rem;letter-spacing:0.15em;padding:0.7rem;cursor:pointer;transition:all 0.2s; }
.more-logout:hover { color:#c0392b;border-color:rgba(192,57,43,0.5); }

/* Transitions */
.slide-up-enter-active,.slide-up-leave-active { transition:all 0.25s ease; }
.slide-up-enter-from,.slide-up-leave-to { opacity:0; }
.slide-up-enter-from .more-menu,.slide-up-leave-to .more-menu { transform:translateY(100%); }

/* Responsive */
@media (max-width: 768px) {
  .sidebar { display:none !important; }
  .mobile-topbar { display:flex; }
  .bottom-nav { display:flex; }
  .mobile-bottom-spacer { height:calc(54px + env(safe-area-inset-bottom)); }
  .game-layout { flex-direction:column; }
}
</style>
