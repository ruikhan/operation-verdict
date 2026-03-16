import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    player:      JSON.parse(localStorage.getItem('player') || 'null'),
    accessToken: localStorage.getItem('access_token') || null,
    loading: false, error: null,
  }),
  getters: {
    isLoggedIn:      s => !!s.accessToken,
    termsAccepted:   s => s.player?.terms_accepted ?? false,
    cinematicViewed: s => s.player?.cinematic_viewed ?? false,
    displayName:     s => s.player ? `${s.player.first_name} ${s.player.last_name}`.trim() || s.player.username : '',
    username:        s => s.player?.username || '',
  },
  actions: {
    async register(payload) {
      this.loading = true; this.error = null
      try { await api.post('/auth/register/', payload); return true }
      catch (e) { this.error = e.response?.data || { detail: 'Registration failed.' }; return false }
      finally { this.loading = false }
    },
    async login(username, password) {
      this.loading = true; this.error = null
      try {
        const { data } = await api.post('/auth/token/', { username, password })
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        this.accessToken = data.access
        await this.fetchProfile()
        return true
      } catch (e) { this.error = e.response?.data || { detail: 'Login failed.' }; return false }
      finally { this.loading = false }
    },
    async fetchProfile() {
      try {
        const { data } = await api.get('/player/profile/')
        this.player = data
        localStorage.setItem('player', JSON.stringify(data))
      } catch (_) {}
    },
    async acceptTerms() {
      try {
        await api.post('/player/accept-terms/', { accepted: true })
        this.player = { ...this.player, terms_accepted: true }
        localStorage.setItem('player', JSON.stringify(this.player))
        return true
      } catch (e) { this.error = e.response?.data; return false }
    },
    async markCinematicViewed() {
      try {
        await api.post('/player/cinematic-complete/')
        this.player = { ...this.player, cinematic_viewed: true }
        localStorage.setItem('player', JSON.stringify(this.player))
      } catch (_) {}
    },
    logout() {
      this.player = null; this.accessToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('player')
    },
  },
})
