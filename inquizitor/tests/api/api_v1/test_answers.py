import logging
import pytest
import random
import time
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from pprint import pformat
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
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice, question=question)

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
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice, question=question)

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
		answer_in = AnswerFactory.stub(schema_type="create", student=user, choice=choice, question=question)

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
		assert result["question_id"] == answer_in["question_id"]

		attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=user.id)
		link = crud.quiz_student_link.get_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=user.id)
		assert attempt.recent_question_id == question.id
		assert link

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
				choice=choice,
				question=question
			)
			if choice.is_correct:
				score += question.points

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

		attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=user.id)
		assert attempt.is_done


# NOTE needs to vary datetimes for automated testing to work 
# with STARTED_AT ordering instead of ATTEMPT ID
# see crud/crud_quiz/attempt.py: get_latest_by_quiz_and_student_ids
@pytest.mark.anyio
class TestRetakeQuiz:
	async def test_retake_quiz(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])

		quiz = crud.quiz.get(db, id=1)
		for i in range(2):
			for question in quiz.questions:
				choice = random.choices(question.choices)[0]
				answer_in = AnswerFactory.stub(
					schema_type="create", 
					content=choice.content, 
					student=user, 
					choice=choice,
					question=question
				)

				r = await client.put(
					f"/quizzes/{quiz.id}/questions/{question.id}/answer", 
					cookies=student_cookies, 
					json=answer_in
				)
				assert r.status_code == 200

			r = await client.get(f"/quizzes/{quiz.id}/finish", cookies=student_cookies)
			assert r.status_code == 200

		attempts = crud.quiz_attempt.get_multi_by_quiz_and_student_ids(
			db, quiz_id=1, student_id=2 # 1 for first quiz, 2 for first_student
		)
		for attempt in attempts:
			quiz = crud.quiz.get(db, id=attempt.quiz_id)
			answers = crud.quiz_answer.get_all_by_attempt(
				db, attempt_id=attempt.id
			)
			assert len(answers) == len(quiz.questions)

@pytest.mark.anyio
class TestGetQuizResults:
	async def test_get_quiz_results_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		superuser_cookies = await superuser_cookies
		r = await client.get(
			"/users/profile", cookies=superuser_cookies
		)
		result = r.json()
		superuser = crud.user.get(db, id=result['id'])

		unique_attempts = []
		quiz = crud.quiz.get(db, id=3)
		for i in range(5): # 5 students take the quiz
			student_in = UserFactory.stub(schema_type="create", is_student=True)
			student = UserFactory(**student_in)
			r = await client.post(
				"/login/token", 
				data={"username": student_in["username"], "password": student_in["password"]}
			)
			student_cookies = r.cookies

			for question in quiz.questions:
				choice = random.choices(question.choices)[0]
				answer_in = AnswerFactory.stub(
					schema_type="create", 
					content=choice.content, 
					student=student, 
					choice=choice,
					question=question
				)

				r = await client.put(
					f"/quizzes/{quiz.id}/questions/{question.id}/answer", 
					cookies=student_cookies, 
					json=answer_in
				)
				assert r.status_code == 200

			attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=student.id)
			unique_attempts.append(attempt)

			r = await client.get(f"/quizzes/{quiz.id}/finish", cookies=student_cookies)
			assert r.status_code == 200


		r = await client.get(f"/quizzes/{quiz.id}/results", cookies=superuser_cookies)
		results = r.json()

		assert r.status_code == 200			
		for result in results:
			assert result["answers"]
			assert result["questions"]
			assert type(result["score"]) == type(1)
			assert result["participant_name"]

		unique_attempt_ids = [attempt.id for attempt in unique_attempts]
		unique_attempt_ids.sort()
		results = [result["answers"][0]["attempt_id"] for result in results]
		results.sort()

		assert unique_attempt_ids == results

		# delete attempts made this session for the purposes of next tests
		for id in unique_attempt_ids:
			attempt = crud.quiz_attempt.remove(db, id=id)

