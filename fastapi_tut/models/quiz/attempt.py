from typing import Optional, List
from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models.quiz.quiz import Quiz
from .question import QuizQuestion
from sqlmodel import Field, Relationship
from ..user import User

class QuizAttempts(TableBase, table=True):
    is_done : Optional[bool] = False
    
    recent_question_id : int = Field(foreign_key="quizquestion.id")
    question : Optional[QuizQuestion] = Relationship(back_populates="attempts")

    student_id : int = Field(foreign_key="user.id")
    student : Optional[User] = Relationship(back_populates='attempts')

    quiz_id : int = Field(foreign_key="quiz.id")
    quiz : Optional[Quiz] = Relationship(back_populates="attempts")