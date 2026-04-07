"""
==============================================================
backend/app/core/security.py
==============================================================
This file handles two security tasks:

1. PASSWORD HASHING
   When a user sets a password, we never store it as plain text.
   We store a "hash" — a scrambled version that can't be reversed.
   Example:  "admin123"  →  "$2b$12$abc...xyz"
   When they log in, we hash what they typed and compare hashes.

2. JWT TOKENS
   After a successful login, we give the user a "token" — like
   a temporary ID card. They send this token with every request
   to prove who they are. Tokens expire after 8 hours.

YOU DON'T NEED TO CHANGE THIS FILE unless you want to switch
from bcrypt to a different hashing algorithm.
==============================================================
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# ── Password hashing setup ────────────────────────────────────────────────────
# bcrypt is the algorithm — it's slow on purpose (makes brute-force hard)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Convert a plain text password to a secure hash.
    Example: hash_password("admin123") → "$2b$12$..."
    The result is stored in the database.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches a stored hash.
    Returns True if they match, False if not.
    Used during login.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Token functions ───────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token containing the user's data.
    The token expires after ACCESS_TOKEN_EXPIRE_MINUTES (default: 8 hours).

    data example: {"sub": "admin", "role": "admin"}
    The "sub" (subject) is the username.
    """
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    # Sign the token with our SECRET_KEY so nobody can fake one
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    Returns the data inside the token, or None if invalid/expired.
    Used on every protected API request.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None   # token is invalid or expired
