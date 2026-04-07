"""
==============================================================
backend/app/database/base.py
==============================================================
This file sets up the DATABASE CONNECTION.

Think of it like this:
  - engine       = the actual connection to your database
  - SessionLocal = a "session" (one conversation with the DB)
  - Base         = the parent class all your tables inherit from

HOW TO CHANGE YOUR DATABASE:
  Just update DATABASE_URL in your .env file.
  Examples:
    SQLite  (local testing): sqlite:///./mansuri.db
    Supabase (production):   postgresql://user:pass@host:5432/dbname

  You never need to change THIS file — only the .env file.

WHAT IS pool_pre_ping?
  Supabase closes idle connections after a few minutes.
  pool_pre_ping=True makes SQLAlchemy test the connection
  before using it, and reconnects if it was dropped.
  Without this, you'd get "connection closed" errors.
==============================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings   # reads DATABASE_URL from .env


# ── Build the database engine ─────────────────────────────────────────────────
# The engine is the actual connection to your database.
# We check whether it's SQLite (local dev) or PostgreSQL (production)
# because SQLite needs one extra setting.

if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite is a simple local file-based database.
    # check_same_thread=False is required for FastAPI (which uses multiple threads).
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,   # set echo=True to print every SQL query (useful for debugging)
    )
else:
    # PostgreSQL (Supabase) — production database.
    # pool_pre_ping   = test connection before using it (handles Supabase timeouts)
    # pool_recycle    = replace connections every 5 min (keeps connections fresh)
    # pool_size       = max 5 persistent connections (more than enough for our use)
    # max_overflow    = allow 10 extra connections during busy moments
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        echo=False,   # change to True to debug SQL queries
    )


# ── Session factory ───────────────────────────────────────────────────────────
# A "session" is one conversation with the database.
# FastAPI creates one session per HTTP request, uses it, then closes it.
# autocommit=False means we control when to save changes (safer).
# autoflush=False  means we control when to send pending changes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Base class for all models ─────────────────────────────────────────────────
# Every table (User, Inventory, Order) inherits from Base.
# SQLAlchemy uses Base to discover all tables and create them.
class Base(DeclarativeBase):
    pass
