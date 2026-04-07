# 🚀 Complete Deployment Guide — Mansuri Admin Portal
## For Complete Beginners | Railway + Supabase (Free DB + Auto Backups)

---

## 📋 What You Will End Up With

| What | Where | Cost |
|---|---|---|
| **Backend API** (FastAPI) | Railway | ~$3/month |
| **Frontend UI** (Streamlit) | Railway | ~$3/month |
| **Database** (PostgreSQL) | Supabase | FREE forever |
| **Auto Backups** (7 days) | Supabase | FREE |
| **TOTAL** | | ~$5–6/month |

---

## 🗺️ Overview of Steps

```
STEP 1 → Create Supabase account + database  (5 min)
STEP 2 → Push code to GitHub                 (5 min)
STEP 3 → Create Railway account              (2 min)
STEP 4 → Deploy Backend on Railway           (5 min)
STEP 5 → Deploy Frontend on Railway          (5 min)
STEP 6 → Open the app and log in             (1 min)
STEP 7 → Set up backups                      (3 min)
```

---

---

# STEP 1 — Create Supabase Database (FREE)

Supabase gives you a free PostgreSQL database with automatic daily backups.

## 1.1 — Create account

1. Open browser → go to **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with your **GitHub account** (easiest)

## 1.2 — Create a new project

1. Click **"New project"**
2. Fill in:
   - **Name:** `mansuri-admin`
   - **Database Password:** create a strong password
     ⚠️ SAVE THIS PASSWORD — you will need it in Step 4
   - **Region:** choose the closest to you
     (e.g. "South Asia (Mumbai)" or "Europe West")
3. Click **"Create new project"**
4. Wait 1–2 minutes for it to set up ☕

## 1.3 — Get your connection string

This is the address your app uses to connect to the database.

1. In your Supabase project, click **"Settings"** (gear icon, bottom left)
2. Click **"Database"** in the left menu
3. Scroll down to **"Connection string"**
4. Click the tab that says **"URI"**
5. You will see something like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefgh.supabase.co:5432/postgres
   ```
6. Click **"Copy"**
7. **Replace `[YOUR-PASSWORD]`** with the password you created in step 1.2
8. Save this string somewhere — you need it in Step 4

> 💡 It should look like:
> `postgresql://postgres:MyPassword123@db.xyzxyzxyz.supabase.co:5432/postgres`

---

---

# STEP 2 — Push Code to GitHub

You already have the repo at: https://github.com/Imajaj/mansuri-admin

## 2.1 — Open Terminal on your Mac

Press `Cmd + Space`, type `Terminal`, press Enter.

## 2.2 — Navigate to the project folder

```bash
# Replace the path below with wherever you saved the project
cd "/Users/ajaj/Documents/Documents - Ajaj's MacBook Pro/work/mansuri_admin/mansuri-admin"
```

## 2.3 — Set up Git and push

Run these commands ONE BY ONE:

```bash
# Check git is initialized
git status

# If you see "not a git repository", run this first:
git init

# Add all files
git add .

# Save a snapshot (commit)
git commit -m "setup: Railway + Supabase deployment"

# Connect to your GitHub repo (only needed first time)
git remote add origin https://github.com/Imajaj/mansuri-admin.git

# If you already added the remote and get an error, run this instead:
git remote set-url origin https://github.com/Imajaj/mansuri-admin.git

# Push to GitHub
git push -u origin main

# If it asks for GitHub username/password:
# Username: Imajaj
# Password: use a GitHub Personal Access Token (not your password)
# Create one at: https://github.com/settings/tokens → "Generate new token (classic)"
# Tick "repo" permission → Generate → copy and use as password
```

## 2.4 — Verify it worked

1. Go to **https://github.com/Imajaj/mansuri-admin**
2. You should see all your files listed there
3. Make sure you do NOT see a `.env` file (it's in .gitignore, so it won't appear)

---

---

# STEP 3 — Create Railway Account

Railway hosts your backend and frontend.

1. Go to **https://railway.app**
2. Click **"Login"**
3. Click **"Login with GitHub"**
4. Authorize Railway to access your GitHub
5. You're in! Railway will show you an empty dashboard.

> 💡 Railway gives you $5 free credit to start with.
> After that it's ~$5–6/month total for both services.

---

---

# STEP 4 — Deploy the Backend (FastAPI)

## 4.1 — Create a new project on Railway

1. In Railway dashboard, click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. You'll see a list of your GitHub repos
4. Click on **"mansuri-admin"**

## 4.2 — Set the root directory to backend

Railway will try to deploy the whole repo. We need to tell it to use only the `backend` folder.

1. After selecting the repo, Railway creates a service
2. Click on the service (it might say "mansuri-admin")
3. Go to **"Settings"** tab
4. Find **"Root Directory"**
5. Type: `backend`
6. Press Enter / Save

## 4.3 — Add environment variables

This is where you paste your secret settings.

1. Click the **"Variables"** tab
2. Click **"New Variable"** for EACH of the following:

   Add them one by one:

   | Variable Name | Value |
   |---|---|
   | `DATABASE_URL` | paste your Supabase URI from Step 1.3 |
   | `SECRET_KEY` | any long random string (e.g. `mYs3cr3tK3y-mansuri-2026-xkq9`) |
   | `ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` |
   | `FIRST_ADMIN_USERNAME` | `admin` |
   | `FIRST_ADMIN_PASSWORD` | choose a strong password (e.g. `Mansuri@2026`) |
   | `FIRST_ADMIN_EMAIL` | your email address |

   > ⚠️ IMPORTANT: Save the admin password somewhere — you need it to log in!

3. After adding all variables, Railway will automatically redeploy.

## 4.4 — Wait for deployment

1. Click the **"Deployments"** tab
2. You'll see a deployment in progress (spinning circle)
3. Wait 2–3 minutes
4. When it shows a green ✅ "Success" — it's live!

## 4.5 — Get your backend URL

1. Click the **"Settings"** tab
2. Under **"Networking"** → **"Public Networking"**
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://mansuri-admin-backend-production.up.railway.app`
5. **Save this URL** — you need it for the frontend (Step 5)

## 4.6 — Test the backend

Open your browser and go to:
```
https://YOUR-BACKEND-URL.up.railway.app/health
```

You should see:
```json
{"status": "ok", "version": "1.0.0"}
```

Also visit the API docs:
```
https://YOUR-BACKEND-URL.up.railway.app/docs
```

You should see a Swagger UI page with all the API endpoints listed.

---

---

# STEP 5 — Deploy the Frontend (Streamlit)

## 5.1 — Add a second service on Railway

1. In your Railway project (same project, not a new one)
2. Click **"+ New"** (top right of the project view)
3. Click **"GitHub Repo"**
4. Select **"mansuri-admin"** again (same repo, different folder)

## 5.2 — Set root directory to frontend

1. Click the new service
2. Go to **"Settings"** tab
3. Find **"Root Directory"**
4. Type: `frontend`
5. Save

## 5.3 — Add environment variable

1. Click **"Variables"** tab
2. Add ONE variable:

   | Variable Name | Value |
   |---|---|
   | `API_BASE_URL` | your backend URL from Step 4.5 (e.g. `https://mansuri-admin-backend-production.up.railway.app`) |

   > ⚠️ NO trailing slash at the end of the URL!

## 5.4 — Wait for deployment

1. Click **"Deployments"** tab
2. Wait 2–3 minutes for the green ✅

## 5.5 — Get your frontend URL

1. Settings → Networking → Generate Domain
2. You'll get: `https://mansuri-admin-frontend-production.up.railway.app`
3. **This is your app's public URL — share it with your team!**

---

---

# STEP 6 — Open the App and Log In 🎉

1. Open your browser
2. Go to your **frontend URL** from Step 5.5
3. You'll see the Mansuri Admin Portal login screen
4. Log in with:
   - **Username:** `admin`
   - **Password:** whatever you set as `FIRST_ADMIN_PASSWORD` in Step 4.3

You should see the dashboard! 🎉

---

---

# STEP 7 — Backups

## Supabase Auto-Backups (already set up — nothing to do!)

Supabase Free tier automatically backs up your database **daily for 7 days**.

To restore a backup:
1. Go to supabase.com → your project
2. Click **"Database"** → **"Backups"**
3. Click **"Restore"** on any backup point

## Manual Backup (run from your Mac anytime)

```bash
# One-time setup — install PostgreSQL tools on Mac
brew install libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Create backend/.env with your real DATABASE_URL
cd "/path/to/mansuri-admin/backend"
cp ../.env.example .env
# Now edit .env and put in your real Supabase DATABASE_URL

# Run the backup script
python backup.py
# Creates: backup_20260407_143022.sql in the backend folder
```

Store this file in Google Drive / iCloud for safekeeping.

---

---

# ✏️ How to Update the App After Changes

Every time you change code and want to deploy:

```bash
cd "/path/to/mansuri-admin"
git add .
git commit -m "describe what you changed"
git push
```

Railway detects the push and automatically redeploys both services.
Takes about 2–3 minutes.

---

---

# 🆘 Troubleshooting

## "Application failed to start" on Railway

1. Click the failed deployment
2. Click **"View Logs"**
3. Scroll to the bottom — the last error tells you what's wrong

Common fixes:
- Missing environment variable → add it in Variables tab
- Wrong DATABASE_URL → double-check Supabase connection string

## "Cannot connect to backend" in Streamlit

1. Check `API_BASE_URL` in frontend Variables
2. Make sure it starts with `https://` not `http://`
3. Make sure there's no trailing `/` at the end

## Backend works but login fails

1. Check `FIRST_ADMIN_USERNAME` and `FIRST_ADMIN_PASSWORD` are set
2. In Railway backend → Deployments → click latest → View Logs
3. Look for "Seeding default admin user" line

## Want to reset the admin password

1. Go to Railway backend → Variables
2. Change `FIRST_ADMIN_PASSWORD` to your new password
3. **This won't auto-update** because the seed only runs if the user doesn't exist
4. Instead, log in with old password → Admin Panel → Update User → change password

---

---

# 📱 Sharing the App with Your Team

Just share the frontend URL:
```
https://mansuri-admin-frontend-production.up.railway.app
```

Create individual accounts for each team member:
1. Log in as admin
2. Go to **Admin Panel** → **Create User**
3. Set their username, email, password
4. Role: `member` (can create + view) or `admin` (full access)
