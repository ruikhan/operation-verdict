<template>
  <div class="page">
    <div class="noise" />

    <div class="container">
      <div class="logo-block">
        <p class="eyebrow">CLASSIFIED OPERATION</p>
        <h1 class="title">OPERATION<br><span class="gold">VERDICT</span></h1>
        <div class="divider"><span>INVESTIGATOR ACCESS</span></div>
      </div>

      <form class="form" @submit.prevent="submit">
        <div class="field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="investigator_42" required autocomplete="username" />
        </div>

        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="••••••••" required autocomplete="current-password" />
        </div>

        <div v-if="errorMsg" class="error-box">▸ {{ errorMsg }}</div>

        <button type="submit" :disabled="auth.loading" class="btn-submit">
          <span v-if="auth.loading">AUTHENTICATING…</span>
          <span v-else>ACCESS SYSTEM →</span>
        </button>

        <p class="register-link">
          New investigator?
          <RouterLink to="/register">Create profile</RouterLink>
        </p>
      </form>

      <p class="footer-note">
        ⚠ This system contains classified evidence materials.<br>
        Unauthorized access is strictly prohibited.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router   = useRouter()
const auth     = useAuthStore()
const username = ref('')
const password = ref('')

const errorMsg = computed(() => {
  if (!auth.error) return ''
  const e = auth.error
  if (e.detail) return e.detail
  if (e.non_field_errors) return e.non_field_errors[0]
  return 'Authentication failed. Check credentials.'
})

async function submit() {
  const ok = await auth.login(username.value, password.value)
  if (ok) {
    if (!auth.termsAccepted)   return router.push('/terms')
    if (!auth.cinematicViewed) return router.push('/briefing')
    router.push('/dashboard')
  }
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
  width: 100%; max-width: 420px;
  animation: fadeUp 0.6s ease forwards;
}

@keyframes fadeUp {
  from { opacity:0; transform: translateY(20px); }
  to   { opacity:1; transform: translateY(0); }
}

.logo-block { text-align: center; margin-bottom: 2.5rem; }

.eyebrow {
  font-family: 'Courier Prime', monospace;
  font-size: 0.7rem; letter-spacing: 0.3em; color: #c9a227; margin-bottom: 0.75rem;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 8vw, 3.8rem);
  font-weight: 900; line-height: 1; color: #f0e6d3; margin-bottom: 1.5rem;
}

.gold { color: #c9a227; }

.divider {
  display: flex; align-items: center; gap: 1rem;
  color: #2a2a3a; font-size: 0.65rem; letter-spacing: 0.2em;
}
.divider::before, .divider::after {
  content: ''; flex: 1; height: 1px; background: rgba(201,162,39,0.15);
}
.divider span { color: #4a4a5a; white-space: nowrap; }

.form {
  background: rgba(13,13,21,0.9);
  border: 1px solid rgba(201,162,39,0.2);
  padding: 2rem;
  display: flex; flex-direction: column; gap: 1.25rem;
}

.field { display: flex; flex-direction: column; gap: 0.4rem; }

label {
  font-size: 0.65rem; letter-spacing: 0.2em;
  text-transform: uppercase; color: #c9a227;
}

input {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(201,162,39,0.25);
  color: #f0e6d3; font-family: 'Courier Prime', monospace;
  font-size: 0.88rem; padding: 0.65rem 0.85rem;
  outline: none; width: 100%; transition: border-color 0.2s;
}
input:focus     { border-color: rgba(201,162,39,0.6); }
input::placeholder { color: #2a2a3a; }

.error-box {
  background: rgba(192,57,43,0.12);
  border: 1px solid rgba(192,57,43,0.35);
  padding: 0.65rem 1rem;
  font-size: 0.78rem; color: #e74c3c;
}

.btn-submit {
  background: transparent; border: 1px solid #c9a227;
  color: #c9a227; font-family: 'Courier Prime', monospace;
  font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase;
  padding: 0.9rem; cursor: pointer; transition: all 0.25s; width: 100%;
}
.btn-submit:hover:not(:disabled) { background: #c9a227; color: #050508; }
.btn-submit:disabled              { opacity: 0.4; cursor: not-allowed; }

.register-link { text-align: center; font-size: 0.78rem; color: #4a4a5a; }
.register-link a { color: #c9a227; text-decoration: none; }
.register-link a:hover { text-decoration: underline; }

.footer-note {
  margin-top: 2rem; text-align: center;
  font-size: 0.65rem; line-height: 1.7;
  color: #2a2a3a; letter-spacing: 0.05em;
}
</style>
