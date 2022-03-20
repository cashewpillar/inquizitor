# ref: https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/type-annotation-strings/
from email.policy import default
from importlib.machinery import FrozenImporter
from typing import List, Optional
from datetime import datetime

from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models.quiz.link import QuizParticipants

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
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    created_at : datetime
    due_date : datetime
    quiz_code : str = Field(unique=True)
    teacher_id : int = Field(foreign_key='user.id')
    
    participants: List["User"] = Relationship(back_populates='student_quizzes', link_model=QuizParticipants)
    
    attempts : List["QuizAttempts"] = Relationship(back_populates="quiz")
    questions: List["QuizQuestion"] = Relationship(back_populates="quiz")
    # marks_of_users: List["MarksOfUser"] = Relationship(back_populates="quiz")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Quiz({self.name!r})>"


# many to many tables connecting user and quizzes

    
# class QuestionTypeBase(SQLModel):
#     name: str = Field(max_length=30)

# class QuestionTypeCreate(QuestionTypeBase):
#     pass

# class QuestionTypeUpdate(QuestionTypeBase):
#     name: Optional[str] = None

# class QuestionTypeInDBBase(QuestionTypeBase, TableBase):
#     pass

# class QuestionType(QuestionTypeInDBBase, table=True):
#     # NOTE skipped crud for getting questions belonging to a question-type
#     questions: List["Question"] = Relationship(back_populates="question_type")

#     def __repr__(self):
#         return f"<QuestionType({self.name!r})>"



    



# class MarksOfUserBase(SQLModel):
#     score: float = None
#     quiz_id: int = Field(default=None, foreign_key="quiz.id")
#     user_id: int = Field(default=None, foreign_key="user.id")

# class MarksOfUserCreate(MarksOfUserBase):
#     pass

# class MarksOfUserUpdate(MarksOfUserBase):
#     quiz_id: int = None
#     user_id: int = None

# class MarksOfUserInDBBase(MarksOfUserBase, TableBase):
#     pass

# class MarksOfUser(MarksOfUserInDBBase, TableBase, table=True):
#     # NOTE: accounts for only 1 quiz (written with data gathering app purposes only in mind)
#     user: "User" = Relationship(back_populates="marks")
#     quiz: Quiz = Relationship(back_populates="marks_of_users")

#     def __repr__(self):
#         # NOTE reference uses `return str(self.quiz)`
#         return f"<MarksOfUser({self.score!r})>"
