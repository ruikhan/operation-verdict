<template>
  <GameLayout>
    <div class="courtroom-page">
      <div class="noise-layer"/>

      <!-- Not ready state -->
      <div class="not-ready" v-if="!game.verdictReached && game.convictionPercent < 50">
        <p class="nr-eyebrow">VERDICT ROOM — LOCKED</p>
        <GlitchText text="CASE NOT YET READY" class="nr-title"/>
        <p class="nr-sub">You need sufficient conviction strength before presenting to the court.</p>
        <div class="nr-progress">
          <p class="np-label">CONVICTION REQUIRED: 100% · CURRENT: {{ game.convictionPercent }}%</p>
          <div class="np-track"><div class="np-fill" :style="{ width: game.convictionPercent + '%' }"/></div>
        </div>
        <RouterLink to="/dashboard" class="back-btn">← RETURN TO CASE FILES</RouterLink>
      </div>

      <!-- Verdict room -->
      <div class="verdict-room" v-else>
        <div class="court-header">
          <p class="court-eyebrow">THE PEOPLE v. JIPRI EIPSTEIN</p>
          <GlitchText text="VERDICT" class="court-title"/>
          <p class="court-sub" v-if="game.verdictReached">ALL EVIDENCE REVIEWED · CASE COMPLETE</p>
        </div>

        <!-- Gavel animation -->
        <div class="gavel-area">
          <div class="gavel" :class="{ strike: gavelStrike }">⚖</div>
          <div class="gavel-sound" v-if="gavelStrike">BANG!</div>
        </div>

        <!-- Verdict card -->
        <div class="verdict-card" :class="{ revealed: verdictRevealed }">
          <div class="verdict-stamp">
            <p class="stamp-text">{{ game.verdictReached ? 'GUILTY' : 'CASE IN PROGRESS' }}</p>
          </div>
          <div class="verdict-details" v-if="verdictRevealed">
            <p class="vd-charge">CHARGES: SEX TRAFFICKING · CONSPIRACY · RICO VIOLATIONS</p>
            <p class="vd-conviction">CONVICTION STRENGTH: {{ game.convictionPercent }}%</p>
            <p class="vd-score">INVESTIGATOR SCORE: {{ game.score.toLocaleString() }} POINTS</p>
            <p class="vd-files">FILES REVIEWED: {{ game.filesReviewed }} / {{ game.totalFiles }}</p>
          </div>
        </div>

        <!-- Stats -->
        <div class="case-stats" v-if="verdictRevealed">
          <div class="stat-card">
            <p class="stat-num">{{ game.filesReviewed }}</p>
            <p class="stat-label">FILES REVIEWED</p>
          </div>
          <div class="stat-card">
            <p class="stat-num">{{ game.progress?.ciphers_solved ?? 0 }}</p>
            <p class="stat-label">CIPHERS DECODED</p>
          </div>
          <div class="stat-card">
            <p class="stat-num">{{ game.progress?.tips_read ?? 0 }}</p>
            <p class="stat-label">TIPS PROCESSED</p>
          </div>
          <div class="stat-card">
            <p class="stat-num">{{ game.progress?.corruption_overcome ?? 0 }}</p>
            <p class="stat-label">CORRUPTION OVERCOME</p>
          </div>
        </div>

        <button class="reveal-btn" v-if="!verdictRevealed" @click="revealVerdict">
          DELIVER VERDICT →
        </button>

        <div class="victim-tribute" v-if="verdictRevealed">
          <p class="tribute-text">This investigation is dedicated to the survivors whose voices were silenced for decades. Justice, however delayed, must be pursued without compromise.</p>
        </div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const verdictRevealed = ref(false)
const gavelStrike     = ref(false)

onMounted(() => game.fetchProgress())

function revealVerdict() {
  gavelStrike.value = true
  setTimeout(() => {
    gavelStrike.value = false
    verdictRevealed.value = true
  }, 800)
}
</script>

<style scoped>
.courtroom-page { padding:2rem 2.5rem;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center; }

.not-ready { text-align:center;max-width:500px; }
.nr-eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#c0392b;margin-bottom:0.75rem; }
.nr-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:1rem; }
.nr-sub { font-size:0.82rem;color:#4a4a5a;margin-bottom:2rem;line-height:1.7; }
.nr-progress { margin-bottom:2rem; }
.np-label { font-size:0.62rem;letter-spacing:0.12em;color:#4a4a5a;margin-bottom:0.5rem; }
.np-track { height:4px;background:rgba(255,255,255,0.04); }
.np-fill  { height:100%;background:#c9a227;transition:width 0.6s ease; }
.back-btn { display:inline-block;background:transparent;border:1px solid rgba(201,162,39,0.3);color:#c9a227;font-family:'Courier Prime',monospace;font-size:0.75rem;letter-spacing:0.15em;padding:0.7rem 1.5rem;text-decoration:none;transition:all 0.25s; }
.back-btn:hover { background:rgba(201,162,39,0.1); }

.verdict-room { display:flex;flex-direction:column;align-items:center;gap:2rem;max-width:680px;width:100%;text-align:center; }
.court-header { }
.court-eyebrow { font-size:0.65rem;letter-spacing:0.3em;color:#4a4a5a;margin-bottom:0.75rem; }
.court-title { font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.5rem; }
.court-sub { font-size:0.72rem;color:#4a9a5a;letter-spacing:0.15em; }

.gavel-area { position:relative;height:80px;display:flex;align-items:center;justify-content:center; }
.gavel { font-size:3rem;transition:transform 0.15s ease; }
.gavel.strike { transform:rotate(-30deg) scale(1.3);filter:brightness(1.5); }
.gavel-sound { position:absolute;right:-20px;top:0;font-family:'Playfair Display',serif;font-size:1.2rem;color:#c9a227;font-style:italic;animation:fadeUp 0.3s ease; }

.verdict-card {
  background:rgba(8,8,14,0.95);border:2px solid rgba(201,162,39,0.2);
  padding:2rem 3rem;width:100%;transition:all 0.5s ease;
}
.verdict-card.revealed { border-color:rgba(74,154,90,0.5);background:rgba(8,20,8,0.95); }
.verdict-stamp { }
.stamp-text { font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;letter-spacing:0.1em;color:#c9a227;text-transform:uppercase; }
.verdict-card.revealed .stamp-text { color:#4a9a5a; }
.verdict-details { margin-top:1.5rem;display:flex;flex-direction:column;gap:0.5rem;animation:fadeUp 0.5s ease; }
.vd-charge { font-size:0.72rem;color:#c0392b;letter-spacing:0.1em; }
.vd-conviction { font-size:0.78rem;color:#4a9a5a; }
.vd-score,.vd-files { font-size:0.75rem;color:#c9a227; }

.case-stats { display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;width:100%;animation:fadeUp 0.5s ease 0.2s both; }
.stat-card { background:rgba(201,162,39,0.04);border:1px solid rgba(201,162,39,0.12);padding:1rem;text-align:center; }
.stat-num { font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:900;color:#c9a227;margin-bottom:0.3rem; }
.stat-label { font-size:0.55rem;letter-spacing:0.15em;color:#4a4a5a; }

.reveal-btn { background:transparent;border:1px solid #c9a227;color:#c9a227;font-family:'Courier Prime',monospace;font-size:0.85rem;letter-spacing:0.2em;padding:1rem 3rem;cursor:pointer;transition:all 0.25s; }
.reveal-btn:hover { background:#c9a227;color:#050508; }

.victim-tribute { border-top:1px solid rgba(201,162,39,0.1);padding-top:1.5rem;animation:fadeUp 0.5s ease 0.4s both; }
.tribute-text { font-family:'Playfair Display',serif;font-size:0.9rem;font-style:italic;color:#4a4a5a;line-height:1.85;max-width:480px;margin:0 auto; }
</style>
