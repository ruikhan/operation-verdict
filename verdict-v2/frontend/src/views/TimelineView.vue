<template>
  <GameLayout>
    <div class="timeline-page">
      <div class="tl-header">
        <p class="eyebrow">CHRONOLOGICAL CASE RECORD</p>
        <GlitchText text="CASE TIMELINE" class="page-title"/>
        <p class="sub">The full history of the suspect's rise and crimes. Locked events unlock as you review files.</p>
      </div>

      <!-- Category filter -->
      <div class="filter-row">
        <button v-for="cat in categories" :key="cat.id" class="filter-btn" :class="{ active: activeFilter === cat.id }" @click="activeFilter = cat.id">
          {{ cat.label }}
        </button>
      </div>

      <!-- Timeline -->
      <div class="timeline-track">
        <div class="track-line"/>
        <div
          v-for="(ev, i) in filteredEvents"
          :key="ev.id"
          class="tl-event"
          :class="[ev.category, { locked: !ev.is_unlocked, left: i % 2 === 0, right: i % 2 === 1 }]"
          @click="ev.is_unlocked ? selectEvent(ev) : null"
        >
          <div class="tl-dot" :class="ev.category"/>
          <div class="tl-connector"/>
          <div class="tl-card" :class="ev.category">
            <div v-if="!ev.is_unlocked" class="tl-locked-card">
              <p class="tl-year">{{ ev.year }}</p>
              <p class="tl-locked-text">🔒 CLASSIFIED</p>
              <p class="tl-unlock-hint">Review {{ ev.unlock_after_reviews }} files to unlock</p>
            </div>
            <template v-else>
              <div class="tl-year-row">
                <span class="tl-year">{{ ev.year }}</span>
                <span class="tl-cat-badge" :class="ev.category">{{ ev.category_label }}</span>
              </div>
              <p class="tl-title">{{ ev.title }}</p>
              <p class="tl-desc" v-if="selectedEvent?.id === ev.id">{{ ev.description }}</p>
              <p class="tl-expand" v-else>CLICK TO EXPAND</p>
            </template>
          </div>
        </div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const activeFilter = ref('all')
const selectedEvent = ref(null)

const categories = [
  { id:'all',      label:'ALL EVENTS' },
  { id:'ascent',   label:'RISE TO POWER' },
  { id:'crime',    label:'CRIMINAL ACTS' },
  { id:'cover_up', label:'COVER-UPS' },
  { id:'exposure', label:'EXPOSURE' },
  { id:'legal',    label:'LEGAL ACTION' },
]

const filteredEvents = computed(() =>
  activeFilter.value === 'all'
    ? game.timeline
    : game.timeline.filter(e => e.category === activeFilter.value)
)

function selectEvent(ev) {
  selectedEvent.value = selectedEvent.value?.id === ev.id ? null : ev
}

onMounted(() => game.fetchTimeline())
</script>

<style scoped>
.timeline-page { padding:2rem 2.5rem; min-height:100vh; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#4a4a5a;margin-bottom:0.4rem; }
.page-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.4rem; }
.sub { font-size:0.75rem;color:#4a4a5a;margin-bottom:1.5rem; }

.filter-row { display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:2.5rem; }
.filter-btn { background:transparent;border:1px solid rgba(255,255,255,0.06);color:#4a4a5a;font-family:'Courier Prime',monospace;font-size:0.62rem;letter-spacing:0.12em;padding:0.4rem 0.85rem;cursor:pointer;transition:all 0.2s; }
.filter-btn:hover { border-color:rgba(201,162,39,0.3);color:#c9a227; }
.filter-btn.active { border-color:#c9a227;color:#c9a227;background:rgba(201,162,39,0.05); }

.timeline-track { position:relative;padding:1rem 0 2rem; }
.track-line { position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(201,162,39,0.15);transform:translateX(-50%); }

.tl-event {
  display:flex;align-items:flex-start;gap:0;margin-bottom:2rem;position:relative;
  cursor:pointer;
}
.tl-event.left  { flex-direction:row; }
.tl-event.right { flex-direction:row-reverse; }

.tl-dot {
  position:absolute;left:50%;top:1rem;width:12px;height:12px;border-radius:50%;
  transform:translateX(-50%);z-index:2;border:2px solid #050508;
}
.tl-dot.ascent  { background:#c9a227; }
.tl-dot.crime   { background:#c0392b; }
.tl-dot.cover_up{ background:#6a5acd; }
.tl-dot.exposure{ background:#4a9a5a; }
.tl-dot.legal   { background:#3a8abd; }

.tl-connector { width:50%;height:1px;background:rgba(201,162,39,0.08);margin-top:1.35rem; }

.tl-card {
  width:calc(50% - 24px);background:rgba(8,8,14,0.9);border:1px solid rgba(255,255,255,0.05);
  padding:1rem 1.25rem;transition:all 0.25s;
}
.tl-card:hover { border-color:rgba(201,162,39,0.25); }
.tl-card.ascent:hover  { border-color:rgba(201,162,39,0.3); }
.tl-card.crime:hover   { border-color:rgba(192,57,43,0.3); }
.tl-card.cover_up:hover{ border-color:rgba(106,90,205,0.3); }
.tl-card.exposure:hover{ border-color:rgba(74,154,90,0.3); }
.tl-card.legal:hover   { border-color:rgba(58,138,189,0.3); }

.tl-locked-card { opacity:0.4;text-align:center;padding:0.5rem 0; }
.tl-locked-text { font-size:0.68rem;letter-spacing:0.2em;color:#4a4a5a; }
.tl-unlock-hint { font-size:0.58rem;color:#2a2a3a;margin-top:0.2rem; }

.tl-year-row { display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem; }
.tl-year { font-size:1rem;font-weight:700;color:#c9a227;font-family:'Courier Prime',monospace; }
.tl-cat-badge { font-size:0.55rem;letter-spacing:0.12em;padding:0.12rem 0.45rem;border:1px solid; }
.tl-cat-badge.ascent  { color:#c9a227;border-color:rgba(201,162,39,0.3); }
.tl-cat-badge.crime   { color:#c0392b;border-color:rgba(192,57,43,0.3); }
.tl-cat-badge.cover_up{ color:#6a5acd;border-color:rgba(106,90,205,0.3); }
.tl-cat-badge.exposure{ color:#4a9a5a;border-color:rgba(74,154,90,0.3); }
.tl-cat-badge.legal   { color:#3a8abd;border-color:rgba(58,138,189,0.3); }

.tl-title { font-family:'Playfair Display',serif;font-size:0.9rem;color:#f0e6d3;margin-bottom:0.4rem; }
.tl-desc  { font-size:0.78rem;color:#8a8a9a;line-height:1.7; }
.tl-expand { font-size:0.58rem;letter-spacing:0.15em;color:#2a2a3a; }

@media(max-width:700px) {
  .track-line { left:20px; }
  .tl-event { flex-direction:column!important;padding-left:40px; }
  .tl-connector { display:none; }
  .tl-dot { left:20px; }
  .tl-card { width:100%; }
}
</style>
