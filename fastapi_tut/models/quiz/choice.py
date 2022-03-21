
from typing import List, Optional

from fastapi_tut.db.base import TableBase
from sqlmodel import Field, Relationship

class QuizChoice(TableBase):
    __tablename__ = 'quizchoice'

    id : Optional[int] = Field(default=None, primary_key=True)
    content : str = Field(max_length=50)
    is_correct : bool
    question_id : int =  Field(foreign_key='quizquestions.id')

    answers: List["QuizAnswer"] = Relationship(back_populates="choice")