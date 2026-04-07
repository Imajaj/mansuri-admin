"""
==============================================================
backend/backup.py
==============================================================
DATABASE BACKUP SCRIPT

Run this script LOCALLY (on your Mac) whenever you want to
download a backup of your Supabase database.

HOW TO USE:
  1. Make sure you have your backend/.env file with DATABASE_URL
  2. Make sure you have PostgreSQL tools installed:
       Mac: brew install libpq
            echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
            source ~/.zshrc
  3. Run:
       cd backend
       python backup.py

  This creates a file like:  backup_20260407_143022.sql
  Store this file safely (Google Drive, etc.)

HOW TO RESTORE from a backup:
  1. Go to Supabase → SQL Editor
  2. Copy-paste the contents of the .sql file and run it
  OR use psql:
     psql "YOUR_DATABASE_URL" < backup_20260407_143022.sql

AUTOMATE IT (optional):
  Run this script from cron (Mac/Linux) to auto-backup weekly:
    crontab -e
    Add line: 0 9 * * 1 cd /path/to/backend && python backup.py
    (runs every Monday at 9am)
==============================================================
"""

import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv

# Load DATABASE_URL from backend/.env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file")
    print("   Make sure backend/.env exists and has DATABASE_URL set")
    exit(1)

if "sqlite" in DATABASE_URL:
    print("ℹ️  You are using SQLite (local dev). Nothing to backup via pg_dump.")
    print("   Just copy your mansuri.db file to backup it.")
    exit(0)

# ── Parse the PostgreSQL URL ──────────────────────────────────────────────────
# Format: postgresql://username:password@host:port/database
try:
    # Remove the protocol prefix
    url = DATABASE_URL.replace("postgresql://", "").replace("postgres://", "")
    # Split into user:pass and host:port/db
    user_pass, rest = url.split("@")
    username, password = user_pass.split(":", 1)
    host_port, dbname = rest.split("/", 1)
    # Handle port — default 5432 if not specified
    if ":" in host_port:
        host, port = host_port.split(":")
    else:
        host = host_port
        port = "5432"
    # Remove any URL params after the dbname (e.g. ?sslmode=require)
    dbname = dbname.split("?")[0]
except Exception as e:
    print(f"❌ Could not parse DATABASE_URL: {e}")
    exit(1)

# ── Create backup filename with timestamp ─────────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"backup_{timestamp}.sql"

print(f"📦 Starting backup of database '{dbname}' from {host}...")

# ── Run pg_dump ───────────────────────────────────────────────────────────────
# pg_dump exports the entire database to a SQL file
env = os.environ.copy()
env["PGPASSWORD"] = password   # pg_dump reads password from env var

try:
    subprocess.run(
        [
            "pg_dump",
            "-h", host,
            "-p", port,
            "-U", username,
            "-d", dbname,
            "-f", filename,
            "--no-password",
            "--clean",          # add DROP TABLE before CREATE TABLE (for clean restore)
            "--if-exists",      # don't error if tables don't exist during DROP
        ],
        env=env,
        check=True,             # raises error if pg_dump fails
    )
    size = os.path.getsize(filename)
    print(f"✅ Backup saved: {filename} ({size:,} bytes)")
    print(f"   Store this file safely — it contains all your data!")

except FileNotFoundError:
    print("❌ pg_dump not found. Install PostgreSQL tools:")
    print("   Mac: brew install libpq")
    print("   Then add to PATH: echo 'export PATH=\"/opt/homebrew/opt/libpq/bin:$PATH\"' >> ~/.zshrc")
    print("   Then run: source ~/.zshrc")

except subprocess.CalledProcessError as e:
    print(f"❌ pg_dump failed: {e}")
    print("   Check that your DATABASE_URL in .env is correct")
