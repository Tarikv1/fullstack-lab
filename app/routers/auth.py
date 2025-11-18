from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app import schemas
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
  # form_data.username is the email in our frontend
  user = session.exec(
      select(User).where(User.email == form_data.username)
  ).first()

  if not user or not verify_password(form_data.password, user.hashed_password):
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect email or password",
          headers={"WWW-Authenticate": "Bearer"},
      )

  access_token = create_access_token(user_id=user.id)
  return schemas.Token(access_token=access_token, token_type="bearer")
