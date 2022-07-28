from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List
from inquizitor.db.base_class import PKModel


class QuizQuestionBase(SQLModel):
    content: str = Field(max_length=200)
    points: int
    order: int
    quiz_id: Optional[int] = Field(default=None, foreign_key="quiz.id")


class QuizQuestionCreate(QuizQuestionBase):
    pass


class QuizQuestionUpdate(QuizQuestionBase):
    content: Optional[str] = None
    points: Optional[int] = None
    order: Optional[int] = None


class QuizQuestionInDBBase(QuizQuestionBase, PKModel):
    pass


class QuizQuestion(QuizQuestionInDBBase, table=True):
    choices: List["QuizChoice"] = Relationship(
        back_populates="question", sa_relationship_kwargs={"cascade": "delete"}
    )
    attempts: List["QuizAttempt"] = Relationship(back_populates="recent_question")
    quiz: Optional["Quiz"] = Relationship(back_populates="questions")
    actions: Optional["QuizAction"] = Relationship(
        back_populates="question", sa_relationship_kwargs={"cascade": "delete"}
    )

    def __repr__(self):
        return f"<Question({self.content!r})>"


class QuizQuestionRead(QuizQuestionBase):
    id: int
    quiz_id: int


class QuizQuestionReadWithChoices(QuizQuestionInDBBase):
    choices: List["QuizChoice"] = []


from inquizitor.models.quiz.choice import QuizChoice
from inquizitor.models.quiz.quiz import Quiz

QuizQuestionReadWithChoices.update_forward_refs()
