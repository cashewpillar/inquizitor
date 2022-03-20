from sqlmodel import Field


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

class QuizAnswer(AnswerInDBBase, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    choice_id : int = Field(foreign_key='quizchoice.id')
    student_id : int = Field(foreign_key='user.id')

    def __repr__(self):
        # TODO return f"question: {self.question.content}, answer: {self.content}, is_correct: {self.is_correct}"
        return f"<Answer({self.content!r})>"