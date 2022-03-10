# TODO setup database for tests, also configure app factory for tests
from httpx import AsyncClient
from typing import Dict, Generator, List

import pytest
import random

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from fastapi_tut import create_app, crud, models, utils
from fastapi_tut.api.deps import get_db
from fastapi_tut.db.init_db import init_db
from fastapi_tut.db.session import TestSession, test_engine
from fastapi_tut.tests.utils.utils import (
	get_superuser_access_token_headers,
	get_superuser_refresh_token_headers,
)

@pytest.fixture(scope="session")
def db() -> Generator:
	"""Create database for the tests."""
	yield TestSession()

@pytest.fixture(scope="module")
def app(db: Session):
	"""Create application for the tests"""
	_app = create_app()
	init_db(db, test_engine)
	yield _app



@pytest.fixture
@pytest.mark.anyio
async def client(app: FastAPI, db: Session) -> Generator:
	"""Client for making asynchronous requests (?)"""
	# See https://fastapi.tiangolo.com/advanced/async-tests/
	def get_session_override():
		return db

	app.dependency_overrides[get_db] = get_session_override
	async with AsyncClient(app=app, base_url="http://test") as ac:
		yield ac
	app.dependency_overrides.clear()

@pytest.fixture
@pytest.mark.anyio
async def production_client(app: FastAPI, db: Session) -> Generator:
	""" Client for making asynchronous requests (?)
		using the production database

		NOTE: Created for unsupported testing cases such
		as with the fastapi_jwt_auth library """
	async with AsyncClient(app=app, base_url="http://test") as ac:
		yield ac



@pytest.fixture
def user(db: Session) -> models.User:
	"""Create user for the tests"""
	data = utils.fake_user()
	user_in = models.UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	return user

@pytest.fixture
def superuser_access_token_headers(app: FastAPI) -> Dict[str, str]:
	return get_superuser_access_token_headers(app)

@pytest.fixture
def superuser_refresh_token_headers(app: FastAPI) -> Dict[str, str]:
	return get_superuser_refresh_token_headers(app)



@pytest.fixture
def quiz(db: Session) -> models.Quiz:
	"""Create quiz for the tests"""
	data = utils.fake_quiz(user.id)
	quiz_in = models.QuizCreate(**data)
	quiz = crud.quiz.create(db, obj_in=quiz_in)

	return quiz

@pytest.fixture
def question_type(db: Session) -> models.QuestionType:
	"""Create one of two question types for the tests"""
	question_type_name = utils.random_question_type()
	question_type_in = models.QuestionTypeCreate(name=question_type_name)
	question_type = crud.question_type.create(db, obj_in=question_type_in)

	return question_type

@pytest.fixture
def questions(db: Session, quiz: models.Quiz, question_type: models.QuestionType) -> List[models.Question]:
	"""Create question set belonging to the quiz for the tests"""
	questions = []
	for i in range(quiz.number_of_questions):
		data = utils.fake_question(quiz.id, question_type.id)
		question_in = models.QuestionCreate(**data)
		question = crud.question.create(db, obj_in=question_in)
		question.quiz = quiz
		questions.append(question)

		rand_index = random.randrange(0,4)
		for i in range(4):
			data = utils.fake_answer(question.id)
			if i == rand_index:
				data["is_correct"] = True
			answer_in = models.AnswerCreate(**data)
			answer = crud.answer.create(db, obj_in=answer_in)
			question.answers.append(answer)

	return questions

@pytest.fixture
def question(db: Session, questions: List[models.Question]) -> models.Question:
	"""Get a question for the tests"""
	return questions[0]

@pytest.fixture
def answers(db: Session, questions: List[models.Question]) -> List[models.Answer]:
	"""Get answer set for a question for the tests"""
	return questions[0].answers

@pytest.fixture
def answer(db: Session, answers: List[models.Answer]) -> models.Answer:
	"""Get an answer for the tests"""
	for answer in answers:
		if answer.is_correct is True:
			return answer
	return answers[0]

@pytest.fixture
def marks_of_students(db: Session, quiz: models.Quiz, user: models.User) -> List[models.MarksOfStudent]:
	"""Create marks of users for the tests"""
	marks_of_students = []
	for i in range(quiz.number_of_questions):
		data = utils.fake_marks_of_student(quiz.id, user.id)
		marks_of_student_in = models.MarksOfStudentCreate(**data)
		marks_of_student = crud.marks_of_student.create(db, obj_in=marks_of_student_in)
		marks_of_students.append(marks_of_student)

	return marks_of_students