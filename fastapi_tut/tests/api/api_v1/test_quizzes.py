import datetime as dt
import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict

from fastapi.encoders import jsonable_encoder

from fastapi_tut import crud
from fastapi_tut.models import QuizStudentLinkCreate
from fastapi_tut.tests.factories import QuizFactory

logging.basicConfig(level=logging.INFO)

DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

@pytest.mark.anyio
class TestReadQuiz:
	async def test_read_quizzes_superuser(
		self, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.get(
			"/quizzes/", cookies=await superuser_cookies
		)
		result = r.json()
		assert r.status_code == 200
		# NOTE tests use asyncio and trio (each function is called twice)
		# so i used the index -1 to get the latest added quiz
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id

	async def test_read_quizzes_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		teacher_cookies = await teacher_cookies
		r = await client.post(
			"/login/test-token", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		r = await client.get(
			"/quizzes/", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id

	async def test_read_quizzes_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		student_cookies = await student_cookies
		r = await client.post(
			"/login/test-token", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory()
		student_link_in = QuizStudentLinkCreate(student_id=student.id, quiz_id=quiz.id)
		crud.quiz_student_link.create(db, obj_in=student_link_in)
		r = await client.get(
			"/quizzes/", cookies=student_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id

	async def test_read_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		teacher_cookies = await teacher_cookies
		r = await client.post(
			"/login/test-token", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		r = await client.get(
			f"/quizzes/{quiz.id}", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result["quiz_code"] == quiz.quiz_code
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_teacher_code(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		teacher_cookies = await teacher_cookies
		r = await client.post(
			"/login/test-token", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		r = await client.get(
			f"/quizzes/{quiz.quiz_code}", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result["quiz_code"] == quiz.quiz_code
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		student_cookies = await student_cookies
		r = await client.post(
			"/login/test-token", cookies=student_cookies
		)
		result = r.json()
		quiz = QuizFactory()
		r = await client.get(
			f"/quizzes/{quiz.id}", cookies=student_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result["quiz_code"] == quiz.quiz_code
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_student_code(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		student_cookies = await student_cookies
		r = await client.post(
			"/login/test-token", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory()
		r = await client.get(
			f"/quizzes/{quiz.quiz_code}", cookies=student_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result["quiz_code"] == quiz.quiz_code
		assert result["teacher_id"] == quiz.teacher_id


@pytest.mark.anyio
class TestDeleteQuiz:
	async def test_delete_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		teacher_cookies = await teacher_cookies
		r = await client.post(
			"/login/test-token", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		r = await client.delete(
			f"/quizzes/{quiz.id}", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		assert result["quiz_code"] == quiz.quiz_code
		assert result["teacher_id"] == quiz.teacher_id

		quiz = crud.quiz.get(db, id=quiz.id)
		assert quiz is None

	async def test_delete_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		# TODO replace with get-user when implemented
		teacher_cookies = await teacher_cookies
		quiz = QuizFactory()
		r = await client.delete(
			f"/quizzes/{quiz.id}", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 400

@pytest.mark.anyio
class TestUpdateQuiz:
	async def test_update_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		# TODO replace with get-user when implemented
		r = await client.post(
			"/login/test-token", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		quiz_in = QuizFactory.stub(schema_type="update")
		r = await client.put(
			f"/quizzes/{quiz.id}", cookies=teacher_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz_in["name"]
		assert result["desc"] == quiz_in["desc"]
		assert result["due_date"] == quiz_in["due_date"]
		assert result["number_of_questions"] == quiz_in["number_of_questions"]
		assert result["quiz_code"] == quiz_in["quiz_code"]