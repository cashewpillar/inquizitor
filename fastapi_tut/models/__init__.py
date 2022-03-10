from .msg import Msg
from .quiz import (
	Quiz, 
	QuizCreate, 
	QuizUpdate,
	QuestionType, 
	QuestionTypeCreate, 
	QuestionTypeUpdate,
	Question, 
	QuestionCreate, 
	QuestionUpdate,
	Answer, 
	AnswerCreate, 
	AnswerUpdate,
	MarksOfStudent,
	MarksOfStudentCreate, 
	MarksOfStudentUpdate, 
)
from .token import Token, TokenPayload, RevokedToken
from .user import Role, RoleCreate, RoleUpdate, User, UserCreate, UserUpdate


""" BOILERPLATE

class ThisBase(SQLModel):
class ThisCreate(ThisBase):
class ThisUpdate(ThisBase):
class ThisInDBBase(ThisBase, TableBase):
class This(ThisInDBBase, TableBase, table=True):

"""