from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

from inquizitor.db.base_class import PKModel


class QuizChoiceBase(SQLModel):
    content: str = Field(max_length=50)
    is_correct: bool
    question_id: Optional[int] = Field(default=None, foreign_key="quizquestion.id")


class QuizChoiceCreate(QuizChoiceBase):
    pass


class QuizChoiceUpdate(QuizChoiceBase):
    content: Optional[str] = None
    is_correct: Optional[bool] = None
    question_id: Optional[int] = None


class QuizChoiceInDBBase(QuizChoiceBase, PKModel):
    pass


class QuizChoice(QuizChoiceInDBBase, table=True):
    question: Optional["QuizQuestion"] = Relationship(back_populates="choices")
    answers: List["QuizAnswer"] = Relationship(
        back_populates="choice", sa_relationship_kwargs={"cascade": "delete"}
    )


class QuizChoiceRead(QuizChoiceBase):
    id: int
    question_id: int


from .question import QuizQuestion

QuizChoice.update_forward_refs()
