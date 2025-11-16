from sqlalchemy import Column, Integer, String, Boolean
from .db import Base

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    done = Column(Boolean, default=False, nullable=False)