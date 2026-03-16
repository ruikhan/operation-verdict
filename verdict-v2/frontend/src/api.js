import axios from 'axios'

// On Render, frontend and backend are separate services.
// VITE_API_URL is set to the Django service URL in Render env vars.
const baseURL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api'

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let failedQueue  = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(p => error ? p.reject(error) : p.resolve(token))
  failedQueue = []
}

api.interceptors.response.use(
  res => res,
  async error => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => failedQueue.push({ resolve, reject }))
          .then(token => { original.headers.Authorization = `Bearer ${token}`; return api(original) })
      }
      original._retry = true; isRefreshing = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) { localStorage.clear(); window.location.href = '/login'; return Promise.reject(error) }
      try {
        const { data } = await axios.post(`${baseURL}/auth/token/refresh/`, { refresh })
        const newAccess = data.access
        localStorage.setItem('access_token', newAccess)
        processQueue(null, newAccess)
        original.headers.Authorization = `Bearer ${newAccess}`
        return api(original)
      } catch (err) {
        processQueue(err, null); localStorage.clear(); window.location.href = '/login'
        return Promise.reject(err)
      } finally { isRefreshing = false }
    }
    return Promise.reject(error)
  }
)

export default api
