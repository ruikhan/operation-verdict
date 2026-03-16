<template>
  <GameLayout>
    <div class="suspect-page">
      <p class="eyebrow">CLASSIFIED SUBJECT PROFILE</p>

      <!-- Main suspect -->
      <div class="main-profile">
        <div class="mugshot-large">
          <div class="mug-lines"><div v-for="i in 10" :key="i" class="ml"/></div>
          <p class="mug-initial">JE</p>
          <div class="mug-stamp">SUSPECT</div>
        </div>
        <div class="profile-info">
          <p class="profile-eyebrow">PRIMARY SUSPECT — FILE #001</p>
          <GlitchText text="JIPRI EIPSTEIN" class="profile-name"/>
          <div class="profile-grid">
            <div class="pf-item"><span class="pf-label">BORN</span><span class="pf-val">1953, Brooklyn NY</span></div>
            <div class="pf-item"><span class="pf-label">STATUS</span><span class="pf-val red">DECEASED — DISPUTED</span></div>
            <div class="pf-item"><span class="pf-label">OCCUPATION</span><span class="pf-val">Financial Manager</span></div>
            <div class="pf-item"><span class="pf-label">KNOWN RESIDENCES</span><span class="pf-val">Manhattan · Palm Beach · Paris · Little St. James</span></div>
            <div class="pf-item"><span class="pf-label">CHARGES</span><span class="pf-val red">Sex Trafficking · Conspiracy · RICO</span></div>
            <div class="pf-item"><span class="pf-label">NPA SIGNED</span><span class="pf-val gold">2008 — Controversial</span></div>
          </div>
          <div class="conviction-meter">
            <p class="pf-label">CASE CONVICTION STRENGTH</p>
            <div class="conv-bar"><div class="conv-inner" :style="{ width: game.convictionPercent + '%' }"/></div>
            <p class="conv-val" :class="convClass">{{ game.convictionPercent }}% — {{ convLabel }}</p>
          </div>
          <RouterLink to="/interrogation" class="interrogate-btn">INTERROGATE THIS SUSPECT →</RouterLink>
        </div>
      </div>

      <!-- Network -->
      <div class="network-section">
        <p class="section-title">KNOWN ASSOCIATES & NETWORK</p>
        <div class="associates-grid">
          <div v-for="assoc in associates" :key="assoc.name" class="assoc-profile" :class="assoc.risk">
            <div class="assoc-mug">
              <p class="assoc-initial">{{ assoc.initials }}</p>
            </div>
            <div class="assoc-info">
              <p class="assoc-name">{{ assoc.name }}</p>
              <p class="assoc-role">{{ assoc.role }}</p>
              <span class="risk-chip" :class="assoc.risk">{{ assoc.risk }}</span>
            </div>
            <div class="connection-type">
              <p class="conn-label">CONNECTION</p>
              <p class="conn-val">{{ assoc.connection }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Properties -->
      <div class="properties-section">
        <p class="section-title">KNOWN PROPERTIES & LOCATIONS</p>
        <div class="props-grid">
          <div v-for="prop in properties" :key="prop.name" class="prop-card">
            <p class="prop-icon">{{ prop.icon }}</p>
            <p class="prop-name">{{ prop.name }}</p>
            <p class="prop-loc">{{ prop.location }}</p>
            <p class="prop-note">{{ prop.note }}</p>
          </div>
        </div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { computed } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const convClass = computed(() => {
  const p = game.convictionPercent
  return p >= 75 ? 'strong' : p >= 40 ? 'mid' : 'weak'
})
const convLabel = computed(() => {
  const p = game.convictionPercent
  if (p >= 90) return 'GUILTY BEYOND REASONABLE DOUBT'
  if (p >= 75) return 'STRONG CASE FOR PROSECUTION'
  if (p >= 50) return 'SUBSTANTIAL EVIDENCE'
  if (p >= 25) return 'PRELIMINARY CASE'
  return 'INVESTIGATION BEGINNING'
})

const associates = [
  { initials:'GM', name:'Lady Ghilaine Maxwell', role:'Primary Recruiter', risk:'critical', connection:'Romantic partner turned operational partner' },
  { initials:'PA', name:'Prince Aldric of Wessex', role:'Royal Associate', risk:'high', connection:'Documented social ties, flight logs' },
  { initials:'BM', name:'Lord Basil Mandelborough', role:'Political Advisor', risk:'high', connection:'Email correspondence, shared events' },
  { initials:'HC', name:'Senator Howard Carver', role:'U.S. Legislator', risk:'high', connection:'Financial records, island visits' },
  { initials:'VR', name:'Viktor Rashenko', role:'Financier', risk:'medium', connection:'Shell company cross-ownership' },
  { initials:'RP', name:'Dr. Raymond Pell', role:'Academic Donor', risk:'low', connection:'Research funding, academic access' },
]

const properties = [
  { icon:'🏛', name:'Manhattan Mansion', location:'71st St, New York', note:'Largest private residence in NYC at time of purchase' },
  { icon:'🌴', name:'Little St. James Island', location:'U.S. Virgin Islands', note:'Primary site of criminal activity. Nicknamed "Pedophile Island"' },
  { icon:'🏡', name:'Zorro Ranch', location:'Stanley, New Mexico', note:'66-acre compound. Staff reported irregular visitor patterns' },
  { icon:'🗼', name:'Paris Apartment', location:'Avenue Foch, Paris', note:'Maintained under third-party ownership. Used for international meetings' },
  { icon:'🌊', name:'Palm Beach Estate', location:'El Brillo Way, Palm Beach', note:'Site of original 2005 complaint. Searched by FBI in 2006' },
]
</script>

<style scoped>
.suspect-page { padding:2rem 2.5rem;min-height:100vh; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#c0392b;margin-bottom:1.5rem; }

.main-profile { display:flex;gap:2rem;margin-bottom:3rem;flex-wrap:wrap; }
.mugshot-large {
  width:180px;height:220px;flex-shrink:0;background:#050508;border:1px solid rgba(192,57,43,0.3);
  position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;
}
.mug-lines { position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-evenly;padding:6px; }
.ml { height:1px;background:rgba(192,57,43,0.06); }
.mug-initial { font-family:'Playfair Display',serif;font-size:3rem;font-weight:900;color:rgba(192,57,43,0.25);position:relative;z-index:1; }
.mug-stamp {
  position:absolute;top:12px;right:-20px;background:rgba(192,57,43,0.15);border:2px solid rgba(192,57,43,0.5);
  color:#c0392b;font-size:0.6rem;letter-spacing:0.2em;padding:0.2rem 1.5rem;transform:rotate(15deg);
}

.profile-info { flex:1;min-width:280px; }
.profile-eyebrow { font-size:0.62rem;letter-spacing:0.2em;color:#c0392b;margin-bottom:0.5rem; }
.profile-name { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:1.25rem; }
.profile-grid { display:grid;grid-template-columns:1fr 1fr;gap:0.85rem;margin-bottom:1.25rem; }
.pf-item { display:flex;flex-direction:column;gap:0.2rem; }
.pf-label { font-size:0.58rem;letter-spacing:0.15em;color:#4a4a5a; }
.pf-val { font-size:0.82rem;color:#f0e6d3; }
.pf-val.red  { color:#c0392b; }
.pf-val.gold { color:#c9a227; }

.conviction-meter { margin-bottom:1.25rem; }
.conv-bar { height:6px;background:rgba(255,255,255,0.04);margin:0.5rem 0 0.35rem; }
.conv-inner { height:100%;background:#c9a227;transition:width 0.8s ease; }
.conv-val { font-size:0.72rem;font-weight:700; }
.conv-val.strong{color:#4a9a5a}.conv-val.mid{color:#c9a227}.conv-val.weak{color:#c0392b}

.interrogate-btn { display:inline-block;margin-top:0.25rem;background:rgba(192,57,43,0.1);border:1px solid rgba(192,57,43,0.4);color:#c0392b;font-family:'Courier Prime',monospace;font-size:0.72rem;letter-spacing:0.15em;padding:0.65rem 1.5rem;text-decoration:none;transition:all 0.25s; }
.interrogate-btn:hover { background:#c0392b;color:#fff; }

.section-title { font-size:0.65rem;letter-spacing:0.25em;color:#4a4a5a;margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:1px solid rgba(201,162,39,0.08); }
.network-section { margin-bottom:2.5rem; }
.associates-grid { display:flex;flex-direction:column;gap:0.6rem; }
.assoc-profile { display:flex;align-items:center;gap:1rem;background:rgba(8,8,14,0.9);border:1px solid rgba(255,255,255,0.04);padding:0.85rem 1.1rem; }
.assoc-profile.critical { border-left:2px solid rgba(192,57,43,0.5); }
.assoc-profile.high     { border-left:2px solid rgba(201,162,39,0.4); }
.assoc-mug { width:40px;height:48px;background:#050508;border:1px solid rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;flex-shrink:0; }
.assoc-initial { font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:700;color:#4a4a5a; }
.assoc-info { flex:1; }
.assoc-name { font-size:0.85rem;color:#f0e6d3;font-weight:700;margin-bottom:0.15rem; }
.assoc-role { font-size:0.65rem;color:#4a4a5a;margin-bottom:0.35rem; }
.risk-chip { font-size:0.55rem;letter-spacing:0.12em;padding:0.1rem 0.45rem;border:1px solid; }
.risk-chip.critical{color:#c0392b;border-color:rgba(192,57,43,0.3)}.risk-chip.high{color:#c9a227;border-color:rgba(201,162,39,0.3)}.risk-chip.medium{color:#6a5acd;border-color:rgba(106,90,205,0.3)}.risk-chip.low{color:#4a4a5a;border-color:rgba(255,255,255,0.08)}
.connection-type { text-align:right;min-width:200px; }
.conn-label { font-size:0.55rem;letter-spacing:0.15em;color:#2a2a3a;margin-bottom:0.2rem; }
.conn-val { font-size:0.7rem;color:#4a4a5a;font-style:italic; }

.props-grid { display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:0.85rem; }
.prop-card { background:rgba(8,8,14,0.9);border:1px solid rgba(255,255,255,0.04);padding:1rem;transition:border-color 0.2s; }
.prop-card:hover { border-color:rgba(201,162,39,0.2); }
.prop-icon { font-size:1.2rem;margin-bottom:0.5rem; }
.prop-name { font-size:0.85rem;color:#f0e6d3;font-weight:700;margin-bottom:0.2rem; }
.prop-loc  { font-size:0.65rem;color:#c9a227;margin-bottom:0.5rem; }
.prop-note { font-size:0.65rem;color:#4a4a5a;line-height:1.6; }
</style>
