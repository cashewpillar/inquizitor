# ref: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/type-annotation-strings/
from email.policy import default
from importlib.machinery import FrozenImporter
from tkinter.tix import COLUMN
from typing import List, Optional
from datetime import datetime

from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models.quiz.link import QuizStudentLink
from ..user import User

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String

# Shared Properties
class QuizBase(SQLModel):
    name: str = Field(max_length=50)
    desc: str = Field(max_length=500)    
    number_of_questions: int = 1
    created_at : datetime = Field(default=datetime.utcnow())
    due_date : datetime
    quiz_code : str = Field(sa_column=Column(String, unique=True))
    teacher_id : int = Field(foreign_key='user.id')
    # time: int = Field(description="Duration of the quiz in seconds", default=1)

# Properties to receive via API on creation
class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    name: Optional[str] = None
    desc: Optional[str] = None    
    number_of_questions: Optional[int] = None
    due_date : Optional[datetime] = None
    quiz_code : Optional[str] = None
    teacher_id : Optional[int] = None
    # time: Optional[int] = None

class QuizInDBBase(QuizBase, TableBase):
    pass

# Additional properties  to return via API
class Quiz(QuizInDBBase, table=True):
    teacher : Optional[User] = Relationship(back_populates='teacher_quizzes')
    students: List[QuizStudentLink] = Relationship(back_populates='quiz')
    attempts : List["QuizAttempt"] = Relationship(back_populates="quiz")
    questions: List["QuizQuestion"] = Relationship(back_populates="quiz")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Quiz({self.name!r})>"


# many to many tables connecting user and quizzes