# ref: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/type-annotation-strings/
from typing import List, Optional

from fastapi_tut.db.base_class import TableBase
from sqlmodel import Field, Relationship, SQLModel

# Shared Properties
class QuizBase(SQLModel):
    name: str = Field(max_length=50)
    desc: str = Field(max_length=500)    
    number_of_questions: int = 1
    time: int = Field(description="Duration of the quiz in seconds", default=1)

# Properties to receive via API on creation
class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    name: Optional[str] = None
    desc: Optional[str] = None    
    number_of_questions: Optional[int] = None
    time: Optional[int] = None

class QuizInDBBase(QuizBase, TableBase):
    pass

# Additional properties  to return via API
class Quiz(QuizInDBBase, table=True):
    questions: List["Question"] = Relationship(back_populates="quiz")
    scores: List["MarksOfUser"] = Relationship(back_populates="quiz")

    def __str__(self):
        return self.name

    # TODO: might be included in crud instead
    # def get_questions(self):
        # return self.question_set.all()


    
class QuestionTypeBase(SQLModel):
    name: str = Field(max_length=30)

class QuestionTypeCreate(QuestionTypeBase):
    pass

class QuestionTypeUpdate(QuestionTypeBase):
    name: Optional[str] = None

class QuestionTypeInDBBase(QuestionTypeBase, TableBase):
    pass

class QuestionType(QuestionTypeInDBBase, table=True):
    questions: List["Question"] = Relationship(back_populates="question_type")

    def __str__(self):
        return self.name



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
    
    def __str__(self):
        return self.content
    
    # def get_answers(self):
        # return self.answer_set.all()
    
    
    
class AnswerBase(SQLModel):
    content: str = Field(max_length=200)
    correct: bool = False
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

    # def __str__(self):
    #     return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"
    


class MarksOfUser(TableBase, table=True):
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    score: float = Field()
    
    # NOTE: accounts for only 1 quiz (written with data gathering app purposes only in mind)
    user: "User" = Relationship(back_populates="score")
    quiz: Quiz = Relationship(back_populates="")

    # def __str__(self):
    #     return str(self.quiz)
