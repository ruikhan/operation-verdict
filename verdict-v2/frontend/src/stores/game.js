import { defineStore } from 'pinia'
import api from '@/api'

export const useGameStore = defineStore('game', {
  state: () => ({
    files: [], progress: null, leaderboard: [],
    tips: [], corruption: [], timeline: [],
    interrogationSession: null, interrogationMessages: [],
    loading: false, error: null,
    timerInterval: null,
  }),

  getters: {
    convictionPercent: s => Math.min(100, Math.round(s.progress?.conviction_strength ?? 0)),
    filesReviewed:     s => s.progress?.files_reviewed ?? 0,
    totalFiles:        s => s.progress?.total_files ?? 0,
    verdictReached:    s => s.progress?.verdict_reached ?? false,
    timeRemaining:     s => s.progress?.time_remaining_secs ?? 7200,
    score:             s => s.progress?.score ?? 0,
    unreadTips:        s => s.tips.filter(t => !t.is_read).length,
    unlockedFiles:     s => s.files.filter(f => f.is_unlocked),
    lockedFiles:       s => s.files.filter(f => !f.is_unlocked),
    activeCorruption:  s => s.corruption.filter(c => !c.is_resolved),
  },

  actions: {
    async fetchAll() {
      this.loading = true
      await Promise.all([
        this.fetchFiles(), this.fetchProgress(),
        this.fetchTips(), this.fetchCorruption(), this.fetchTimeline(),
      ])
      this.loading = false
    },

    async fetchFiles() {
      try { const { data } = await api.get('/files/'); this.files = data } catch (_) {}
    },
    async fetchProgress() {
      try { const { data } = await api.get('/progress/'); this.progress = data } catch (_) {}
    },
    async fetchLeaderboard() {
      try { const { data } = await api.get('/leaderboard/'); this.leaderboard = data } catch (_) {}
    },
    async fetchTips() {
      try { const { data } = await api.get('/tips/'); this.tips = data } catch (_) {}
    },
    async fetchCorruption() {
      try { const { data } = await api.get('/corruption/'); this.corruption = data } catch (_) {}
    },
    async fetchTimeline() {
      try { const { data } = await api.get('/timeline/'); this.timeline = data } catch (_) {}
    },

    async reviewFile(fileId, notes = '') {
      try {
        const { data } = await api.post(`/files/${fileId}/review/`, { notes })
        this.progress = data.progress
        const idx = this.files.findIndex(f => f.file_id === fileId)
        if (idx !== -1) this.files[idx] = { ...this.files[idx], is_reviewed: true }
        await this.fetchFiles()
        return data
      } catch (e) { this.error = e.response?.data; return null }
    },

    async solveCipher(fileId, answer) {
      try {
        const { data } = await api.post(`/files/${fileId}/cipher/`, { answer })
        if (data.correct) await this.fetchProgress()
        return data
      } catch (e) { return { correct: false, detail: 'Error submitting cipher.' } }
    },

    async startInterrogation(suspect = 'Jipri Eipstein') {
      try {
        const { data } = await api.post('/interrogation/start/', { suspect })
        this.interrogationSession = data
        this.interrogationMessages = []
        return data
      } catch (e) { return null }
    },

    async sendMessage(sessionId, message) {
      if (!sessionId) { console.error('sendMessage: sessionId is undefined'); return null }
      try {
        const { data } = await api.post(`/interrogation/${sessionId}/message/`, { message })
        this.interrogationMessages.push({ role: 'investigator', content: message, created_at: new Date().toISOString() })
        this.interrogationMessages.push({ role: 'suspect', content: data.reply, created_at: new Date().toISOString() })
        if (data.clue_unlocked) await this.fetchProgress()
        return data
      } catch (e) { return null }
    },

    async readTip(tipId) {
      try {
        await api.post(`/tips/${tipId}/read/`)
        const idx = this.tips.findIndex(t => t.id === tipId)
        if (idx !== -1) this.tips[idx] = { ...this.tips[idx], is_read: true }
        await this.fetchProgress()
      } catch (_) {}
    },

    async resolveCorruption(eventId, code) {
      try {
        const { data } = await api.post(`/corruption/${eventId}/resolve/`, { code })
        if (data.correct) {
          const idx = this.corruption.findIndex(c => c.id === eventId)
          if (idx !== -1) this.corruption[idx] = { ...this.corruption[idx], is_resolved: true }
          await this.fetchProgress()
        }
        return data
      } catch (e) { return { correct: false, detail: 'Server error.' } }
    },

    startTimer() {
      if (this.timerInterval) return
      this.timerInterval = setInterval(async () => {
        if (!this.progress) return
        const secs = Math.max(0, (this.progress.time_remaining_secs ?? 7200) - 5)
        this.progress = { ...this.progress, time_remaining_secs: secs }
        if (secs % 30 === 0) {
          await api.post('/timer/update/', { time_remaining_secs: secs })
        }
        if (secs === 0) this.stopTimer()
      }, 5000)
    },

    stopTimer() {
      if (this.timerInterval) { clearInterval(this.timerInterval); this.timerInterval = null }
    },

    async syncTimer() {
      if (!this.progress) return
      await api.post('/timer/update/', { time_remaining_secs: this.progress.time_remaining_secs })
    },
  },
})
