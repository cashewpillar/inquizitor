import logging
import pytest
import random
from httpx import AsyncClient
from sqlmodel import Session
from typing import Dict

from inquizitor import crud
from inquizitor.tests.factories import AnswerFactory, QuizFactory, UserFactory

@pytest.mark.anyio
class TestUpdateAnswer:
	# NOTE superuser and teacher should also be able to answer a quiz for testing purposes (?)
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