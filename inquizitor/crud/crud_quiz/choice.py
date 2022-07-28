from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizChoice, QuizChoiceCreate, QuizChoiceUpdate

class CRUDQuizChoice(CRUDBase[QuizChoice, QuizChoiceCreate, QuizChoiceUpdate]):
    pass

quiz_choice = CRUDQuizChoice(QuizChoice)
