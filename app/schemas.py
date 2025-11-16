from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None

class TodoOut(TodoBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None