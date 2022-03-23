from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models.quiz.quiz import Quiz

from .question import QuizQuestion
from ..user import User

class QuizAttemptsBase(SQLModel):
    is_done : Optional[bool] = False
    recent_question_id : int = Field(foreign_key="quizquestion.id")
    student_id : int = Field(foreign_key="user.id")
    quiz_id : int = Field(foreign_key="quiz.id")

class QuizAttemptsCreate(QuizAttemptsBase):
    pass

class QuizAttemptsUpdate(QuizAttemptsBase):
    is_done : Optional[bool] = None
    recent_question_id : Optional[int] = None
    student_id : Optional[int] = None
    quiz_id : Optional[int] = None

class QuizAttemptsInDBBase(QuizAttemptsBase, TableBase):
    pass

class QuizAttempts(QuizAttemptsInDBBase, table=True):
    question : Optional[QuizQuestion] = Relationship(back_populates="attempts")
    student : Optional[User] = Relationship(back_populates='attempts')
    quiz : Optional[Quiz] = Relationship(back_populates="attempts")