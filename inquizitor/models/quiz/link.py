from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from inquizitor.db.base_class import PKModel


class QuizStudentLinkBase(SQLModel):
    quiz_id: int = Field(foreign_key="quiz.id", default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id", default=None, primary_key=True)


class QuizStudentLinkCreate(QuizStudentLinkBase):
    pass


class QuizStudentLinkUpdate(QuizStudentLinkBase):
    quiz_id: Optional[int] = None
    student_id: Optional[int] = None


class QuizStudentLinkInDBBase(QuizStudentLinkBase):
    pass


class QuizStudentLink(QuizStudentLinkInDBBase, table=True):
    quiz: "Quiz" = Relationship(back_populates="students")
    student: "User" = Relationship(back_populates="student_quizzes")
