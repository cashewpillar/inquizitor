
class QuizQuestions(TableBase):
    content : str = Field(max_length=256)
    points : int
    order : int 
    quiz_id : int = fk


class QuestionBase(SQLModel):
    content: str = Field(max_length=200)
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    question_type_id: int = Field(default=None, foreign_key="questiontype.id")

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    content: Optional[str] = None
    quiz_id: Optional[int] = None
    question_type_id: Optional[int] = None

class QuestionInDBBase(QuestionBase, TableBase):
    pass

class Question(QuestionInDBBase, table=True):
    quiz: Optional[Quiz] = Relationship(back_populates="questions")
    question_type: Optional[QuestionType] = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")
    
    def __repr__(self):
        return f"<Question({self.content!r})>"
    
    
