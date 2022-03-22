from sqlmodel import SQLModel, Field, Relationship

class QuizStudentLink(SQLModel, table=True):
    quiz_id : int = Field(foreign_key='quiz.id', default=None, primary_key=True)
    student_id : int = Field(foreign_key='user.id', default=None, primary_key=True)

    quiz : 'Quiz' = Relationship(back_populates='students')

    student : 'User' = Relationship(back_populates='student_quizzes')





    