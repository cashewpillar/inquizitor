# ref: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/type-annotation-strings/
from typing import List, Optional
from datetime import datetime

from inquizitor.db.base_class import PKModel
from inquizitor.models.quiz.link import QuizStudentLink
from inquizitor.models.user import User

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String

# Shared Properties
class QuizBase(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50)
    desc: Optional[str] = Field(default=None, max_length=500)
    number_of_questions: int = 1
    created_at: datetime = Field(default=datetime.now())
    due_date: Optional[datetime] = None
    quiz_code: str = Field(default=None, sa_column=Column(String, unique=True))
    teacher_id: Optional[int] = Field(default=None, foreign_key="user.id")


# Properties to receive via API on creation
class QuizCreate(QuizBase):
    name: str
    teacher_id: int


class QuizUpdate(QuizBase):
    name: Optional[str] = None
    desc: Optional[str] = None
    number_of_questions: Optional[int] = None
    created_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    quiz_code: Optional[str] = None
    teacher_id: Optional[int] = None


class QuizInDBBase(QuizBase, PKModel):
    pass


# Additional properties  to return via API
class Quiz(QuizInDBBase, table=True):
    teacher: Optional[User] = Relationship(back_populates="teacher_quizzes")
    students: List[QuizStudentLink] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "delete"}
    )
    attempts: List["QuizAttempt"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "delete"}
    )
    questions: List["QuizQuestion"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"cascade": "delete"}
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Quiz({self.name!r})>"


# response model that will be sent to client
class QuizRead(QuizInDBBase):
    quiz_code: str
    created_at: datetime
    teacher_id: int


# NOTE the model with answers and score should have been a separate model (quiz_attempt)
class QuizReadWithQuestions(QuizInDBBase):
    questions: List["QuizQuestion"] = []
    answers: Optional[
        list
    ] = []  # NOTE removed QuizAnswer validation by making it generic
    score: Optional[int]  # same as above
    participant_name: Optional[str] = None


from .question import QuizQuestion

QuizReadWithQuestions.update_forward_refs()
