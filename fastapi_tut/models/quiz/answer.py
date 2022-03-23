from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from fastapi_tut.db.base_class import TableBase
from .choice import QuizChoice
from ..user import User

class QuizAnswerBase(SQLModel):
    content: str = Field(max_length=200)
    is_correct: bool = False
    student_id : int = Field(foreign_key='user.id')
    choice_id : int = Field(foreign_key='quizchoice.id')

class QuizAnswerCreate(QuizAnswerBase):
    pass

class QuizAnswerUpdate(QuizAnswerBase):
    content: Optional[str] = None
    is_correct: Optional[bool] = None
    student_id: Optional[int] = None
    choice_id: Optional[int] = None

class QuizAnswerInDBBase(QuizAnswerBase, TableBase):
    pass

class QuizAnswer(QuizAnswerInDBBase, table=True):
    student : Optional[User] = Relationship(back_populates='answers')
    choice : Optional[QuizChoice] = Relationship(back_populates="answers")
    

    def __repr__(self):
        # TODO return f"question: {self.question.content}, answer: {self.content}, is_correct: {self.is_correct}"
        return f"<Answer({self.content!r})>"
