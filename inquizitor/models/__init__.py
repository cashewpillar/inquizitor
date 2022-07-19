from .msg import Msg
from .quiz import (
    QuizAnswer,
    QuizAnswerCreate,
    QuizAnswerUpdate,
    QuizReadWithQuestions,
    QuizAttempt,
    QuizAttemptCreate,
    QuizAttemptUpdate,
    QuizChoice,
    QuizChoiceCreate,
    QuizChoiceUpdate,
    QuizStudentLink,
    QuizStudentLinkCreate,
    QuizStudentLinkUpdate,
    QuizQuestion,
    QuizQuestionCreate,
    QuizQuestionUpdate,
    QuizQuestionReadWithChoices,
    Quiz,
    QuizCreate,
    QuizUpdate,
)
from .token import Token, TokenPayload, RevokedToken
from .user import User, UserCreate, UserUpdate, ShowUser


""" SQLMODEL BOILERPLATE

class ThisBase(SQLModel):
class ThisCreate(ThisBase):
class ThisUpdate(ThisBase):
class ThisInDBBase(ThisBase, PKModel):
class This(ThisInDBBase, table=True):

"""
