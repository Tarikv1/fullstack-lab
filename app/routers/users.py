from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app import schemas
from app.security import hash_password, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=schemas.UserOut,
             status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, session: Session = Depends(get_session)):
  existing = session.exec(
      select(User).where(User.email == user_in.email)
  ).first()
  if existing:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Email already registered",
      )

  user = User(
      email=user_in.email,
      hashed_password=hash_password(user_in.password),
      is_active=True,
  )
  session.add(user)
  session.commit()
  session.refresh(user)
  return user


@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
  return current_user
