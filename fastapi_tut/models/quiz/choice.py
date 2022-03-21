
from typing import List, Optional

from fastapi_tut.db.base_class import TableBase
from sqlmodel import Field, Relationship

class QuizChoice(TableBase, table=True):
    content : str = Field(max_length=50)
    is_correct : bool
    question_id : int =  Field(foreign_key='quizquestion.id')

    answers: List["QuizAnswer"] = Relationship(back_populates="choice")