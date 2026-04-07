"""
==============================================================
backend/app/models/user.py
==============================================================
This file defines the 'users' TABLE in the database.

Each class = one table.
Each Mapped[type] = one column.

ROLES:
  "admin"  → can create, view, edit, delete, manage users
  "member" → can only create and view records

HOW TO ADD A NEW COLUMN (example: phone number):
  1. Add this line inside the class:
       phone: Mapped[str] = mapped_column(String(20), nullable=True)
  2. Also add "phone" to UserCreate and UserOut in schemas/user.py
  3. Restart the server
  NOTE: If the table already exists in the DB, you must run:
        ALTER TABLE users ADD COLUMN phone VARCHAR(20);
        (in Supabase SQL editor)
==============================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base   # all models must inherit from Base


class User(Base):
    # This is the actual table name in the database
    __tablename__ = "users"

    # Primary key — auto-increments (1, 2, 3, ...)
    # index=True makes lookups by ID fast
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Login username — must be unique across all users
    # index=True because we search by username on every login
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    # Email address — must be unique
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)

    # Hashed password — we NEVER store plain text passwords
    # Example stored value: "$2b$12$abc123..." (bcrypt hash)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    # User role: "admin" or "member"
    # Controls what the user can do in the system
    role: Mapped[str] = mapped_column(String(20), default="member", nullable=False)

    # If False, user cannot log in (soft disable without deleting)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # When the account was created — set automatically
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
