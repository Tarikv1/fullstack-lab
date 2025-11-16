from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.note import Note, NoteCreate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=Note)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    db_note = Note(title=note.title, body=note.body)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/", response_model=List[Note])
def list_notes(session: Session = Depends(get_session)):
    notes = session.exec(select(Note)).all()
    return notes


@router.get("/{note_id}", response_model=Note)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
