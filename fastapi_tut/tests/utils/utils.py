import logging
import pytest
import random
from httpx import AsyncClient
from pprint import pformat
from typing import Any, Dict
from sqlmodel import Session

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from fastapi_tut import crud
from fastapi_tut.core.config import settings
from fastapi_tut.tests.factories import AnswerFactory, UserFactory

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
async def get_superuser_cookies(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_SUPERUSER_USERNAME,
		"password": settings.FIRST_SUPERUSER_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/token", data=login_data)
	return r.cookies

@pytest.mark.anyio
async def get_student_cookies(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_STUDENT_USERNAME,
		"password": settings.FIRST_STUDENT_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/token", data=login_data)
	return r.cookies

@pytest.mark.anyio
async def get_teacher_cookies(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_TEACHER_USERNAME,
		"password": settings.FIRST_TEACHER_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/token", data=login_data)
	return r.cookies

@pytest.mark.anyio
async def get_quiz_session_objects(app: FastAPI, db: Session) -> Dict[str, Any]:
	"""Retrieve the user's quiz, answers, and cookies after completing a quiz."""
	user_in = UserFactory.stub(schema_type="create", is_student=True)
	user = UserFactory(**user_in)
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/token", 
				data={"username": user_in["username"], "password": user_in["password"]}
			)
	student_cookies = r.cookies

	quiz = crud.quiz.get(db, id=1) # first dummy quiz
	answers = []
	for question in quiz.questions: # add answers
		choice = random.choices(question.choices)[0]
		answer_in = AnswerFactory.stub(
			schema_type="create", 
			content=choice.content, 
			student=user, 
			choice=choice
		)
		answers.append(answer_in)

		async with AsyncClient(app=app, base_url="http://test") as ac:
			r = await ac.put(
				f"/quizzes/{quiz.id}/questions/{question.id}/answer", 
				cookies=student_cookies, 
				json=answer_in
			)

	return {"quiz": quiz, "answers": answers, "student_cookies": student_cookies}