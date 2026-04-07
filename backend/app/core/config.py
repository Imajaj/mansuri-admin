"""
==============================================================
backend/app/core/config.py
==============================================================
This file reads all settings from the .env file.

WHY USE A .env FILE?
  Instead of hardcoding passwords in code (dangerous!),
  we store them in a .env file that is:
    - Never committed to GitHub (it's in .gitignore)
    - Easy to change without touching code
    - Different for local vs production

HOW TO ADD A NEW SETTING:
  1. Add it to .env:       MY_SETTING=hello
  2. Add it here:          MY_SETTING: str = "default_value"
  3. Use it anywhere:      from app.core.config import settings
                           print(settings.MY_SETTING)
==============================================================
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ── Database ──────────────────────────────────────────────
    # This is the connection string for your database.
    # Format: postgresql://username:password@host:port/database_name
    # You will paste your Supabase connection string here via Railway env vars.
    DATABASE_URL: str = "sqlite:///./mansuri.db"   # default = local SQLite for testing

    # ── JWT Security ──────────────────────────────────────────
    # SECRET_KEY is used to sign login tokens.
    # IMPORTANT: Change this to a long random string in production!
    # Generate one with: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY: str = "dev-secret-change-this-in-production"
    ALGORITHM: str = "HS256"                  # signing algorithm (don't change)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480    # 8 hours — how long login stays valid

    # ── First Admin User ──────────────────────────────────────
    # These credentials are used to create the first admin account
    # automatically when the server starts for the first time.
    # Change these to something secure in Railway environment variables!
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "admin123"
    FIRST_ADMIN_EMAIL: str = "admin@mansuri.local"

    # ── App Info ──────────────────────────────────────────────
    PROJECT_NAME: str = "Mansuri Admin Portal"
    VERSION: str = "1.0.0"

    # This tells pydantic-settings to look for a .env file
    # env_file=".env" means it reads from backend/.env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create ONE shared instance — import this everywhere
# Usage: from app.core.config import settings
#        print(settings.DATABASE_URL)
settings = Settings()
