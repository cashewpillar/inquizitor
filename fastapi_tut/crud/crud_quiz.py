from sqlmodel import Session

from typing import Dict, Any, Optional, Union

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import (
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
)

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	# went with implicit definition despite https://www.python.org/dev/peps/pep-0020/#id2
	pass

class CRUDQuestionType(CRUDBase[QuestionType, QuestionTypeCreate, QuestionTypeUpdate]):
	pass

class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
	pass

class CRUDQuestion(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
	pass

answer = CRUDQuestionType(Answer)
question_type = CRUDQuestionType(QuestionType)
question = CRUDQuestion(Question)
quiz = CRUDQuiz(Quiz)