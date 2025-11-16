from typing import Optional
from sqlmodel import SQLModel, Field


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str


class NoteCreate(SQLModel):
    title: str
    body: str
