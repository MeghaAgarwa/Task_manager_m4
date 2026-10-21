from sqlalchemy import DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import List, Optional
from app.database import Base



class User(Base):   # this class represents a table in the database
    __tablename__ = "user"     # name of the table in the database
    
    # columns of the table
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100),nullable=True)

    # relationship to the Task model
    task: Mapped[List["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[str] = mapped_column(Enum('low','medium','high',name='priority_enum'), default="medium")
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # foreign key to the User model
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  
    # relationship to the User model
    owner: Mapped["User"] = relationship(back_populates="task")