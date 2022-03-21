from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List
from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models.quiz.quiz import Quiz
#     quiz_id : int = fk


class QuestionBase(SQLModel):
    content: str = Field(max_length=200)
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    # question_type_id: int = Field(default=None, foreign_key="questiontype.id")

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    content: Optional[str] = None
    quiz_id: Optional[int] = None
    question_type_id: Optional[int] = None

class QuestionInDBBase(QuestionBase, TableBase):
    pass

# class QuizQuestions(TableBase):
#     content : str = Field(max_length=256)
#     points : int
#     order : int 

class QuizQuestion(QuestionInDBBase, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    # content : str = Field(max_length=256)
    points : int
    order : int

    
    choices: List["QuizChoice"] = Relationship(back_populates="question")
    attempts: List["QuizAttempts"] = Relationship(back_populates="question")
    
    quiz_id : int = Field(foreign_key="quiz.id")
    quiz: Optional[Quiz] = Relationship(back_populates="questions")
    
    # question_type: Optional[QuestionType] = Relationship(back_populates="questions")
    # answers: List["Answer"] = Relationship(back_populates="question")
    
    def __repr__(self):
        return f"<Question({self.content!r})>"
    
    
