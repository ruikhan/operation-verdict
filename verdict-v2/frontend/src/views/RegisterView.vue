<template>
  <div class="page">
    <div class="noise" />

    <div class="container">
      <!-- Logo -->
      <div class="logo-block">
        <p class="eyebrow">CLASSIFIED OPERATION</p>
        <h1 class="title">OPERATION<br><span class="gold">VERDICT</span></h1>
        <p class="subtitle">Investigator Registration</p>
      </div>

      <!-- Form -->
      <form class="form" @submit.prevent="submit">
        <div class="row-2">
          <div class="field">
            <label>First Name</label>
            <input v-model="form.first_name" type="text" placeholder="Jane" required />
          </div>
          <div class="field">
            <label>Last Name</label>
            <input v-model="form.last_name" type="text" placeholder="Doe" required />
          </div>
        </div>

        <div class="field">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="investigator_42" required autocomplete="username" />
        </div>

        <div class="field">
          <label>Email Address</label>
          <input v-model="form.email" type="email" placeholder="jane@example.com" required />
        </div>

        <div class="row-3">
          <div class="field">
            <label>Age</label>
            <input v-model.number="form.age" type="number" min="18" max="120" placeholder="25" required />
          </div>
          <div class="field">
            <label>Sex</label>
            <select v-model="form.sex" required>
              <option value="" disabled>Select</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
              <option value="N">Prefer not to say</option>
            </select>
          </div>
          <div class="field">
            <label>Phone Number</label>
            <input v-model="form.phone_number" type="tel" placeholder="+1 555 0100" required />
          </div>
        </div>

        <div class="row-2">
          <div class="field">
            <label>Password</label>
            <input v-model="form.password" type="password" placeholder="min. 8 characters" required autocomplete="new-password" />
          </div>
          <div class="field">
            <label>Confirm Password</label>
            <input v-model="form.confirm_password" type="password" placeholder="repeat password" required autocomplete="new-password" />
          </div>
        </div>

        <!-- Errors -->
        <div v-if="errors.length" class="errors">
          <p v-for="(e, i) in errors" :key="i" class="error-line">▸ {{ e }}</p>
        </div>

        <button type="submit" :disabled="auth.loading" class="btn-submit">
          <span v-if="auth.loading">CREATING PROFILE…</span>
          <span v-else>REGISTER AS INVESTIGATOR →</span>
        </button>

        <p class="login-link">
          Already registered?
          <RouterLink to="/login">Sign in</RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const form = ref({
  first_name: '', last_name: '', username: '', email: '',
  age: '', sex: '', phone_number: '',
  password: '', confirm_password: '',
})

const errors = computed(() => {
  if (!auth.error) return []
  const e = auth.error
  if (typeof e === 'string') return [e]
  return Object.entries(e).flatMap(([field, msgs]) =>
    Array.isArray(msgs) ? msgs.map(m => `${field}: ${m}`) : [`${field}: ${msgs}`]
  )
})

async function submit() {
  const ok = await auth.register(form.value)
  if (ok) {
    await auth.login(form.value.username, form.value.password)
    router.push('/terms')
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #050508;
  padding: 2rem 1rem;
  position: relative;
}

.noise {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  opacity: 0.4;
}

.container {
  position: relative; z-index: 1;
  width: 100%; max-width: 640px;
  animation: fadeUp 0.6s ease forwards;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.logo-block { text-align: center; margin-bottom: 2.5rem; }

.eyebrow {
  font-family: 'Courier Prime', monospace;
  font-size: 0.7rem; letter-spacing: 0.3em;
  color: #c9a227; margin-bottom: 0.75rem;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 6vw, 3.2rem);
  font-weight: 900; line-height: 1;
  color: #f0e6d3; margin-bottom: 0.5rem;
}

.gold { color: #c9a227; }

.subtitle {
  font-family: 'Courier Prime', monospace;
  font-size: 0.78rem; letter-spacing: 0.2em;
  color: #4a4a5a;
}

.form {
  background: rgba(13,13,21,0.9);
  border: 1px solid rgba(201,162,39,0.2);
  padding: 2rem;
  display: flex; flex-direction: column; gap: 1.25rem;
}

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.row-3 { display: grid; grid-template-columns: 80px 1fr 1fr; gap: 1rem; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }

label {
  font-size: 0.65rem; letter-spacing: 0.2em;
  text-transform: uppercase; color: #c9a227;
}

input, select {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(201,162,39,0.25);
  color: #f0e6d3;
  font-family: 'Courier Prime', monospace;
  font-size: 0.88rem; padding: 0.6rem 0.85rem;
  outline: none; width: 100%;
  transition: border-color 0.2s;
}

input:focus, select:focus { border-color: rgba(201,162,39,0.6); }
input::placeholder         { color: #2a2a3a; }
select option              { background: #0d0d15; }

.errors {
  background: rgba(192,57,43,0.12);
  border: 1px solid rgba(192,57,43,0.35);
  padding: 0.75rem 1rem;
}

.error-line {
  font-size: 0.78rem; color: #e74c3c;
  line-height: 1.6;
}

.btn-submit {
  background: transparent;
  border: 1px solid #c9a227;
  color: #c9a227;
  font-family: 'Courier Prime', monospace;
  font-size: 0.8rem; letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 0.9rem; cursor: pointer;
  transition: all 0.25s; width: 100%;
}

.btn-submit:hover:not(:disabled) { background: #c9a227; color: #050508; }
.btn-submit:disabled              { opacity: 0.4; cursor: not-allowed; }

.login-link {
  text-align: center;
  font-size: 0.78rem; color: #4a4a5a;
}

.login-link a { color: #c9a227; text-decoration: none; }
.login-link a:hover { text-decoration: underline; }

@media (max-width: 540px) {
  .row-2, .row-3 { grid-template-columns: 1fr; }
  .form { padding: 1.5rem; }
}
</style>
