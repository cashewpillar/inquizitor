from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from inquizitor.db.base_class import PKModel
from .choice import QuizChoice
from ..user import User


class QuizAnswerBase(SQLModel):
    content: Optional[str] = Field(max_length=200)
    is_correct: Optional[bool] = None
    student_id: int = Field(foreign_key="user.id")
    choice_id: Optional[int] = Field(foreign_key="quizchoice.id")
    attempt_id: Optional[int] = Field(foreign_key="quizattempt.id", index=True)
    question_id: int = Field(foreign_key="quizquestion.id", index=True)


class QuizAnswerCreate(QuizAnswerBase):
    pass


class QuizAnswerUpdate(QuizAnswerBase):
    content: Optional[str] = None
    is_correct: Optional[bool] = None
    student_id: Optional[int] = None
    choice_id: Optional[int] = None
    attempt_id: Optional[int] = None
    question_id: Optional[int] = None


class QuizAnswerInDBBase(QuizAnswerBase, PKModel):
    pass


class QuizAnswer(QuizAnswerInDBBase, table=True):
    student: Optional[User] = Relationship(back_populates="answers")
    choice: Optional[QuizChoice] = Relationship(back_populates="answers")
    attempt: Optional["QuizAttempt"] = Relationship(back_populates="answers")
    question: Optional["QuizQuestion"] = Relationship(back_populates="answers")

    def __repr__(self):
        return f"<Answer({self.content!r})>"
