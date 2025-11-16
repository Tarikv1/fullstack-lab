from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Todo, User
from .schemas import (
    TodoCreate,
    TodoUpdate,
    TodoOut,
    UserCreate,
    UserOut,
    Token,
)
from .security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# ---------------------------------------------------------------------------
# Helper functions for users / auth
# ---------------------------------------------------------------------------

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, token_data.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# ---------------------------------------------------------------------------
# Simple health/sum endpoints (for earlier tests)
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"ok": True}


@app.get("/sum")
def sum_route(a: float, b: float):
    # tests expect the key to be "result"
    return {"result": a + b}


# ---------------------------------------------------------------------------
# Todos CRUD (currently NOT protected by auth)
# ---------------------------------------------------------------------------

@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(title=payload.title, done=payload.done)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/todos", response_model=list[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.id.asc()).all()


@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    return todo


@app.patch("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    if payload.title is not None:
        todo.title = payload.title
    if payload.done is not None:
        todo.done = payload.done

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo)
    db.commit()
    return


# ---------------------------------------------------------------------------
# User signup / login / me (JWT auth)
# ---------------------------------------------------------------------------

@app.post("/users/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm: username (we use as email), password
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=user.id)
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
