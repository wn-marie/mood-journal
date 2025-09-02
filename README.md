# Mood Journal (SDG 3) – AI-Powered Emotion Tracker

An AI-assisted mood journaling app for SDG 3 (Good Health and Well-being). Users write journal entries, get instant emotion analysis, view mood trends, and optionally subscribe via IntaSend (M-Pesa, Cards). Built with Flask, Supabase, and Hugging Face.

## ✨ Features
- Real-time emotion analysis (Happy/Sad/Angry/Neutral, etc.) with confidence scores
- Clean UI with tabs: New Entry, Recent Entries, Premium, Mood Distribution, Mood Trends
- Charts (Chart.js) for distribution and trends
- Local login (name + email) with welcome banner
- Dark mode with persistent preference
- Supabase (PostgreSQL) for entries and payments
- IntaSend integration ready for monetization

## 🧭 Quick Start
1) Clone and enter the project
```bash
git clone https://github.com/wn-marie/mood-journal.git
cd mood-journal
```
2) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```
3) Install dependencies
```bash
pip install -r requirements.txt
```
4) Copy env example and fill values
```bash
copy env_example.txt .env   # Windows
```
Edit `.env` (keep it private, never commit):
```
SECRET_KEY=replace-with-a-random-string
HUGGINGFACE_API_KEY=hf_xxx
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
INTASEND_API_KEY=...
INTASEND_PUBLISHABLE_KEY=...
```
5) Run locally
```bash
python app.py
# Open http://localhost:5000
```

## 🗃️ Database (Supabase)
- Create a Supabase project → get `SUPABASE_URL` and `SUPABASE_ANON_KEY`
- Create tables:
```sql
-- journal_entries
create table if not exists journal_entries (
  id bigint generated always as identity primary key,
  content text,
  emotion_label text,
  sentiment_score double precision,
  ai_provider text,
  detailed_analysis text,
  created_at timestamp with time zone default now()
);

-- payments
create table if not exists payments (
  id bigint generated always as identity primary key,
  plan_type text,
  amount numeric,
  status text,
  intasend_payment_id text,
  created_at timestamp with time zone default now()
);
```

## 🤖 AI Emotion Analysis
- Primary: Hugging Face Inference API
- We try a rich emotion model first, then fall back to sentiment models
- Backend endpoint: `POST /api/ai/analyze` returns `{ emotion_label, sentiment_score, detailed_analysis }`

## 💳 Monetization (IntaSend)
- Ready to accept M-Pesa and cards
- Set `INTASEND_API_KEY` and `INTASEND_PUBLISHABLE_KEY` in `.env`
- Endpoint: `POST /api/payment/initiate` (returns a payment URL in a production setup)

## 🌐 Deploy (Render - quickest)
1) Ensure these files exist:
```
Procfile       # contains:  web: gunicorn app:app
requirements.txt
```
2) Push to GitHub (without secrets)
```bash
git add .
git commit -m "deploy: prepare"
git push origin main
```
3) Render → New Web Service → Connect repo
- Start command: `gunicorn app:app`
- Add Environment Variables from `.env`
- Deploy → copy the live URL

## 🔐 Secrets Policy
- Keep `.env` in the project root; do NOT commit it
- `.gitignore` includes:
```
.env
*.env
.env.*
```
- If a secret was ever committed, rotate it in the provider and clean history (e.g., `git filter-repo`)

## 🧪 Quick API Test
```bash
curl -X POST http://localhost:5000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"content":"I feel very happy today!"}'
```

## 🚑 Troubleshooting
- Flask not found: activate venv and `pip install -r requirements.txt`
- Supabase `proxy` error: pin versions
```bash
pip uninstall -y httpx httpcore gotrue supabase
pip install "httpx==0.28.1" "httpcore==1.0.5" "gotrue>=2.6.1" "supabase>=2.4.0"
```
- websockets module error:
```bash
pip install -U "websockets>=12.0" websocket-client
```

## 🛠️ Tech Stack
- Frontend: HTML, CSS, JS, Chart.js
- Backend: Flask, Flask-CORS
- AI: Hugging Face Inference API
- DB: Supabase (PostgreSQL)
- Payments: IntaSend

## 📜 Build Summary (What we did)
- Separated HTML/CSS/JS, added tabbed navigation and dark mode
- Implemented instant emotion analysis and confidence scores
- Wired Supabase CRUD for entries and stats
- Added IntaSend payment initiation endpoints
- Added simple login and welcome banner (localStorage)
- Wrote deployment and secret-handling guidance

---
Built for the Vibe Coding Hackathon • SDG 3: Good Health and Well-being
# mood-journal