<template>
  <GameLayout>
    <div class="board-page">
      <div class="board-header">
        <p class="eyebrow">INVESTIGATION COMMAND CENTER</p>
        <GlitchText text="EVIDENCE BOARD" class="page-title"/>
        <p class="sub">All reviewed evidence and connections. New nodes appear as you review files.</p>
      </div>

      <div class="board-area" ref="boardRef">
        <svg class="strings-svg" :width="boardW" :height="boardH">
          <line v-for="(conn, i) in connections" :key="i"
            :x1="conn.x1" :y1="conn.y1" :x2="conn.x2" :y2="conn.y2"
            stroke="rgba(201,162,39,0.25)" stroke-width="1" stroke-dasharray="4 4"/>
        </svg>

        <!-- Central suspect node -->
        <div class="board-node suspect-node" :style="{ left: centerX - 60 + 'px', top: centerY - 40 + 'px' }">
          <div class="node-pin red"/>
          <p class="node-label suspect">JIPRI EIPSTEIN</p>
          <p class="node-sub">PRIMARY SUSPECT</p>
        </div>

        <!-- File nodes -->
        <div
          v-for="(file, i) in reviewedFiles"
          :key="file.file_id"
          class="board-node file-node"
          :class="strengthClass(file.evidence_strength)"
          :style="fileNodePos(i)"
        >
          <div class="node-pin gold"/>
          <p class="node-id">{{ file.file_id }}</p>
          <p class="node-codename">{{ file.code_name }}</p>
          <p class="node-strength">{{ file.evidence_strength }}%</p>
        </div>

        <!-- Associate nodes -->
        <div
          v-for="(assoc, i) in visibleAssociates"
          :key="assoc.name"
          class="board-node assoc-node"
          :class="assoc.risk"
          :style="assocNodePos(i)"
        >
          <div class="node-pin" :class="assoc.risk"/>
          <p class="node-assoc-name">{{ assoc.short }}</p>
          <p class="node-role">{{ assoc.role }}</p>
        </div>

        <!-- Empty state -->
        <div class="board-empty" v-if="reviewedFiles.length === 0">
          <TypewriterText text="NO EVIDENCE PINNED YET. REVIEW CASE FILES TO POPULATE THE BOARD." :speed="30"/>
        </div>
      </div>

      <!-- Legend -->
      <div class="legend">
        <div class="legend-item"><span class="leg-dot red"/><span>Primary Suspect</span></div>
        <div class="legend-item"><span class="leg-dot gold"/><span>Evidence File</span></div>
        <div class="legend-item"><span class="leg-dot critical"/><span>Critical Associate</span></div>
        <div class="legend-item"><span class="leg-dot high"/><span>High Risk Associate</span></div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import TypewriterText from '@/components/TypewriterText.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game    = useGameStore()
const boardRef= ref(null)
const boardW  = ref(900)
const boardH  = ref(600)

const centerX = computed(() => boardW.value / 2)
const centerY = computed(() => boardH.value / 2)

const reviewedFiles = computed(() => game.files.filter(f => f.is_reviewed))

const allAssociates = [
  { name:'Lady Ghilaine Maxwell', short:'MAXWELL', role:'Recruiter', risk:'critical' },
  { name:'Prince Aldric', short:'PRINCE ALDRIC', role:'Royal Assoc.', risk:'high' },
  { name:'Sen. Carver', short:'SEN. CARVER', role:'Legislator', risk:'high' },
  { name:'Lord Mandelborough', short:'LORD MANDEL', role:'Political', risk:'high' },
]
const visibleAssociates = computed(() => allAssociates.slice(0, Math.min(allAssociates.length, Math.floor(reviewedFiles.value.length / 2) + 1)))

function fileNodePos(i) {
  const total = reviewedFiles.value.length || 1
  const angle = (i / total) * 2 * Math.PI - Math.PI / 2
  const r = Math.min(boardW.value, boardH.value) * 0.32
  const x = centerX.value + r * Math.cos(angle) - 60
  const y = centerY.value + r * Math.sin(angle) - 35
  return { left: x + 'px', top: y + 'px' }
}

function assocNodePos(i) {
  const total = visibleAssociates.value.length || 1
  const angle = (i / total) * 2 * Math.PI + Math.PI / 4
  const r = Math.min(boardW.value, boardH.value) * 0.45
  const x = centerX.value + r * Math.cos(angle) - 55
  const y = centerY.value + r * Math.sin(angle) - 30
  return { left: x + 'px', top: y + 'px' }
}

const connections = computed(() => {
  const conns = []
  const cxPx = centerX.value
  const cyPx = centerY.value
  reviewedFiles.value.forEach((_, i) => {
    const pos = fileNodePos(i)
    conns.push({ x1: cxPx, y1: cyPx, x2: parseInt(pos.left) + 60, y2: parseInt(pos.top) + 35 })
  })
  visibleAssociates.value.forEach((_, i) => {
    const pos = assocNodePos(i)
    conns.push({ x1: cxPx, y1: cyPx, x2: parseInt(pos.left) + 55, y2: parseInt(pos.top) + 30 })
  })
  return conns
})

function strengthClass(v) { return v >= 75 ? 'strong' : v >= 45 ? 'mid' : 'weak' }

function resize() {
  if (boardRef.value) { boardW.value = boardRef.value.offsetWidth; boardH.value = Math.max(500, boardRef.value.offsetHeight) }
}
onMounted(() => { resize(); window.addEventListener('resize', resize) })
onUnmounted(() => window.removeEventListener('resize', resize))
</script>

<style scoped>
.board-page { padding:2rem 2.5rem;min-height:100vh;display:flex;flex-direction:column; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#4a4a5a;margin-bottom:0.4rem; }
.page-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.4rem; }
.sub { font-size:0.75rem;color:#4a4a5a;margin-bottom:1.5rem; }

.board-area {
  flex:1;min-height:580px;background:rgba(5,5,8,0.8);border:1px solid rgba(201,162,39,0.1);
  position:relative;overflow:hidden;
  background-image:
    linear-gradient(rgba(201,162,39,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(201,162,39,0.03) 1px, transparent 1px);
  background-size:40px 40px;
}
.strings-svg { position:absolute;top:0;left:0;pointer-events:none; }

.board-node { position:absolute;background:rgba(10,10,18,0.95);border:1px solid;padding:0.6rem 0.85rem;min-width:100px;max-width:140px;text-align:center;cursor:default; }

.suspect-node { border-color:rgba(192,57,43,0.5);min-width:120px;animation:pulse-gold 3s ease-in-out infinite; }
.file-node { border-color:rgba(201,162,39,0.2);animation:fadeUp 0.4s ease; }
.file-node.strong { border-color:rgba(74,154,90,0.35); }
.file-node.weak   { border-color:rgba(192,57,43,0.25); }
.assoc-node { border-color:rgba(255,255,255,0.05); }
.assoc-node.critical { border-color:rgba(192,57,43,0.3); }
.assoc-node.high     { border-color:rgba(201,162,39,0.2); }

.node-pin { width:10px;height:10px;border-radius:50%;margin:0 auto 0.4rem;border:2px solid rgba(5,5,8,0.8); }
.node-pin.red      { background:#c0392b; }
.node-pin.gold     { background:#c9a227; }
.node-pin.critical { background:#c0392b; }
.node-pin.high     { background:#c9a227; }

.node-label.suspect { font-size:0.72rem;font-weight:700;color:#f0e6d3;letter-spacing:0.06em; }
.node-sub   { font-size:0.55rem;color:#c0392b;letter-spacing:0.12em;margin-top:0.15rem; }
.node-id    { font-size:0.58rem;color:#4a4a5a;letter-spacing:0.15em; }
.node-codename { font-size:0.7rem;color:#f0e6d3;font-weight:700;margin:0.2rem 0; }
.node-strength { font-size:0.6rem;color:#c9a227; }
.node-assoc-name { font-size:0.68rem;color:#f0e6d3;font-weight:700; }
.node-role { font-size:0.55rem;color:#4a4a5a;margin-top:0.15rem; }

.board-empty { position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:0.75rem;color:#2a2a3a;text-align:center;padding:2rem; }

.legend { display:flex;gap:1.5rem;margin-top:1rem;padding-top:0.85rem;border-top:1px solid rgba(201,162,39,0.08);flex-wrap:wrap; }
.legend-item { display:flex;align-items:center;gap:0.4rem;font-size:0.62rem;color:#4a4a5a; }
.leg-dot { width:8px;height:8px;border-radius:50%; }
.leg-dot.red{background:#c0392b}.leg-dot.gold{background:#c9a227}.leg-dot.critical{background:#c0392b;opacity:0.6}.leg-dot.high{background:#c9a227;opacity:0.6}
</style>
