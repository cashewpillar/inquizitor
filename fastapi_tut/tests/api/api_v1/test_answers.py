import logging
import pytest
import random
from fastapi import FastAPI
from httpx import AsyncClient
from sqlmodel import Session
from typing import Any, Dict

from fastapi_tut import crud
from fastapi_tut.tests.factories import AnswerFactory, QuizFactory, UserFactory
from fastapi_tut.tests.utils.utils import get_quiz_session_objects


@pytest.mark.anyio
class TestUpdateAnswer:
	async def test_update_answer_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		superuser_cookies = await superuser_cookies
		r = await client.get(
			"/users/profile", cookies=superuser_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])

		quiz = crud.quiz.get(db, id=1)
		question = crud.quiz_question.get(db, id=1)
		choice = crud.quiz_choice.get(db, id=1)
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice)

		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{question.id}/answer", cookies=superuser_cookies, json=answer_in
		)
		assert r.status_code == 400

	async def test_update_answer_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])

		quiz = crud.quiz.get(db, id=1)
		question = crud.quiz_question.get(db, id=1)
		choice = crud.quiz_choice.get(db, id=1)
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice)

		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{question.id}/answer", cookies=teacher_cookies, json=answer_in
		)
		assert r.status_code == 400

	async def test_update_answer_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])

		quiz = crud.quiz.get(db, id=1)
		question = crud.quiz_question.get(db, id=1)
		choice = crud.quiz_choice.get(db, id=1)
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice)

		# NOTE NOT WORKING access the quiz to create attempt obj
		r = await client.get(
			f"/quizzes/{quiz.quiz_code}", cookies=student_cookies
		)

		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{question.id}/answer", 
			cookies=student_cookies, 
			json=answer_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == answer_in["content"]
		assert result["is_correct"] == answer_in["is_correct"]
		assert result["student_id"] == answer_in["student_id"]
		assert result["choice_id"] == answer_in["choice_id"]

		attempt = crud.quiz_attempt.get_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=user.id)
		assert attempt.recent_question_id == question.id

@pytest.mark.anyio
class TestGetScore:
	# TODO what if a question is left unanswered?
	async def test_get_score(
		self, db: Session, client: AsyncClient
	) -> None:
		user_in = UserFactory.stub(schema_type="create", is_student=True)
		user = UserFactory(**user_in)
		r = await client.post(
				"/login/token", 
				data={"username": user_in["username"], "password": user_in["password"]}
			)
		student_cookies = r.cookies

		score = 0
		quiz = crud.quiz.get(db, id=1)
		for question in quiz.questions:
			choice = random.choices(question.choices)[0]
			answer_in = AnswerFactory.stub(
				schema_type="create", 
				content=choice.content, 
				student=user, 
				choice=choice
			)
			if choice.is_correct:
				score += 1

			r = await client.put(
				f"/quizzes/{quiz.id}/questions/{question.id}/answer", 
				cookies=student_cookies, 
				json=answer_in
			)
			result = r.json()
			assert r.status_code == 200

		r = await client.get(f"/quizzes/{quiz.id}/finish", cookies=student_cookies)
		result = r.json()
		assert r.status_code == 200
		assert result == score

@pytest.mark.anyio
class TestReadAnswers:
	"""
	NOTE
	- any teacher can read answers of a specific student for a quiz they did not author
	"""
	async def test_read_answers_admin(
		self, 
		app: FastAPI, 
		client: AsyncClient, 
		quiz_session_objects: Dict[str, Any], 
		superuser_cookies: Dict[str, str]
	) -> None:
		quiz = quiz_session_objects["quiz"]
		answers = quiz_session_objects["answers"]
		student_cookies = quiz_session_objects["student_cookies"]
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		user_id = r.json()['id']

		r = await client.get(
			f"/quizzes/{quiz.id}/answers?student_id={user_id}", cookies=await superuser_cookies
		)
		result = r.json()
		assert r.status_code == 200
		for i, answer in enumerate(result):
			assert answer["is_correct"]	 == answers[i]["is_correct"]
			assert answer["student_id"] == answers[i]["student_id"]
			assert answer["choice_id"] == answers[i]["choice_id"]

	async def test_read_answers_teacher(
		self, 
		app: FastAPI, 
		client: AsyncClient, 
		quiz_session_objects: Dict[str, Any], 
		teacher_cookies: Dict[str, str]
	) -> None:
		quiz = quiz_session_objects["quiz"]
		answers = quiz_session_objects["answers"]
		student_cookies = quiz_session_objects["student_cookies"]
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		user_id = r.json()['id']

		r = await client.get(
			f"/quizzes/{quiz.id}/answers?student_id={user_id}", cookies=await teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		for i, answer in enumerate(result):
			assert answer["is_correct"]	 == answers[i]["is_correct"]
			assert answer["student_id"] == answers[i]["student_id"]
			assert answer["choice_id"] == answers[i]["choice_id"]

	async def test_read_answers_student(
		self, app: FastAPI, client: AsyncClient, quiz_session_objects: Dict[str, Any]
	) -> None:
		quiz = quiz_session_objects["quiz"]
		answers = quiz_session_objects["answers"]
		student_cookies = quiz_session_objects["student_cookies"]

		r = await client.get(f"/quizzes/{quiz.id}/answers", cookies=student_cookies)
		result = r.json()
		assert r.status_code == 200
		for i, answer in enumerate(result):
			assert answer["is_correct"]	 == answers[i]["is_correct"]
			assert answer["student_id"] == answers[i]["student_id"]
			assert answer["choice_id"] == answers[i]["choice_id"]

	async def test_read_answers_student_no_answer(
		self, db: Session, app: FastAPI, client: AsyncClient
	) -> None:
		user_in = UserFactory.stub(schema_type="create", is_student=True)
		user = UserFactory(**user_in)
		async with AsyncClient(app=app, base_url="http://test") as ac:
			r = await ac.post(
					"/login/token", 
					data={"username": user_in["username"], "password": user_in["password"]}
				)
		student_cookies = r.cookies

		QUIZ_ID = 1 # first dummy quiz
		r = await client.get(f"/quizzes/{QUIZ_ID}/answers", cookies=student_cookies)
		result = r.json()
		assert r.status_code == 200
		assert result == []