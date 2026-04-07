# 🏗️ Mansuri Admin Portal

Internal admin system for **Mansuri Enterprises** and **Aman Stone Crusher**.

## Quick Start

**Read `DEPLOY_GUIDE.md` for the full step-by-step deployment guide.**

| Service | Tech | Hosted on |
|---|---|---|
| Backend API | FastAPI (Python) | Railway |
| Frontend UI | Streamlit (Python) | Railway |
| Database | PostgreSQL | Supabase (Free) |

## Default Login
- Username: `admin`
- Password: set by you in Railway environment variables

## Project Structure
```
mansuri-admin/
├── backend/              ← FastAPI REST API
│   ├── app/
│   │   ├── main.py       ← entry point
│   │   ├── core/         ← config, security, dependencies
│   │   ├── database/     ← DB connection setup
│   │   ├── models/       ← database tables
│   │   ├── schemas/      ← data validation
│   │   ├── routes/       ← API endpoints
│   │   └── services/     ← business logic
│   ├── backup.py         ← run locally to backup database
│   ├── requirements.txt
│   ├── Procfile          ← tells Railway how to start backend
│   └── railway.json
├── frontend/             ← Streamlit UI
│   ├── app.py            ← entry point + login + navigation
│   ├── pages/            ← dashboard, inventory, orders, admin
│   ├── utils/            ← api.py (HTTP calls), auth.py (session)
│   ├── .streamlit/       ← Streamlit config for production
│   ├── requirements.txt
│   ├── Procfile          ← tells Railway how to start frontend
│   └── railway.json
├── .gitignore            ← keeps .env files out of GitHub
├── .env.example          ← template for local development
└── DEPLOY_GUIDE.md       ← complete deployment guide
```
