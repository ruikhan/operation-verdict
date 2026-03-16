<template>
  <div class="page">
    <div class="noise" />

    <div class="container">
      <div class="header">
        <p class="eyebrow">OPERATION VERDICT</p>
        <h2 class="title">TERMS & <span class="gold">POLICIES</span></h2>
        <p class="sub">Read carefully before entering the investigation system</p>
      </div>

      <div class="scroll-box" ref="scrollEl" @scroll="onScroll">
        <section class="clause">
          <h3>§ 1 — INVESTIGATOR OATH</h3>
          <p>By accessing Operation Verdict, you confirm you are acting as an independent investigator committed to uncovering truth, protecting victims, and ensuring accountability. You agree to handle all case materials with the utmost seriousness and respect for those harmed.</p>
        </section>

        <section class="clause">
          <h3>§ 2 — NATURE OF CONTENT</h3>
          <p>This investigation system contains fictional case files inspired by real-world patterns of institutional abuse, coercion, and trafficking. All named individuals are fictionalised characters. The content is designed for educational and awareness purposes. Nothing within constitutes legal advice or official documentation.</p>
        </section>

        <section class="clause red">
          <h3>§ 3 — SENSITIVE MATERIAL WARNING</h3>
          <p>Case files contain references to crimes against minors, sexual exploitation, coercion, and institutional cover-ups. This content may be distressing. You must be 18 years of age or older to proceed. If you are affected by these themes, please seek support before continuing.</p>
        </section>

        <section class="clause">
          <h3>§ 4 — DATA USAGE</h3>
          <p>Your investigator profile, progress, and case review records are stored securely on our servers. This data is used solely to track your investigation progress within the game. We do not share or sell your personal information to third parties.</p>
        </section>

        <section class="clause">
          <h3>§ 5 — PROHIBITED CONDUCT</h3>
          <p>You agree not to attempt to reverse-engineer the system, reproduce or distribute case file contents, or use this platform to harass or defame any real-world individuals. Violation of these terms will result in immediate account termination.</p>
        </section>

        <section class="clause">
          <h3>§ 6 — GAME OBJECTIVE</h3>
          <p>Your objective as an investigator is to review all available victim testimonies and evidence files, build a compelling conviction case, and ensure the suspect "Jipri Eipstein" is prosecuted to the fullest extent of the law. Justice is the only verdict we seek.</p>
        </section>

        <div class="scroll-cue" v-if="!hasScrolled">↓ Scroll to read all terms</div>
      </div>

      <div class="acceptance-row">
        <label class="checkbox-label" :class="{ disabled: !hasScrolled }">
          <input type="checkbox" v-model="accepted" :disabled="!hasScrolled" />
          <span class="checkmark" />
          <span>I have read and agree to all Terms & Policies. I understand the sensitive nature of this investigation.</span>
        </label>
      </div>

      <button class="btn-proceed" :disabled="!accepted || loading" @click="proceed">
        <span v-if="loading">PROCESSING…</span>
        <span v-else>ENTER THE INVESTIGATION →</span>
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router    = useRouter()
const auth      = useAuthStore()
const scrollEl  = ref(null)
const hasScrolled = ref(false)
const accepted  = ref(false)
const loading   = ref(false)
const errorMsg  = ref('')

function onScroll() {
  const el = scrollEl.value
  if (!el) return
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 40) {
    hasScrolled.value = true
  }
}

async function proceed() {
  loading.value = true
  errorMsg.value = ''
  const ok = await auth.acceptTerms()
  if (ok) {
    router.push('/briefing')
  } else {
    errorMsg.value = 'Failed to record acceptance. Please try again.'
  }
  loading.value = false
}
</script>

<style scoped>
.page {
  min-height: 100vh; display: flex;
  align-items: center; justify-content: center;
  background: #050508; padding: 2rem 1rem;
  position: relative;
}
.noise {
  position: fixed; inset: 0; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  opacity: 0.4;
}
.container {
  position: relative; z-index: 1;
  width: 100%; max-width: 680px;
  animation: fadeUp 0.6s ease;
}
@keyframes fadeUp {
  from { opacity:0; transform:translateY(20px); }
  to   { opacity:1; transform:translateY(0); }
}
.header { text-align: center; margin-bottom: 2rem; }
.eyebrow { font-size: 0.65rem; letter-spacing: 0.3em; color: #c9a227; margin-bottom: 0.5rem; }
.title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.8rem, 5vw, 2.8rem);
  font-weight: 900; color: #f0e6d3; margin-bottom: 0.5rem;
}
.gold { color: #c9a227; }
.sub { font-size: 0.75rem; color: #4a4a5a; letter-spacing: 0.1em; }

.scroll-box {
  background: rgba(13,13,21,0.9);
  border: 1px solid rgba(201,162,39,0.2);
  padding: 1.75rem 2rem;
  max-height: 380px; overflow-y: auto;
  position: relative;
}

.clause {
  margin-bottom: 1.75rem; padding-bottom: 1.75rem;
  border-bottom: 1px solid rgba(201,162,39,0.08);
}
.clause:last-of-type { border-bottom: none; }
.clause h3 {
  font-size: 0.68rem; letter-spacing: 0.2em;
  color: #c9a227; margin-bottom: 0.65rem;
  font-weight: 700;
}
.clause p { font-size: 0.84rem; color: #8a8a9a; line-height: 1.8; }
.clause.red h3 { color: #c0392b; }
.clause.red p  { color: #a06060; }

.scroll-cue {
  position: sticky; bottom: 0;
  text-align: center; padding: 0.5rem;
  font-size: 0.65rem; letter-spacing: 0.2em;
  color: #4a4a5a;
  animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1}50%{opacity:0.3} }

.acceptance-row { padding: 1.25rem 0; }
.checkbox-label {
  display: flex; gap: 0.85rem; align-items: flex-start;
  cursor: pointer; font-size: 0.78rem; color: #8a8a9a; line-height: 1.6;
}
.checkbox-label.disabled { opacity: 0.35; cursor: not-allowed; }
.checkbox-label input { display: none; }
.checkmark {
  flex-shrink: 0; width: 18px; height: 18px; margin-top: 2px;
  border: 1px solid rgba(201,162,39,0.4);
  background: rgba(255,255,255,0.02);
  position: relative; transition: all 0.2s;
}
.checkbox-label input:checked + .checkmark {
  background: #c9a227; border-color: #c9a227;
}
.checkbox-label input:checked + .checkmark::after {
  content: '✓'; position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: #050508; font-weight: 900;
}

.btn-proceed {
  width: 100%; background: transparent; border: 1px solid #c9a227;
  color: #c9a227; font-family: 'Courier Prime', monospace;
  font-size: 0.82rem; letter-spacing: 0.2em; text-transform: uppercase;
  padding: 1rem; cursor: pointer; transition: all 0.25s;
}
.btn-proceed:hover:not(:disabled) { background: #c9a227; color: #050508; }
.btn-proceed:disabled              { opacity: 0.3; cursor: not-allowed; }

.error { margin-top: 0.75rem; font-size: 0.75rem; color: #e74c3c; text-align: center; }
</style>
