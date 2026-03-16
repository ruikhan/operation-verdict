const CACHE_NAME = 'operation-verdict-v3'
const STATIC_ASSETS = ['/', '/manifest.json']

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  )
  self.skipWaiting()
})

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url)

  // Only handle http/https — ignore chrome-extension and other schemes
  if (!url.protocol.startsWith('http')) return

  // Always network-first for API calls
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() =>
        new Response('{"error":"offline"}', { headers: { 'Content-Type': 'application/json' } })
      )
    )
    return
  }

  // Cache-first for static assets
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached
      return fetch(e.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') return response
        const clone = response.clone()
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone))
        return response
      }).catch(() => caches.match('/'))
    })
  )
})
