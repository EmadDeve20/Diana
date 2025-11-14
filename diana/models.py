from typing import Literal

from datetime import datetime


from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from diana.database import Base



class Todo(Base):
    __tablename__ = "todos"


    title: Mapped[str] = mapped_column(String(255)) 

    status: Mapped[Literal["done", "in_progress"]] = mapped_column(String(25), default="in_progres")
    
    done_datetime: Mapped[datetime] = mapped_column(DateTime(), nullable=True, default=None)

