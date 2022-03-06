from typing import Dict, Any, Optional, Union, List

from sqlmodel import Session

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

# went with implicit definition for all crud classes despite https://www.python.org/dev/peps/pep-0020/#id2
class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
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