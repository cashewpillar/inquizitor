
from typing import List, Optional

from fastapi_tut.db.base_class import TableBase
from .question import  QuizQuestion
from sqlmodel import Field, Relationship

class QuizChoice(TableBase, table=True):
    content : str = Field(max_length=50)
    is_correct : bool
    
    question_id : int =  Field(foreign_key='quizquestion.id')
    question : Optional[QuizQuestion] = Relationship(back_populates="choices")

    answers: List["QuizAnswer"] = Relationship(back_populates="choice")