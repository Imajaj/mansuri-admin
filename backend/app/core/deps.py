"""
==============================================================
backend/app/core/deps.py
==============================================================
This file contains "dependencies" — reusable functions that
FastAPI injects into route handlers automatically.

Think of them as guards and helpers:
  - get_db()           → gives the route a database session
  - get_current_user() → reads the JWT token, returns the user
  - require_admin()    → blocks non-admin users with 403 error

HOW FASTAPI USES THESE:
  @router.get("/something")
  def my_route(db = Depends(get_db), user = Depends(get_current_user)):
      # db is ready to use, user is the logged-in person
      ...

YOU RARELY NEED TO CHANGE THIS FILE.
If you add a new role (e.g. "manager"), add a new function
like require_manager() following the same pattern as require_admin().
==============================================================
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database.base import SessionLocal
from app.models.user import User

# This tells FastAPI where the login endpoint is (for Swagger UI docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator:
    """
    Creates a database session for one request, then closes it.

    FastAPI calls this automatically when a route uses Depends(get_db).
    The 'yield' makes it work like a context manager — the code after
    yield runs even if there's an error (ensures the connection closes).
    """
    db = SessionLocal()
    try:
        yield db          # hand the session to the route
    finally:
        db.close()        # always close, even if something crashed


def get_current_user(
    token: str = Depends(oauth2_scheme),    # reads Bearer token from request header
    db: Session = Depends(get_db),
) -> User:
    """
    Reads the JWT token from the request, looks up the user in the DB.
    If token is missing/invalid/expired → returns 401 Unauthorized.
    If user not found or disabled → returns 404.

    Use this on any route that requires a logged-in user.
    """
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    user = db.query(User).filter(
        User.username == username,
        User.is_active == True      # also checks the user isn't disabled
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Same as get_current_user but ALSO checks the user is an admin.
    If not admin → returns 403 Forbidden.

    Use this on routes that only admins should access (delete, update, etc.)
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need admin privileges to perform this action.",
        )
    return current_user
