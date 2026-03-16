<template>
  <GameLayout>
    <div class="lb-page">
      <div class="lb-header">
        <p class="eyebrow">GLOBAL INVESTIGATOR RANKINGS</p>
        <GlitchText text="LEADERBOARD" class="page-title"/>
        <p class="sub">Race other investigators to achieve a full conviction. Score = conviction strength × time bonus + cipher solves.</p>
      </div>
      <div class="my-rank-card" v-if="myEntry">
        <p class="mr-label">YOUR RANK</p>
        <div class="mr-row">
          <span class="mr-num">#{{ myEntry.rank }}</span>
          <div class="mr-info">
            <p class="mr-name">{{ myEntry.display_name }}</p>
            <p class="mr-score">{{ myEntry.score.toLocaleString() }} pts</p>
          </div>
          <span class="verdict-tag" v-if="myEntry.verdict_reached">⚖ VERDICT</span>
        </div>
      </div>
      <div class="lb-table">
        <div class="lb-thead">
          <span>RANK</span><span>INVESTIGATOR</span><span>SCORE</span><span>CONVICTION</span><span>STATUS</span>
        </div>
        <div v-if="loading" class="lb-loading">
          <TypewriterText text="FETCHING RANKINGS..." :speed="40"/>
        </div>
        <div v-for="entry in leaderboard" :key="entry.rank" class="lb-row" :class="{ me: entry.username === auth.username }">
          <span class="lb-rank" :class="{ gold: entry.rank === 1, silver: entry.rank === 2, bronze: entry.rank === 3 }">
            {{ entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : entry.rank === 3 ? '🥉' : `#${entry.rank}` }}
          </span>
          <span class="lb-name">{{ entry.display_name }}</span>
          <span class="lb-score">{{ entry.score.toLocaleString() }}</span>
          <span class="lb-conv" :class="convClass(entry.conviction_pct)">{{ Math.round(entry.conviction_pct) }}%</span>
          <span class="lb-status">
            <span class="verdict-badge" v-if="entry.verdict_reached">CONVICTED</span>
            <span class="active-badge" v-else>ACTIVE</span>
          </span>
        </div>
        <div v-if="!loading && leaderboard.length === 0" class="lb-empty">
          <TypewriterText text="NO INVESTIGATORS ON THE BOARD YET. BE THE FIRST." :speed="30"/>
        </div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import TypewriterText from '@/components/TypewriterText.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'
import { useAuthStore } from '@/stores/auth'

const game = useGameStore()
const auth = useAuthStore()
const loading = ref(false)

const leaderboard = computed(() => game.leaderboard)
const myEntry = computed(() => leaderboard.value.find(e => e.username === auth.username))
function convClass(p) { return p >= 75 ? 'strong' : p >= 40 ? 'mid' : 'weak' }

onMounted(async () => { loading.value = true; await game.fetchLeaderboard(); loading.value = false })
</script>

<style scoped>
.lb-page { padding:2rem 2.5rem;min-height:100vh; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#c9a227;margin-bottom:0.4rem; }
.page-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.4rem; }
.sub { font-size:0.75rem;color:#4a4a5a;margin-bottom:2rem; }

.my-rank-card { background:rgba(201,162,39,0.05);border:1px solid rgba(201,162,39,0.2);padding:1rem 1.5rem;margin-bottom:1.5rem; }
.mr-label { font-size:0.58rem;letter-spacing:0.2em;color:#4a4a5a;margin-bottom:0.5rem; }
.mr-row { display:flex;align-items:center;gap:1rem; }
.mr-num { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#c9a227;line-height:1; }
.mr-name { font-size:0.88rem;color:#f0e6d3;font-weight:700; }
.mr-score { font-size:0.75rem;color:#c9a227; }
.verdict-tag { font-size:0.65rem;color:#4a9a5a;border:1px solid rgba(74,154,90,0.3);padding:0.2rem 0.65rem;margin-left:auto; }

.lb-table { background:rgba(8,8,14,0.9);border:1px solid rgba(201,162,39,0.1); }
.lb-thead { display:grid;grid-template-columns:60px 1fr 100px 100px 100px;padding:0.65rem 1.25rem;border-bottom:1px solid rgba(201,162,39,0.1);font-size:0.58rem;letter-spacing:0.15em;color:#4a4a5a; }
.lb-row { display:grid;grid-template-columns:60px 1fr 100px 100px 100px;padding:0.85rem 1.25rem;border-bottom:1px solid rgba(255,255,255,0.03);align-items:center;transition:background 0.2s; }
.lb-row:hover { background:rgba(201,162,39,0.03); }
.lb-row.me { background:rgba(201,162,39,0.05);border-left:2px solid #c9a227; }
.lb-rank { font-size:0.85rem; }
.lb-name { font-size:0.82rem;color:#f0e6d3; }
.lb-score{ font-size:0.82rem;color:#c9a227;font-family:'Courier Prime',monospace; }
.lb-conv { font-size:0.78rem;font-weight:700; }
.lb-conv.strong{color:#4a9a5a}.lb-conv.mid{color:#c9a227}.lb-conv.weak{color:#c0392b}
.verdict-badge { font-size:0.55rem;letter-spacing:0.1em;color:#4a9a5a;border:1px solid rgba(74,154,90,0.3);padding:0.12rem 0.45rem; }
.active-badge  { font-size:0.55rem;letter-spacing:0.1em;color:#4a4a5a; }
.lb-loading,.lb-empty { padding:2rem;text-align:center;font-size:0.75rem;color:#4a4a5a; }
</style>
