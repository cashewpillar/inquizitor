from .msg import Msg
from .quiz import (
    QuestionType,
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
    QuizAction,
    QuizActionCreate,
    QuizActionUpdate,
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
