# ref: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/type-annotation-strings/

from fastapi_tut.db.base_class import Base
from sqlmodel import Field, Relationship
# from django.contrib.auth.models import User
# import random

from fastapi_tut.models import User

class Quiz(Base, table=True):
    name: str = Field(max_length=50)
    desc: str = Field(max_length=500)    
    number_of_questions: int =Field(default=1)
    time: int = Field(help_text="Duration of the quiz in seconds", default="1")
    
    questions: List["Question"] = Relationship(back_populates="quiz")
    scores: List["MarksOfUser"] = Relationship(back_populates="quiz")

    def __str__(self):
        return self.name

    # might be included in crud instead
    # def get_questions(self):
        # return self.question_set.all()

    
class QuestionType(Base, table=True):
    name: str = Field(max_length=30)

    questions: List["Question"] = Relationship(back_populates="question_type")

    def __str__(self):
        return self.name


class Question(Base, table=True):
    content: str = Field(max_length=200)
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    question_type_id: int = Field(default=None, foreign_key="questiontype.id")
    # question_type = # fill-in-the-blanks or multiple-choice

    quiz: Optional[Quiz] = Relationship(back_populates="questions")
    question_type: Optional[QuestionType] = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")
    
    def __str__(self):
        return self.content
    
    # def get_answers(self):
        # return self.answer_set.all()
    
    
class Answer(Base, table=True):
    content: str = Field(max_length=200)
    correct: bool = Field(default=False)
    question_id: int = Field(default=None, foreign_key="question.id")
    
    question: Question = Relationship(back_populates="answers")

    # def __str__(self):
    #     return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"
    

class MarksOfUser(Base, table=True):
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    score: float = Field()
    
    # NOTE: accounts for only 1 quiz (written with data gathering app purposes only in mind)
    user: "User" = Relationship(back_populates="score")
    quiz: Quiz = Relationship(back_populates="")

    # def __str__(self):
    #     return str(self.quiz)
