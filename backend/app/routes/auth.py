"""
app/routes/auth.py
Authentication and user management endpoints.
"""
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserOut, UserUpdate
from app.services.auth import create_user, login, update_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Standard OAuth2 login – returns JWT access token."""
    return login(db, form_data.username, form_data.password)


@router.post("/users", response_model=UserOut, dependencies=[Depends(require_admin)])
def create_user_endpoint(data: UserCreate, db: Session = Depends(get_db)):
    """Admin only: create a new user."""
    return create_user(db, data)


@router.get("/users", response_model=List[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)):
    """Admin only: list all users."""
    return db.query(User).order_by(User.id).all()


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user_endpoint(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """Admin only: update a user's details / role / password."""
    return update_user(db, user_id, data)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    """Return the authenticated user's profile."""
    return current_user
