from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

from inquizitor.db.base_class import PKModel
from inquizitor.models.quiz.quiz import Quiz

from .question import QuizQuestion
from ..user import User

class QuizAttemptBase(SQLModel):
    is_done: Optional[bool] = False
    recent_question_id: Optional[int] = Field(default=None, foreign_key="quizquestion.id")
    student_id: int = Field(foreign_key="user.id")
    quiz_id: int = Field(foreign_key="quiz.id")
    started_at: datetime = Field(default=datetime.now())

class QuizAttemptCreate(QuizAttemptBase):
    pass

class QuizAttemptUpdate(QuizAttemptBase):
    is_done: Optional[bool] = None
    recent_question_id: Optional[int] = None
    student_id: Optional[int] = None
    quiz_id: Optional[int] = None

class QuizAttemptInDBBase(QuizAttemptBase, PKModel):
    pass

class QuizAttempt(QuizAttemptInDBBase, table=True):
    recent_question: Optional[QuizQuestion] = Relationship(back_populates="attempts")
    student: Optional[User] = Relationship(back_populates='attempts')
    quiz: Optional[Quiz] = Relationship(back_populates="attempts")
    answers: Optional["QuizAnswer"] = Relationship(back_populates='attempt')
