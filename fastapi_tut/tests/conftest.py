# TODO setup database for tests, also configure app factory for tests
from httpx import AsyncClient
from typing import Dict, Generator

import pytest
import random

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from fastapi_tut import create_app, crud, models, utils
from fastapi_tut.api.deps import get_db
from fastapi_tut.db.session import TestSession
from fastapi_tut.tests.utils.utils import (
	get_superuser_access_token_headers,
	get_superuser_refresh_token_headers,
)

@pytest.fixture(scope="session")
def db() -> Generator:
	"""Create database for the tests."""
	yield TestSession()

@pytest.fixture(scope="module")
def app():
	"""Create application for the tests"""
	_app = create_app()
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
	data = utils.fake_quiz()
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
def question(db: Session, quiz: models.Quiz, question_type: models.QuestionType) -> models.Question:
	"""Create question for the tests"""
	data = utils.fake_question(quiz.id, question_type.id)
	question_in = models.QuestionCreate(**data)
	question = crud.question.create(db, obj_in=question_in)

	return question

# NOTE: will update and create a set fixture consisting of 1 question 1 question type 4 answers
@pytest.fixture
def answer(db: Session, question: models.Question) -> models.Answer:
	"""Create answer for the tests"""
	data = utils.fake_answer(question.id)
	answer_in = models.AnswerCreate(**data)
	answer = crud.answer.create(db, obj_in=answer_in)
	
	return answer

@pytest.fixture
def marks_of_user(db: Session, quiz: models.Quiz, user: models.User) -> models.MarksOfUser:
	"""Create marks of user for the tests"""
	data = utils.fake_marks_of_user(quiz.id, user.id)
	marks_of_user_in = models.MarksOfUserCreate(**data)
	marks_of_user = crud.marks_of_user.create(db, obj_in=marks_of_user_in)

	return marks_of_user