from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Todo
from .schemas import TodoCreate, TodoUpdate, TodoOut

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/sum")
def sum_route(a: float, b: float):
    return {"result": a + b}

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
