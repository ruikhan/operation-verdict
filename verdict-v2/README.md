# ⚖️ Operation Verdict v2
### Django + Vue.js + PostgreSQL · Docker · PWA · Render Deployment

---

## 🚀 Local Development

```bash
cd operation-verdict-v2
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"  # Windows only
docker compose down -v    # wipe old DB if upgrading from v1
docker compose up --build
```

Open **http://localhost**

---

## 📱 PWA — Install on Mobile

The app is a **Progressive Web App** — fully installable on any device.

**iOS (iPhone/iPad):**
1. Open **http://your-render-url** in Safari
2. Tap the Share button (box with arrow)
3. Tap **"Add to Home Screen"**
4. Tap **Add** — it installs like a real app

**Android:**
1. Open in Chrome
2. Tap the three-dot menu
3. Tap **"Add to Home Screen"** or **"Install App"**

**Desktop (Chrome/Edge):**
1. Look for the install icon in the address bar
2. Click **Install**

---

## 🌐 Deploy to Render (Live Server)

### Prerequisites
- Push the project to a **GitHub repository**
- Have a **Render account** at render.com

### Option A — One-Click Blueprint (Recommended)

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Operation Verdict v2"
git remote add origin https://github.com/YOUR_USERNAME/operation-verdict.git
git push -u origin main
```

2. Go to **render.com → Dashboard → New → Blueprint**
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create all 3 services automatically:
   - `operation-verdict-db` (PostgreSQL)
   - `operation-verdict-backend` (Django)
   - `operation-verdict-frontend` (Vue static site)

5. Click **Apply** — deployment takes ~5 minutes

### Option B — Manual Setup

**Step 1: Create PostgreSQL Database**
- Render Dashboard → New → PostgreSQL
- Name: `operation-verdict-db`
- Plan: Free
- Copy the **Internal Database URL**

**Step 2: Deploy Django Backend**
- Render Dashboard → New → Web Service
- Connect GitHub repo
- **Root Directory:** `backend`
- **Runtime:** Python 3
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
- **Environment Variables:**

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `config.settings_prod` |
| `SECRET_KEY` | (click Generate) |
| `DATABASE_URL` | (paste from Step 1) |
| `ALLOWED_HOSTS` | `your-backend-name.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend-name.onrender.com` |
| `ANTHROPIC_API_KEY` | (optional — for live AI interrogation) |

**Step 3: Deploy Vue Frontend**
- Render Dashboard → New → Static Site
- Connect same GitHub repo
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `dist`
- **Environment Variables:**

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-backend-name.onrender.com` |

- **Rewrite Rules:**
  - Source: `/*` → Destination: `/index.html` (for SPA routing)

---

## ⚠️ Render Free Tier Notes

| Service | Free Tier Behaviour |
|---------|-------------------|
| Backend (Web Service) | **Spins down after 15 min inactivity.** First request after sleep takes ~30s to wake up. |
| Frontend (Static Site) | Always on. No spin-down. |
| Database (PostgreSQL) | Free for **90 days**, then $7/month. |

**To avoid cold starts:** Upgrade backend to Starter plan ($7/month) or use an uptime monitor like UptimeRobot to ping the backend every 10 minutes.

---

## 🎮 Game Features (v2)

| Feature | Description |
|---------|-------------|
| **10 Victim Files** | Tiered unlock system — files unlock as you review more |
| **Cipher Puzzles** | Encoded messages hidden inside evidence files |
| **AI Interrogation** | Chat with suspects using Claude API |
| **Anonymous Tips** | Tip inbox unlocks progressively |
| **Corruption System** | Some files blocked by corrupt officials — find bypass codes |
| **Case Timeline** | 16 chronological events, some locked |
| **Evidence Board** | String-and-pins connection map |
| **Leaderboard** | Global investigator rankings |
| **2-Hour Timer** | Countdown pressure mechanic with score bonus |
| **Verdict Room** | Courtroom finale with full case stats |

---

## 🗂 Project Structure

```
operation-verdict-v2/
├── render.yaml                    ← One-click Render deployment
├── .gitignore
├── docker-compose.yml             ← Local development
│
├── backend/
│   ├── build.sh                   ← Render build script
│   ├── requirements.txt
│   ├── config/
│   │   ├── settings.py            ← Development settings
│   │   └── settings_prod.py       ← Production (Render) settings
│   └── api/
│       ├── models.py              ← 11 models
│       ├── views.py               ← 20+ endpoints
│       └── management/commands/seed_data.py
│
└── frontend/
    ├── public/
    │   ├── manifest.json          ← PWA manifest
    │   ├── sw.js                  ← Service worker
    │   └── icons/                 ← App icons
    └── src/
        ├── components/
        │   ├── GameLayout.vue     ← Sidebar (desktop) + Bottom nav (mobile)
        │   ├── TypewriterText.vue
        │   └── GlitchText.vue
        └── views/                 ← 12 screens
```
