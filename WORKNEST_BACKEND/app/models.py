from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    comment = Column(String)
    time_period = Column(String)
    status = Column(String, default="Pending")
    completed = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))