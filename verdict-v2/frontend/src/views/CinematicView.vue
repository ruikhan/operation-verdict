<template>
  <div class="page" @click="advance">
    <div class="noise" />
    <div class="scanline" />

    <!-- Progress bar -->
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPct + '%' }" />
    </div>

    <!-- Scene content -->
    <transition name="scene" mode="out-in">
      <div class="scene" :key="currentIndex">

        <!-- INTRO TITLE -->
        <template v-if="current.type === 'intro'">
          <p class="eyebrow">OPERATION VERDICT</p>
          <h1 class="main-title">CASE FILE<br><span class="gold">DECLASSIFIED</span></h1>
          <p class="tap-hint">CLICK TO BEGIN BRIEFING</p>
        </template>

        <!-- CHAPTER HEADING -->
        <template v-else-if="current.type === 'chapter'">
          <p class="chapter-num">{{ current.num }}</p>
          <h2 class="chapter-title">{{ current.title }}</h2>
          <p class="chapter-years">{{ current.years }}</p>
        </template>

        <!-- NARRATION TEXT -->
        <template v-else-if="current.type === 'narration'">
          <div class="narration-wrap">
            <div class="narration-bar" :class="{ red: current.red }" />
            <p class="narration" :class="{ red: current.red }">{{ current.text }}</p>
          </div>
        </template>

        <!-- NETWORK MAP -->
        <template v-else-if="current.type === 'network'">
          <p class="eyebrow" style="margin-bottom:1.5rem">KNOWN ASSOCIATES — NETWORK MAP</p>
          <div class="network-grid">
            <div class="network-center">
              <div class="suspect-dot" />
              <p class="suspect-name">JIPRI<br>EIPSTEIN</p>
            </div>
            <div
              v-for="(assoc, i) in network"
              :key="i"
              class="assoc-card"
              :class="assoc.risk"
              :style="{ animationDelay: `${i * 0.12}s` }"
            >
              <span class="assoc-risk">{{ assoc.risk.toUpperCase() }}</span>
              <p class="assoc-name">{{ assoc.name }}</p>
              <p class="assoc-role">{{ assoc.role }}</p>
            </div>
          </div>
        </template>

        <!-- FINALE — MISSION BRIEFING -->
        <template v-else-if="current.type === 'finale'">
          <div class="finale-wrap">
            <div class="red-stamp">CLASSIFIED</div>
            <h2 class="finale-title">YOUR MISSION</h2>
            <p class="finale-body">
              You have been granted access to <strong>{{ totalFiles }} classified victim case files</strong>.
              Review each file. Build the conviction. Leave no evidence unexamined.
            </p>
            <p class="finale-body" style="margin-top:1rem">
              The goal: <span class="gold">100% conviction certainty</span>.<br>
              Jipri Eipstein must be prosecuted for his crimes.
            </p>
            <button class="btn-enter" @click.stop="enterGame">
              ENTER INVESTIGATION ROOM →
            </button>
          </div>
        </template>

      </div>
    </transition>

    <!-- Nav hint -->
    <div class="nav-hint" v-if="current.type !== 'finale'">
      <span>{{ currentIndex + 1 }} / {{ scenes.length }}</span>
      <span v-if="currentIndex < scenes.length - 1">CLICK TO CONTINUE →</span>
    </div>

    <!-- Skip -->
    <button class="skip-btn" @click.stop="skipAll" v-if="currentIndex < scenes.length - 1">
      SKIP BRIEFING
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const network = [
  { name: 'Lady Ghilaine Maxwell',    role: 'Primary Recruiter',  risk: 'critical' },
  { name: 'Prince Aldric of Wessex',  role: 'Royal Associate',    risk: 'high' },
  { name: 'Lord Basil Mandelborough', role: 'Political Advisor',  risk: 'high' },
  { name: 'Senator Howard Carver',    role: 'U.S. Legislator',    risk: 'high' },
  { name: 'Viktor Rashenko',          role: 'Financier',          risk: 'medium' },
  { name: 'Dr. Raymond Pell',         role: 'Academic Donor',     risk: 'low' },
]

const totalFiles = 8

const scenes = [
  { type: 'intro' },
  { type: 'chapter', num: 'CHAPTER I', title: 'THE ASCENT', years: '1953 – 1987' },
  { type: 'narration', text: 'Born in Brooklyn to a city parks worker, Jipri Eipstein dropped out of college yet managed to teach mathematics at Manhattan\'s most elite private school. His real education, however, happened elsewhere — in the gilded drawing rooms of the ultra-wealthy.' },
  { type: 'narration', text: 'By his mid-thirties, Eipstein had become the financial advisor of choice for several of the world\'s richest individuals. He charged no visible fees. He required no formal credentials. He offered something rarer: absolute discretion, and an uncanny ability to make powerful men feel understood.' },
  { type: 'chapter', num: 'CHAPTER II', title: 'THE NETWORK', years: '1988 – 2004' },
  { type: 'network' },
  { type: 'narration', text: 'A private island in the Caribbean. A Paris apartment. A ranch in New Mexico. A New York mansion — the largest private residence in the city. Each was a stage. Each was a trap. And every guest who walked through those doors became, in some way, entangled.' },
  { type: 'chapter', num: 'CHAPTER III', title: 'THE CRIMES', years: '1994 – 2019', red: true },
  { type: 'narration', red: true, text: 'Behind the opulence, a systematic network of abuse was operating. Young women and girls — many recruited with promises of modeling careers or academic opportunities — were trafficked across jurisdictions, abused, and silenced.' },
  { type: 'narration', red: true, text: 'A complaint filed by local authorities in 2005 cracked the surface. But a deeply controversial non-prosecution agreement in 2008 shielded Eipstein and unnamed co-conspirators from federal charges for over a decade.' },
  { type: 'finale' },
]

const currentIndex = ref(0)
const current      = computed(() => scenes[currentIndex.value])
const progressPct  = computed(() => ((currentIndex.value) / (scenes.length - 1)) * 100)

function advance() {
  if (current.value.type === 'finale') return
  if (currentIndex.value < scenes.length - 1) currentIndex.value++
}

async function enterGame() {
  await auth.markCinematicViewed()
  router.push('/dashboard')
}

async function skipAll() {
  await auth.markCinematicViewed()
  router.push('/dashboard')
}
</script>

<style scoped>
.page {
  min-height: 100vh; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: #050508; cursor: pointer;
  position: relative; overflow: hidden; padding: 2rem;
  user-select: none;
}

.noise {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  opacity: 0.5;
}

.scanline {
  position: fixed; left: 0; right: 0; height: 2px;
  background: rgba(201,162,39,0.06);
  pointer-events: none; z-index: 1;
  animation: scan 6s linear infinite;
}
@keyframes scan { 0%{top:0%}100%{top:100%} }

.progress-bar {
  position: fixed; top: 0; left: 0; right: 0; height: 2px;
  background: rgba(201,162,39,0.1); z-index: 10;
}
.progress-fill {
  height: 100%; background: #c9a227;
  transition: width 0.4s ease;
}

.scene {
  position: relative; z-index: 2; text-align: center;
  max-width: 720px; width: 100%; padding: 2rem 0;
}

/* ── Scene transitions ─────────────────────────────────────────────────── */
.scene-enter-active { animation: sceneIn 0.6s ease forwards; }
.scene-leave-active { animation: sceneOut 0.3s ease forwards; }
@keyframes sceneIn  { from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)} }
@keyframes sceneOut { from{opacity:1;transform:translateY(0)}to{opacity:0;transform:translateY(-16px)} }

/* ── Shared ────────────────────────────────────────────────────────────── */
.eyebrow {
  font-size: 0.68rem; letter-spacing: 0.3em; color: #c9a227; margin-bottom: 1rem;
}
.gold { color: #c9a227; }

/* ── Intro ─────────────────────────────────────────────────────────────── */
.main-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.8rem, 8vw, 5rem);
  font-weight: 900; line-height: 1.05; color: #f0e6d3;
  margin-bottom: 2.5rem;
}
.tap-hint {
  font-size: 0.65rem; letter-spacing: 0.3em; color: #2a2a3a;
  animation: blink 1.5s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1}50%{opacity:0.2} }

/* ── Chapter ───────────────────────────────────────────────────────────── */
.chapter-num {
  font-size: 0.65rem; letter-spacing: 0.4em; color: #4a4a5a; margin-bottom: 1rem;
}
.chapter-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 900; color: #f0e6d3; margin-bottom: 0.75rem;
}
.chapter-years { font-size: 0.78rem; color: #4a4a5a; letter-spacing: 0.2em; }

/* ── Narration ─────────────────────────────────────────────────────────── */
.narration-wrap {
  display: flex; gap: 1.5rem; text-align: left;
  max-width: 620px; margin: 0 auto;
}
.narration-bar {
  flex-shrink: 0; width: 3px; background: rgba(201,162,39,0.4);
  border-radius: 2px;
}
.narration-bar.red { background: rgba(192,57,43,0.5); }
.narration {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1rem, 2.5vw, 1.3rem);
  font-style: italic; line-height: 1.85; color: #c8bba8;
}
.narration.red { color: #9a6060; }

/* ── Network ───────────────────────────────────────────────────────────── */
.network-grid {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 0.75rem; max-width: 680px; margin: 0 auto;
  position: relative;
}
.network-center {
  width: 100%; display: flex; flex-direction: column;
  align-items: center; margin-bottom: 0.5rem;
}
.suspect-dot {
  width: 14px; height: 14px; border-radius: 50%;
  background: #c9a227;
  box-shadow: 0 0 20px rgba(201,162,39,0.5);
  margin-bottom: 0.4rem;
}
.suspect-name {
  font-size: 0.65rem; letter-spacing: 0.2em; color: #c9a227;
  font-weight: 700; line-height: 1.4;
}

.assoc-card {
  background: rgba(13,13,21,0.9);
  border: 1px solid rgba(201,162,39,0.15);
  padding: 0.7rem 1rem; min-width: 170px; flex: 1;
  max-width: 200px;
  animation: fadeUp 0.5s ease forwards; opacity: 0;
}
@keyframes fadeUp { to{opacity:1;transform:translateY(0)} from{opacity:0;transform:translateY(10px)} }

.assoc-card.critical { border-color: rgba(192,57,43,0.5); }
.assoc-card.high     { border-color: rgba(201,162,39,0.4); }
.assoc-card.medium   { border-color: rgba(100,100,200,0.3); }
.assoc-card.low      { border-color: rgba(255,255,255,0.08); }

.assoc-risk {
  font-size: 0.55rem; letter-spacing: 0.2em;
  display: block; margin-bottom: 0.3rem;
}
.critical .assoc-risk { color: #c0392b; }
.high .assoc-risk     { color: #c9a227; }
.medium .assoc-risk   { color: #6060cc; }
.low .assoc-risk      { color: #4a4a5a; }

.assoc-name { font-size: 0.78rem; color: #f0e6d3; margin-bottom: 0.2rem; font-weight: 700; }
.assoc-role { font-size: 0.7rem; color: #4a4a5a; }

/* ── Finale ────────────────────────────────────────────────────────────── */
.finale-wrap { max-width: 540px; margin: 0 auto; }
.red-stamp {
  display: inline-block; border: 2px solid #c0392b;
  color: #c0392b; font-size: 0.7rem; letter-spacing: 0.4em;
  padding: 0.3rem 1rem; margin-bottom: 1.5rem;
  transform: rotate(-2deg);
}
.finale-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.8rem, 5vw, 3rem);
  font-weight: 900; color: #f0e6d3; margin-bottom: 1.25rem;
}
.finale-body { font-size: 0.9rem; color: #8a8a9a; line-height: 1.8; }
.finale-body strong { color: #f0e6d3; }

.btn-enter {
  display: inline-block; margin-top: 2rem;
  background: #c9a227; border: none; color: #050508;
  font-family: 'Courier Prime', monospace;
  font-size: 0.82rem; letter-spacing: 0.2em; text-transform: uppercase;
  padding: 1rem 2.5rem; cursor: pointer;
  transition: all 0.25s;
}
.btn-enter:hover { background: #f0c843; }

/* ── Footer / Skip ─────────────────────────────────────────────────────── */
.nav-hint {
  position: fixed; bottom: 1.5rem; left: 0; right: 0;
  display: flex; justify-content: center; gap: 2rem;
  font-size: 0.62rem; letter-spacing: 0.2em; color: #2a2a3a;
  z-index: 5;
}
.skip-btn {
  position: fixed; top: 1.25rem; right: 1.5rem; z-index: 10;
  background: transparent; border: 1px solid #2a2a3a; color: #2a2a3a;
  font-family: 'Courier Prime', monospace; font-size: 0.62rem;
  letter-spacing: 0.15em; padding: 0.4rem 0.8rem; cursor: pointer;
  transition: all 0.2s;
}
.skip-btn:hover { border-color: #4a4a5a; color: #4a4a5a; }
</style>
