<template>
  <GameLayout>
    <div class="interrogation-page">
      <div class="noise-layer"/>

      <div class="int-header">
        <p class="eyebrow">LIVE INTERROGATION SESSION</p>
        <GlitchText text="SUSPECT INTERVIEW ROOM" class="page-title" />
        <p class="sub">Question the suspect directly. Every exchange may reveal hidden clues.</p>
      </div>

      <!-- Suspect selector -->
      <div class="suspect-row" v-if="!session">
        <div
          v-for="s in suspects" :key="s.id"
          class="suspect-card"
          :class="{ selected: selectedSuspect === s.id }"
          @click="selectedSuspect = s.id"
        >
          <div class="mugshot">
            <div class="mugshot-lines"><div v-for="i in 6" :key="i" class="mshot-line"/></div>
            <p class="mugshot-initial">{{ s.initial }}</p>
          </div>
          <p class="suspect-name">{{ s.name }}</p>
          <p class="suspect-role">{{ s.role }}</p>
          <span class="risk-tag" :class="s.risk">{{ s.risk }}</span>
        </div>
      </div>

      <button v-if="!session" class="btn-start" @click="startSession" :disabled="!selectedSuspect || starting">
        {{ starting ? 'ESTABLISHING CONNECTION...' : 'BEGIN INTERROGATION →' }}
      </button>

      <!-- Chat interface -->
      <div class="chat-container" v-if="session">
        <div class="chat-header">
          <div class="session-info">
            <span class="live-dot" />
            <span class="live-label">LIVE</span>
            <span class="session-suspect">Interviewing: {{ session.suspect }}</span>
          </div>
          <div class="clue-badge" v-if="clueUnlocked">🔓 CLUE UNLOCKED — CHECK TIP INBOX</div>
          <button class="end-btn" @click="endSession">END SESSION</button>
        </div>

        <div class="messages-area" ref="messagesEl">
          <!-- System message -->
          <div class="sys-msg">
            <TypewriterText :text="`Interrogation session initiated. Subject: ${session.suspect}. Proceed with questioning.`" :speed="25" />
          </div>

          <div v-for="(msg, i) in game.interrogationMessages" :key="i" class="message" :class="msg.role">
            <div class="msg-role">{{ msg.role === 'investigator' ? 'YOU' : session.suspect.split(' ')[0].toUpperCase() }}</div>
            <div class="msg-bubble">
              <TypewriterText v-if="msg.role === 'suspect' && i === game.interrogationMessages.length - 1"
                :text="msg.content" :speed="20" />
              <span v-else>{{ msg.content }}</span>
            </div>
          </div>

          <div class="typing-indicator" v-if="thinking">
            <span/><span/><span/>
          </div>
        </div>

        <div class="input-area">
          <input
            v-model="userMessage"
            type="text"
            placeholder="TYPE YOUR QUESTION..."
            @keyup.enter="sendMessage"
            :disabled="thinking"
            class="msg-input"
          />
          <button class="send-btn" @click="sendMessage" :disabled="thinking || !userMessage.trim()">
            {{ thinking ? '...' : 'SEND ↵' }}
          </button>
        </div>

        <!-- Suggested questions -->
        <div class="suggestions">
          <p class="sug-label">SUGGESTED LINES OF QUESTIONING:</p>
          <div class="sug-pills">
            <button v-for="q in suggestions" :key="q" class="sug-pill" @click="userMessage = q" :disabled="thinking">
              {{ q }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </GameLayout>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import GameLayout from '@/components/GameLayout.vue'
import TypewriterText from '@/components/TypewriterText.vue'
import GlitchText from '@/components/GlitchText.vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const session        = ref(null)
const selectedSuspect= ref('Jipri Eipstein')
const userMessage    = ref('')
const thinking       = ref(false)
const starting       = ref(false)
const clueUnlocked   = ref(false)
const messagesEl     = ref(null)

const suspects = [
  { id:'Jipri Eipstein', initial:'JE', name:'Jipri Eipstein', role:'Primary Suspect', risk:'critical' },
  { id:'Lady Ghilaine Maxwell', initial:'GM', name:'Lady G. Maxwell', role:'Primary Recruiter', risk:'critical' },
  { id:'Senator Howard Carver', initial:'HC', name:'Sen. H. Carver', role:'U.S. Legislator', risk:'high' },
  { id:'Lord Basil Mandelborough', initial:'BM', name:'Lord B. Mandelborough', role:'Political Advisor', risk:'high' },
]

const suggestions = [
  'Where were you between 1997 and 2005?',
  'Who recruited the victims?',
  'What happened on Little St. James island?',
  'Why did the 2008 deal happen?',
  'Name your financial backers.',
  'Who else was involved?',
]

async function startSession() {
  starting.value = true
  const s = await game.startInterrogation(selectedSuspect.value)
  if (s) session.value = s
  starting.value = false
}

async function sendMessage() {
  if (!userMessage.value.trim() || thinking.value || !session.value) return
  const msg = userMessage.value.trim()
  userMessage.value = ''
  thinking.value = true
  const result = await game.sendMessage(session.value.session_id, msg)
  if (result?.clue_unlocked) clueUnlocked.value = true
  thinking.value = false
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

function endSession() {
  session.value = null
  game.interrogationMessages = []
  clueUnlocked.value = false
}
</script>

<style scoped>
.interrogation-page { padding:2rem 2.5rem; min-height:100vh; }
.eyebrow { font-size:0.62rem;letter-spacing:0.3em;color:#c0392b;margin-bottom:0.4rem; }
.page-title { font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#f0e6d3;display:block;margin-bottom:0.4rem; }
.sub { font-size:0.75rem;color:#4a4a5a;margin-bottom:2rem; }

.suspect-row { display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:1rem;margin-bottom:1.5rem; }
.suspect-card {
  background:rgba(10,10,20,0.8);border:1px solid rgba(201,162,39,0.1);
  padding:1.25rem 1rem;cursor:pointer;transition:all 0.25s;text-align:center;
}
.suspect-card:hover,.suspect-card.selected { border-color:rgba(201,162,39,0.45); }
.suspect-card.selected { background:rgba(201,162,39,0.05); }
.mugshot {
  width:64px;height:80px;background:#050508;border:1px solid rgba(201,162,39,0.15);
  margin:0 auto 0.75rem;position:relative;overflow:hidden;
  display:flex;align-items:center;justify-content:center;
}
.mugshot-lines { position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-evenly;padding:4px; }
.mshot-line { height:1px;background:rgba(201,162,39,0.06); }
.mugshot-initial { font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:900;color:rgba(201,162,39,0.3);position:relative;z-index:1; }
.suspect-name { font-size:0.78rem;color:#f0e6d3;font-weight:700;margin-bottom:0.2rem; }
.suspect-role { font-size:0.62rem;color:#4a4a5a;margin-bottom:0.5rem; }
.risk-tag { font-size:0.55rem;letter-spacing:0.12em;padding:0.15rem 0.5rem;border:1px solid; }
.risk-tag.critical { color:#c0392b;border-color:rgba(192,57,43,0.4); }
.risk-tag.high     { color:#c9a227;border-color:rgba(201,162,39,0.4); }

.btn-start {
  background:transparent;border:1px solid #c9a227;color:#c9a227;
  font-family:'Courier Prime',monospace;font-size:0.82rem;letter-spacing:0.2em;
  padding:0.9rem 2.5rem;cursor:pointer;transition:all 0.25s;margin-bottom:2rem;
}
.btn-start:hover:not(:disabled){background:#c9a227;color:#050508}
.btn-start:disabled{opacity:0.4;cursor:not-allowed}

.chat-container { background:rgba(8,8,14,0.9);border:1px solid rgba(201,162,39,0.2);display:flex;flex-direction:column;max-height:75vh; }
.chat-header { display:flex;align-items:center;gap:1rem;padding:0.85rem 1.25rem;border-bottom:1px solid rgba(201,162,39,0.1);flex-wrap:wrap; }
.live-dot { width:8px;height:8px;border-radius:50%;background:#c0392b;animation:pulse-gold 1s ease-in-out infinite; }
.live-label { font-size:0.6rem;letter-spacing:0.2em;color:#c0392b; }
.session-suspect { font-size:0.72rem;color:#4a4a5a;flex:1; }
.clue-badge { font-size:0.62rem;color:#4a9a5a;border:1px solid rgba(74,154,90,0.3);padding:0.2rem 0.6rem;letter-spacing:0.1em; }
.end-btn { background:transparent;border:1px solid rgba(192,57,43,0.3);color:#4a4a5a;font-family:'Courier Prime',monospace;font-size:0.6rem;letter-spacing:0.12em;padding:0.3rem 0.75rem;cursor:pointer;transition:all 0.2s; }
.end-btn:hover { color:#c0392b;border-color:rgba(192,57,43,0.6); }

.messages-area { flex:1;overflow-y:auto;padding:1.25rem;display:flex;flex-direction:column;gap:1rem;min-height:300px; }
.sys-msg { font-size:0.7rem;color:#2a2a3a;letter-spacing:0.1em;text-align:center;padding:0.5rem;border:1px solid rgba(255,255,255,0.03); }

.message { display:flex;flex-direction:column;gap:0.3rem;animation:fadeUp 0.3s ease; }
.message.investigator { align-items:flex-end; }
.message.suspect       { align-items:flex-start; }
.msg-role { font-size:0.58rem;letter-spacing:0.2em;color:#4a4a5a; }
.msg-bubble { max-width:75%;padding:0.75rem 1rem;font-size:0.84rem;line-height:1.65; }
.message.investigator .msg-bubble { background:rgba(201,162,39,0.08);border:1px solid rgba(201,162,39,0.2);color:#f0e6d3; }
.message.suspect .msg-bubble { background:rgba(192,57,43,0.06);border:1px solid rgba(192,57,43,0.2);color:#c8bba8;font-style:italic; }

.typing-indicator { display:flex;gap:4px;padding:0.5rem; }
.typing-indicator span { width:6px;height:6px;background:#4a4a5a;border-radius:50%;animation:pulse-gold 0.8s ease-in-out infinite; }
.typing-indicator span:nth-child(2){animation-delay:.15s}.typing-indicator span:nth-child(3){animation-delay:.3s}

.input-area { display:flex;gap:0.5rem;padding:1rem 1.25rem;border-top:1px solid rgba(201,162,39,0.08); }
.msg-input { flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(201,162,39,0.2);color:#f0e6d3;font-family:'Courier Prime',monospace;font-size:0.85rem;padding:0.65rem 1rem;outline:none;transition:border-color 0.2s; }
.msg-input:focus { border-color:rgba(201,162,39,0.5); }
.msg-input::placeholder { color:#2a2a3a; }
.send-btn { background:#c9a227;border:none;color:#050508;font-family:'Courier Prime',monospace;font-size:0.72rem;letter-spacing:0.15em;padding:0 1.25rem;cursor:pointer;transition:all 0.2s;font-weight:700; }
.send-btn:hover:not(:disabled){background:#f0c843}
.send-btn:disabled{opacity:0.35;cursor:not-allowed}

.suggestions { padding:0.75rem 1.25rem 1rem;border-top:1px solid rgba(255,255,255,0.03); }
.sug-label { font-size:0.58rem;letter-spacing:0.15em;color:#2a2a3a;margin-bottom:0.5rem; }
.sug-pills { display:flex;flex-wrap:wrap;gap:0.4rem; }
.sug-pill { background:transparent;border:1px solid rgba(255,255,255,0.05);color:#4a4a5a;font-family:'Courier Prime',monospace;font-size:0.62rem;padding:0.3rem 0.75rem;cursor:pointer;transition:all 0.2s; }
.sug-pill:hover:not(:disabled){border-color:rgba(201,162,39,0.3);color:#c9a227}
</style>
