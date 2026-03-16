<template>
  <GameLayout>
    <div class="tips-page">
      <div class="tips-header">
        <p class="eyebrow">SECURE CHANNEL — ENCRYPTED</p>
        <GlitchText text="ANONYMOUS TIP INBOX" class="page-title"/>
        <p class="sub">Classified information from protected sources. New tips unlock as you review more files.</p>
      </div>

      <div class="tips-list">
        <div v-for="tip in game.tips" :key="tip.id" class="tip-envelope" :class="{ unread: !tip.is_read }" @click="openTip(tip)">
          <div class="env-left">
            <div class="env-icon">{{ categoryIcon(tip.category) }}</div>
            <div class="env-body">
              <p class="env-from">FROM: <span class="from-alias">{{ tip.sender_alias }}</span></p>
              <p class="env-title">{{ tip.title }}</p>
              <span class="env-cat">{{ tip.category_label }}</span>
            </div>
          </div>
          <div class="env-right">
            <span class="unread-dot" v-if="!tip.is_read"/>
            <span class="read-mark" v-else>READ</span>
          </div>
        </div>

        <div v-if="game.tips.length === 0" class="empty-inbox">
          <p class="empty-icon">📭</p>
          <TypewriterText text="NO TIPS AVAILABLE YET. REVIEW MORE FILES TO UNLOCK SOURCES." :speed="30"/>
        </div>
      </div>

      <!-- Tip detail modal -->
      <Transition name="modal">
        <div class="modal-overlay" v-if="selectedTip" @click.self="selectedTip = null">
          <div class="tip-modal">
            <div class="tip-modal-header">
              <div class="tip-from-block">
                <p class="tip-category">{{ categoryIcon(selectedTip.category) }} {{ selectedTip.category_label }}</p>
                <p class="tip-from-alias">SOURCE: {{ selectedTip.sender_alias }}</p>
              </div>
              <button class="modal-close" @click="selectedTip = null">✕</button>
            </div>
            <div class="tip-modal-body">
              <h3 class="tip-modal-title">{{ selectedTip.title }}</h3>
              <div class="tip-divider"/>
              <p class="tip-content">
                <TypewriterText :text="selectedTip.content" :speed="18" :delay="200"/>
              </p>
              <div class="tip-footer">
                <p class="tip-warning">⚠ This information is unverified. Cross-reference with case files before using as evidence.</p>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import TypewriterText from '@/components/TypewriterText.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const selectedTip = ref(null)

onMounted(() => game.fetchTips())

const icons = { location:'📍', associate:'👤', financial:'💰', witness:'👁', evidence:'📄' }
function categoryIcon(cat) { return icons[cat] || '📨' }

async function openTip(tip) {
  selectedTip.value = tip
  if (!tip.is_read) await game.readTip(tip.id)
}
</script>

<style scoped>
.tips-page { padding:2rem 2.5rem; min-height:100vh; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#4a9a5a;margin-bottom:0.4rem; }
.page-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.4rem; }
.sub { font-size:0.75rem;color:#4a4a5a;margin-bottom:2rem; }

.tips-list { display:flex;flex-direction:column;gap:0.75rem; }

.tip-envelope {
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(8,8,14,0.9);border:1px solid rgba(255,255,255,0.05);
  padding:1rem 1.25rem;cursor:pointer;transition:all 0.25s;
}
.tip-envelope:hover { border-color:rgba(74,154,90,0.3);background:rgba(8,8,14,0.97); }
.tip-envelope.unread { border-color:rgba(74,154,90,0.2);background:rgba(74,154,90,0.03); }

.env-left { display:flex;align-items:center;gap:1rem; }
.env-icon { font-size:1.1rem;width:32px;text-align:center; }
.env-from { font-size:0.6rem;letter-spacing:0.15em;color:#4a4a5a;margin-bottom:0.2rem; }
.from-alias { color:#4a9a5a; }
.env-title { font-size:0.88rem;color:#f0e6d3;margin-bottom:0.25rem; }
.env-cat { font-size:0.58rem;letter-spacing:0.12em;color:#4a4a5a;border:1px solid rgba(255,255,255,0.05);padding:0.1rem 0.45rem; }

.env-right { flex-shrink:0; }
.unread-dot { display:block;width:8px;height:8px;border-radius:50%;background:#4a9a5a;animation:pulse-gold 1.5s ease-in-out infinite; }
.read-mark { font-size:0.58rem;letter-spacing:0.12em;color:#2a2a3a; }

.empty-inbox { display:flex;flex-direction:column;align-items:center;gap:1rem;padding:4rem;text-align:center;font-size:0.75rem;color:#4a4a5a; }
.empty-icon { font-size:2rem; }

.modal-overlay { position:fixed;inset:0;z-index:100;background:rgba(5,5,8,0.93);display:flex;align-items:center;justify-content:center;padding:1.5rem; }
.tip-modal { background:#0a0a14;border:1px solid rgba(74,154,90,0.3);width:100%;max-width:560px;animation:fadeUp 0.3s ease; }
.tip-modal-header { display:flex;justify-content:space-between;align-items:flex-start;padding:1.25rem 1.5rem;border-bottom:1px solid rgba(74,154,90,0.1); }
.tip-category { font-size:0.62rem;letter-spacing:0.2em;color:#4a9a5a;margin-bottom:0.25rem; }
.tip-from-alias { font-size:0.72rem;color:#4a4a5a; }
.modal-close { background:transparent;border:none;color:#4a4a5a;font-size:1rem;cursor:pointer; }
.tip-modal-body { padding:1.5rem; }
.tip-modal-title { font-family:'Playfair Display',serif;font-size:1.15rem;color:#f0e6d3;margin-bottom:1rem; }
.tip-divider { height:1px;background:rgba(74,154,90,0.1);margin-bottom:1rem; }
.tip-content { font-size:0.85rem;color:#c8bba8;line-height:1.85;margin-bottom:1.25rem; }
.tip-footer { border-top:1px solid rgba(255,255,255,0.04);padding-top:0.85rem; }
.tip-warning { font-size:0.65rem;color:#4a4a5a;letter-spacing:0.06em;line-height:1.6; }
.modal-enter-active,.modal-leave-active{transition:opacity 0.3s}
.modal-enter-from,.modal-leave-to{opacity:0}
</style>
