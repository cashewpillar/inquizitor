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
    teacher_id: int = Field(default=None, foreign_key="user.id")

# Properties to receive via API on creation
class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    name: Optional[str] = None
    desc: Optional[str] = None    
    number_of_questions: Optional[int] = None
    time: Optional[int] = None
    teacher_id: Optional[int] = None

class QuizInDBBase(QuizBase, TableBase):
    pass

# Additional properties  to return via API
class Quiz(QuizInDBBase, table=True):
    questions: List["Question"] = Relationship(back_populates="quiz")
    marks_of_students: List["MarksOfStudent"] = Relationship(back_populates="quiz")
    teacher: "User" = Relationship(back_populates="quizzes")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Quiz({self.name!r})>"


    
class QuestionTypeBase(SQLModel):
    name: str = Field(max_length=30)

class QuestionTypeCreate(QuestionTypeBase):
    pass

class QuestionTypeUpdate(QuestionTypeBase):
    name: Optional[str] = None

class QuestionTypeInDBBase(QuestionTypeBase, TableBase):
    pass

class QuestionType(QuestionTypeInDBBase, table=True):
    # NOTE skipped crud for getting questions belonging to a question-type
    questions: List["Question"] = Relationship(back_populates="question_type")

    def __repr__(self):
        return f"<QuestionType({self.name!r})>"



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



class MarksOfStudentBase(SQLModel):
    score: float = None
    quiz_id: int = Field(default=None, foreign_key="quiz.id")
    student_id: int = Field(default=None, foreign_key="user.id")

class MarksOfStudentCreate(MarksOfStudentBase):
    pass

class MarksOfStudentUpdate(MarksOfStudentBase):
    quiz_id: int = None
    student_id: int = None

class MarksOfStudentInDBBase(MarksOfStudentBase, TableBase):
    pass

class MarksOfStudent(MarksOfStudentInDBBase, TableBase, table=True):
    # NOTE: accounts for only 1 quiz (written with data gathering app purposes only in mind)
    student: "User" = Relationship(back_populates="marks")
    quiz: Quiz = Relationship(back_populates="marks_of_students")

    def __repr__(self):
        # NOTE reference uses `return str(self.quiz)`
        return f"<MarksOfStudent({self.score!r})>"
