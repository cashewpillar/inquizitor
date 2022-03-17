from os import F_OK


class QuizAnswers(TableBase):
    choice_id : int = fk
    student_id : int = fk

class AnswerBase(SQLModel):
    content: str = Field(max_length=200)
    is_correct: bool = False
    question_id: int = Field(default=None, foreign_key="question.id")

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(AnswerBase):
    content: str = None
    question_id: int = None

class AnswerInDBBase(AnswerBase, TableBase):
    pass

class Answer(AnswerInDBBase, table=True):
    question: Question = Relationship(back_populates="answers")

    def __repr__(self):
        # TODO return f"question: {self.question.content}, answer: {self.content}, is_correct: {self.is_correct}"
        return f"<Answer({self.content!r})>"
