from typing import List, Optional

from fastapi_tut.db.base_class import TableBase
from .question import  QuizQuestion
from sqlmodel import Field, Relationship, SQLModel

class QuizChoiceBase(SQLModel):
    content : str = Field(max_length=50)
    is_correct : bool
    question_id : int =  Field(foreign_key='quizquestion.id')

class QuizChoiceCreate(QuizChoiceBase):
    pass

class QuizChoiceUpdate(QuizChoiceBase):
    content : Optional[str] = None
    is_correct : Optional[bool] = None
    question_id : Optional[int] = None

class QuizChoiceInDBBase(QuizChoiceBase, TableBase):
    pass

class QuizChoice(QuizChoiceInDBBase, table=True):
    question : Optional[QuizQuestion] = Relationship(back_populates="choices")
    answers: List["QuizAnswer"] = Relationship(back_populates="choice")