from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from .schemas import TokenData

# In real apps, put these in environment variables or config
SECRET_KEY = "change-me-in-production-very-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use pbkdf2_sha256 instead of bcrypt to avoid backend issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    # pbkdf2_sha256 has no 72-byte limit, but keep function in one place
    if password is None:
        password = ""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if plain_password is None:
        plain_password = ""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str | None = payload.get("sub")
        if sub is None:
            return None
        return TokenData(user_id=int(sub))
    except (JWTError, ValueError):
        return None
