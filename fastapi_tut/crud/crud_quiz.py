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
	MarksOfUser, 
	MarksOfUserCreate, 
	MarksOfUserUpdate,
)

class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
	# went with implicit definition despite https://www.python.org/dev/peps/pep-0020/#id2
	pass

class CRUDMarksOfUser(CRUDBase[MarksOfUser, MarksOfUserCreate, MarksOfUserUpdate]):
	pass
	
class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	pass

class CRUDQuestionType(CRUDBase[QuestionType, QuestionTypeCreate, QuestionTypeUpdate]):
	pass

class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
	pass


answer = CRUDAnswer(Answer)
marks_of_user = CRUDMarksOfUser(MarksOfUser)
question_type = CRUDQuestionType(QuestionType)
question = CRUDQuestion(Question)
quiz = CRUDQuiz(Quiz)