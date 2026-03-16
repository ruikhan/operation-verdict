<template>
  <GameLayout>
    <div class="dashboard">
      <!-- Header -->
      <div class="topbar">
        <div>
          <p class="eyebrow">CLASSIFIED DATABASE</p>
          <GlitchText text="VICTIM FILES" class="page-title" />
        </div>
        <div class="top-pills">
          <span class="pill green">{{ game.filesReviewed }} REVIEWED</span>
          <span class="pill gold">{{ game.lockedFiles.length }} LOCKED</span>
          <span class="pill red" v-if="game.activeCorruption.length">{{ game.activeCorruption.length }} BLOCKED</span>
        </div>
      </div>

      <!-- Unlock progress tiers -->
      <div class="tier-row">
        <div v-for="tier in 4" :key="tier" class="tier-chip" :class="{ active: tierUnlocked(tier) }">
          <span>TIER {{ tier }}</span>
          <span class="tier-req" v-if="!tierUnlocked(tier)">{{ tierReq(tier) }} reviews needed</span>
          <span class="tier-req" v-else>UNLOCKED</span>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="game.loading" class="loading-state">
        <div class="dots"><span/><span/><span/></div>
        <TypewriterText text="ACCESSING CLASSIFIED DATABASE..." :speed="40" />
      </div>

      <!-- File grid -->
      <div v-else class="file-grid">
        <div
          v-for="file in game.files"
          :key="file.file_id"
          class="polaroid-card"
          :class="[file.status, {
            reviewed: file.is_reviewed,
            locked: !file.is_unlocked,
            corrupted: file.is_corrupted && !isCorruptionResolved(file)
          }]"
          @click="file.is_unlocked ? openFile(file) : null"
        >
          <!-- Locked overlay -->
          <div class="lock-overlay" v-if="!file.is_unlocked">
            <p class="lock-icon">🔒</p>
            <p class="lock-text">TIER {{ file.unlock_tier }}</p>
            <p class="lock-req">{{ tierReq(parseInt(file.unlock_tier)) }} more reviews</p>
          </div>

          <!-- Corrupted overlay -->
          <div class="corrupt-overlay" v-else-if="file.is_corrupted && !isCorruptionResolved(file)">
            <p class="corrupt-icon">⛔</p>
            <p class="corrupt-text">ACCESS BLOCKED</p>
            <p class="corrupt-sub">{{ file.corruption_blocker }}</p>
            <RouterLink to="/tips" class="corrupt-link">FIND OVERRIDE →</RouterLink>
          </div>

          <!-- Card content -->
          <template v-else>
            <div class="card-top">
              <span class="file-id-tag">{{ file.file_id }}</span>
              <div class="card-badges">
                <span class="cipher-badge" v-if="file.has_cipher">🔐 CIPHER</span>
                <span class="reviewed-badge" v-if="file.is_reviewed">✓</span>
              </div>
            </div>

            <!-- Photo placeholder -->
            <div class="photo-area">
              <div class="photo-inner">
                <div class="photo-lines">
                  <div v-for="i in 5" :key="i" class="photo-line" />
                </div>
                <p class="photo-label">CLASSIFIED</p>
              </div>
              <div class="strength-overlay">
                <div class="strength-bar-v" :style="{ height: file.evidence_strength + '%' }" :class="strengthClass(file.evidence_strength)" />
              </div>
            </div>

            <!-- Polaroid caption -->
            <div class="caption">
              <p class="caption-name">{{ file.code_name }}</p>
              <p class="caption-meta">AGE {{ file.victim_age }} · {{ file.incident_year }}</p>
              <p class="caption-loc">{{ file.location }}</p>
              <div class="status-dot-row">
                <span class="status-dot" :class="file.status" />
                <span class="status-text">{{ file.status_label }}</span>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- File Detail Modal -->
    <Transition name="modal">
      <div class="modal-overlay" v-if="selectedFile" @click.self="closeFile">
        <div class="modal">
          <div class="modal-header">
            <div>
              <p class="modal-eyebrow">⚠ CLASSIFIED EVIDENCE FILE</p>
              <h3 class="modal-title">{{ selectedFile.file_id }} — {{ selectedFile.code_name }}</h3>
            </div>
            <button class="modal-close" @click="closeFile">✕</button>
          </div>

          <div class="modal-body">
            <div class="detail-grid">
              <div class="d-item"><span class="d-label">AGE AT TIME</span><span class="d-val red">{{ selectedFile.victim_age }}</span></div>
              <div class="d-item"><span class="d-label">YEAR</span><span class="d-val">{{ selectedFile.incident_year }}</span></div>
              <div class="d-item"><span class="d-label">LOCATION</span><span class="d-val">{{ selectedFile.location }}</span></div>
              <div class="d-item"><span class="d-label">STATUS</span><span class="d-val" :class="selectedFile.status">{{ selectedFile.status_label }}</span></div>
            </div>

            <div class="evidence-section">
              <p class="s-label">EVIDENCE ON FILE</p>
              <ul class="ev-list">
                <li v-for="(item,i) in selectedFile.evidence_items" :key="i">▸ {{ item }}</li>
              </ul>
            </div>

            <!-- Strength bar -->
            <div class="strength-section">
              <p class="s-label">EVIDENCE STRENGTH <span :class="strengthClass(selectedFile.evidence_strength)">{{ selectedFile.evidence_strength }}%</span></p>
              <div class="str-track"><div class="str-fill" :style="{ width: selectedFile.evidence_strength + '%' }" :class="strengthClass(selectedFile.evidence_strength)"/></div>
            </div>

            <!-- Cipher puzzle -->
            <div class="cipher-section" v-if="selectedFile.has_cipher">
              <p class="s-label">🔐 ENCODED MESSAGE DETECTED</p>
              <div class="cipher-box">
                <p class="cipher-key">{{ selectedFile.cipher_key }}</p>
              </div>
              <div class="cipher-input-row">
                <input v-model="cipherAnswer" type="text" placeholder="ENTER DECODED MESSAGE..." class="cipher-input"
                  @keyup.enter="submitCipher" :disabled="cipherSolved" />
                <button class="cipher-btn" @click="submitCipher" :disabled="cipherSolved || !cipherAnswer">
                  {{ cipherSolved ? '✓ SOLVED' : 'DECODE' }}
                </button>
              </div>
              <p class="cipher-result" :class="{ success: cipherSolved, fail: cipherFail }">
                {{ cipherSolved ? '✓ Cipher decoded — bonus conviction added' : cipherFail ? '✗ Incorrect. Try again.' : '' }}
              </p>
            </div>

            <!-- Notes -->
            <div class="notes-section">
              <label class="s-label">INVESTIGATOR NOTES</label>
              <textarea v-model="reviewNotes" placeholder="Record your analysis..." rows="3" />
            </div>

            <div v-if="selectedFile.is_reviewed" class="already-reviewed">✓ File reviewed and logged to conviction case.</div>
            <button v-else class="btn-review" :disabled="reviewing" @click="submitReview">
              {{ reviewing ? 'LOGGING...' : 'MARK REVIEWED — ADD TO CONVICTION CASE' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </GameLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import TypewriterText from '@/components/TypewriterText.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const selectedFile = ref(null)
const reviewNotes  = ref('')
const reviewing    = ref(false)
const cipherAnswer = ref('')
const cipherSolved = ref(false)
const cipherFail   = ref(false)

onMounted(() => game.fetchAll())

function tierUnlocked(tier) {
  const req = { 1:0, 2:2, 3:4, 4:6 }
  return game.filesReviewed >= req[tier]
}
function tierReq(tier) {
  const req = { 1:0, 2:2, 3:4, 4:6 }
  return Math.max(0, req[tier] - game.filesReviewed)
}
function isCorruptionResolved(file) {
  const ev = game.corruption.find(c => c.affected_file === file.id)
  return !ev || ev.is_resolved
}
function strengthClass(v) {
  return v >= 75 ? 'strong' : v >= 45 ? 'mid' : 'weak'
}

function openFile(file) {
  selectedFile.value = file
  reviewNotes.value  = ''
  cipherAnswer.value = ''
  cipherSolved.value = false
  cipherFail.value   = false
}
function closeFile() { selectedFile.value = null }

async function submitReview() {
  if (!selectedFile.value) return
  reviewing.value = true
  const result = await game.reviewFile(selectedFile.value.file_id, reviewNotes.value)
  if (result) selectedFile.value = { ...selectedFile.value, is_reviewed: true }
  reviewing.value = false
}

async function submitCipher() {
  if (!selectedFile.value || !cipherAnswer.value) return
  const result = await game.solveCipher(selectedFile.value.file_id, cipherAnswer.value)
  if (result.correct) { cipherSolved.value = true; cipherFail.value = false }
  else { cipherFail.value = true; setTimeout(() => { cipherFail.value = false }, 2000) }
}
</script>

<style scoped>
.dashboard { padding:2rem 2.5rem; min-height:100vh; }
.topbar { display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid rgba(201,162,39,0.1); }
.eyebrow { font-size:0.62rem; letter-spacing:0.3em; color:#4a4a5a; margin-bottom:0.25rem; }
.page-title { font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:#f0e6d3; }
.top-pills { display:flex; gap:0.5rem; flex-wrap:wrap; }
.pill { font-size:0.6rem; letter-spacing:0.12em; padding:0.3rem 0.75rem; border:1px solid; }
.pill.green { color:#4a9a5a; border-color:rgba(74,154,90,0.3); }
.pill.gold  { color:#c9a227; border-color:rgba(201,162,39,0.3); }
.pill.red   { color:#c0392b; border-color:rgba(192,57,43,0.3); }

.tier-row { display:flex; gap:0.5rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.tier-chip {
  padding:0.4rem 0.85rem; border:1px solid rgba(255,255,255,0.04);
  font-size:0.6rem; letter-spacing:0.12em; color:#2a2a3a;
}
.tier-chip.active { border-color:rgba(201,162,39,0.3); color:#c9a227; }
.tier-req { display:block; font-size:0.55rem; color:#2a2a3a; margin-top:0.1rem; }
.tier-chip.active .tier-req { color:#4a4a5a; }

.loading-state { display:flex; flex-direction:column; align-items:center; gap:1rem; padding:4rem; font-size:0.78rem; color:#4a4a5a; }
.dots { display:flex; gap:6px; }
.dots span { width:8px;height:8px;background:#c9a227;border-radius:50%;animation:pulse-gold 1.2s ease-in-out infinite; }
.dots span:nth-child(2){animation-delay:.2s}.dots span:nth-child(3){animation-delay:.4s}

.file-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:1.25rem; }

.polaroid-card {
  background:#0a0a12; border:1px solid rgba(201,162,39,0.1);
  cursor:pointer; transition:all 0.25s; position:relative;
  padding:0.85rem 0.85rem 1.25rem;
}
.polaroid-card:hover:not(.locked):not(.corrupted) {
  border-color:rgba(201,162,39,0.45); transform:translateY(-3px) rotate(0.5deg);
  box-shadow:0 8px 24px rgba(0,0,0,0.5);
}
.polaroid-card.reviewed { border-color:rgba(74,154,90,0.2); }
.polaroid-card.locked   { cursor:not-allowed; opacity:0.5; }
.polaroid-card.corrupted{ cursor:not-allowed; }

.lock-overlay, .corrupt-overlay {
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:220px; text-align:center; gap:0.4rem;
}
.lock-icon,.corrupt-icon { font-size:1.4rem; }
.lock-text,.corrupt-text { font-size:0.68rem;letter-spacing:0.2em;color:#4a4a5a; }
.lock-req { font-size:0.6rem;color:#2a2a3a; }
.corrupt-sub { font-size:0.6rem;color:#c0392b;opacity:0.7; }
.corrupt-link { font-size:0.6rem;color:#c9a227;text-decoration:none;margin-top:0.4rem;letter-spacing:0.12em; }

.card-top { display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem; }
.file-id-tag { font-size:0.6rem;letter-spacing:0.2em;color:#2a2a3a; }
.card-badges { display:flex;gap:0.3rem; }
.cipher-badge { font-size:0.55rem;color:#6a5acd;border:1px solid rgba(106,90,205,0.3);padding:0.1rem 0.35rem; }
.reviewed-badge { font-size:0.6rem;color:#4a9a5a;border:1px solid rgba(74,154,90,0.3);padding:0.1rem 0.35rem;font-weight:700; }

.photo-area { position:relative;background:#050508;height:140px;margin-bottom:0.75rem;overflow:hidden; }
.photo-inner { position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px; }
.photo-lines { display:flex;flex-direction:column;gap:6px;width:60%; }
.photo-line { height:1px;background:rgba(201,162,39,0.08); }
.photo-label { font-size:0.6rem;letter-spacing:0.25em;color:#1a1a22; }
.strength-overlay { position:absolute;right:6px;top:6px;bottom:6px;width:4px;background:rgba(255,255,255,0.03); }
.strength-bar-v { position:absolute;bottom:0;left:0;width:100%;transition:height 0.6s ease; }
.strength-bar-v.strong { background:#4a9a5a; }
.strength-bar-v.mid    { background:#c9a227; }
.strength-bar-v.weak   { background:#c0392b; }

.caption { padding-top:0.5rem;border-top:1px solid rgba(255,255,255,0.04); }
.caption-name { font-family:'Playfair Display',serif;font-size:0.82rem;font-weight:700;color:#f0e6d3;margin-bottom:0.2rem; }
.caption-meta { font-size:0.6rem;color:#4a4a5a; }
.caption-loc  { font-size:0.6rem;color:#2a2a3a;margin-bottom:0.4rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis; }
.status-dot-row { display:flex;align-items:center;gap:0.4rem; }
.status-dot { width:6px;height:6px;border-radius:50; }
.status-dot.high_confidence,.status-dot.corroborated,.status-dot.original { background:#4a9a5a; }
.status-dot.pending,.status-dot.active { background:#c9a227; }
.status-dot.sealed,.status-dot.cold,.status-dot.recanted { background:#c0392b; }
.status-text { font-size:0.58rem;color:#4a4a5a;letter-spacing:0.06em; }

/* Modal */
.modal-overlay { position:fixed;inset:0;z-index:100;background:rgba(5,5,8,0.93);display:flex;align-items:center;justify-content:center;padding:1.5rem; }
.modal { background:#0a0a14;border:1px solid rgba(201,162,39,0.3);width:100%;max-width:600px;max-height:90vh;overflow-y:auto;animation:fadeUp 0.3s ease; }
.modal-header { display:flex;justify-content:space-between;align-items:flex-start;padding:1.5rem 1.75rem 1.25rem;border-bottom:1px solid rgba(201,162,39,0.1); }
.modal-eyebrow { font-size:0.6rem;letter-spacing:0.25em;color:#c0392b;margin-bottom:0.35rem; }
.modal-title { font-family:'Playfair Display',serif;font-size:1.15rem;color:#f0e6d3; }
.modal-close { background:transparent;border:none;color:#4a4a5a;font-size:1.1rem;cursor:pointer; }
.modal-body { padding:1.5rem 1.75rem;display:flex;flex-direction:column;gap:1.25rem; }
.detail-grid { display:grid;grid-template-columns:1fr 1fr;gap:0.85rem; }
.d-item { display:flex;flex-direction:column;gap:0.25rem; }
.d-label { font-size:0.58rem;letter-spacing:0.15em;color:#4a4a5a; }
.d-val { font-size:0.85rem;color:#f0e6d3; }
.d-val.red { color:#c0392b;font-weight:700; }
.d-val.high_confidence,.d-val.corroborated { color:#4a9a5a; }
.d-val.pending,.d-val.active { color:#c9a227; }
.d-val.sealed,.d-val.cold,.d-val.recanted { color:#c0392b; }
.s-label { font-size:0.6rem;letter-spacing:0.2em;color:#4a4a5a;margin-bottom:0.5rem;display:flex;gap:0.5rem;align-items:center; }
.s-label .strong { color:#4a9a5a; }
.s-label .mid    { color:#c9a227; }
.s-label .weak   { color:#c0392b; }
.ev-list { list-style:none;display:flex;flex-direction:column;gap:0.4rem; }
.ev-list li { font-size:0.82rem;color:#8a8a9a; }
.str-track { height:4px;background:rgba(255,255,255,0.04); }
.str-fill  { height:100%;transition:width 0.6s ease; }
.str-fill.strong{background:#4a9a5a}.str-fill.mid{background:#c9a227}.str-fill.weak{background:#c0392b}
.cipher-section { background:rgba(106,90,205,0.05);border:1px solid rgba(106,90,205,0.2);padding:1rem; }
.cipher-box { background:#050508;padding:0.75rem;margin:0.5rem 0; }
.cipher-key { font-family:'Courier Prime',monospace;font-size:0.78rem;color:#6a5acd;letter-spacing:0.1em;word-break:break-all; }
.cipher-input-row { display:flex;gap:0.5rem; }
.cipher-input { flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(106,90,205,0.3);color:#f0e6d3;font-family:'Courier Prime',monospace;font-size:0.82rem;padding:0.6rem 0.85rem;outline:none;text-transform:uppercase; }
.cipher-btn { background:transparent;border:1px solid rgba(106,90,205,0.5);color:#6a5acd;font-family:'Courier Prime',monospace;font-size:0.7rem;letter-spacing:0.15em;padding:0 1rem;cursor:pointer;transition:all 0.2s; }
.cipher-btn:hover:not(:disabled) { background:#6a5acd;color:#fff; }
.cipher-btn:disabled { opacity:0.4;cursor:not-allowed; }
.cipher-result { font-size:0.72rem;margin-top:0.4rem; }
.cipher-result.success { color:#4a9a5a; }
.cipher-result.fail    { color:#c0392b; }
.notes-section { display:flex;flex-direction:column;gap:0.4rem; }
textarea { background:rgba(255,255,255,0.02);border:1px solid rgba(201,162,39,0.2);color:#f0e6d3;font-family:'Courier Prime',monospace;font-size:0.82rem;padding:0.75rem 1rem;outline:none;resize:vertical;width:100%;transition:border-color 0.2s; }
textarea:focus { border-color:rgba(201,162,39,0.5); }
textarea::placeholder { color:#2a2a3a; }
.already-reviewed { font-size:0.75rem;color:#4a9a5a;letter-spacing:0.1em;padding:0.75rem;border:1px solid rgba(74,154,90,0.25); }
.btn-review { background:transparent;border:1px solid #c9a227;color:#c9a227;font-family:'Courier Prime',monospace;font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;padding:0.9rem;cursor:pointer;transition:all 0.25s;width:100%; }
.btn-review:hover:not(:disabled){background:#c9a227;color:#050508}
.btn-review:disabled{opacity:0.35;cursor:not-allowed}
.modal-enter-active,.modal-leave-active{transition:opacity 0.3s}
.modal-enter-from,.modal-leave-to{opacity:0}
</style>
