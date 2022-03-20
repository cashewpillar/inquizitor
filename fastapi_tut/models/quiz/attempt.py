from typing import Optional, List
from fastapi_tut.db.base_class import TableBase
from sqlmodel import Field

class QuizAttempts(TableBase):
    is_done : Optional[bool] = False
    quiz_id : int = Field(foreign_key="quiz.id")
    recent_question_id : int = Field(foreign_key="quizquestions.id")
    student_id : int = Field(foreign_key="user.id")
