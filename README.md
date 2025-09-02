# Mood Journal (SDG 3) – AI-Powered Emotion Tracker

An AI-assisted mood journaling app for SDG 3 (Good Health and Well-being). Users write journal entries, get instant emotion analysis, view mood trends, and optionally subscribe via IntaSend (M-Pesa, Cards). Built with Flask, Supabase, and Hugging Face.

---

## ✨ Features

- Real-time emotion analysis (Happy/Sad/Angry/Neutral, etc.) with confidence scores
- Clean UI with tabs: New Entry, Recent Entries, Premium, Mood Distribution, Mood Trends
- Charts (Chart.js) for distribution and trends
- Local login (name + email) with welcome banner
- Dark mode with persistent preference
- Supabase (PostgreSQL) for entries and payments
- IntaSend integration ready for monetization

---

#
## 🛠️ Tech Stack

- Frontend: HTML, CSS, JS, Chart.js
- Backend: Flask, Flask-CORS
- AI: Hugging Face Inference API
- DB: Supabase (PostgreSQL)
- Payments: IntaSend

---

## 📜 Build Summary

- Separated HTML/CSS/JS, added tabbed navigation and dark mode
- Instant emotion analysis and confidence scores
- Supabase CRUD for entries and stats
- IntaSend payment initiation endpoints
- Simple login and welcome banner (localStorage)
- Deployment and secret-handling guidance

---

Built for the Vibe Coding Hackathon • SDG 3: Good Health
