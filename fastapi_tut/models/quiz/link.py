from sqlmodel import SQLModel, Field

class QuizParticipants(SQLModel, table=True):
    quiz_id : int = Field(foreign_key='quiz.id', default=None, primary_key=True)
    student_id : int = Field(foreign_key='user.id', default=None, primary_key=True)
