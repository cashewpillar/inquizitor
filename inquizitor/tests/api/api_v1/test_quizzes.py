import datetime as dt
import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict

from fastapi.encoders import jsonable_encoder

from inquizitor import crud
from inquizitor.models import QuizStudentLinkCreate
from inquizitor.tests.factories import *

logging.basicConfig(level=logging.INFO)

DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

@pytest.mark.anyio
class TestReadQuizzes:
	async def test_read_quizzes_superuser(
		self, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.get(
			"/quizzes/", cookies=await superuser_cookies
		)
		result = r.json()
		logging.info(f"{pformat(result[-1])}\n\n")
		assert r.status_code == 200
		# NOTE tests use asyncio and trio (each function is called twice)
		# so i used the index -1 to get the latest added quiz
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result[-1]["quiz_code"]
		assert result[-1]["teacher_id"] == quiz.teacher_id

	async def test_read_quizzes_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		question = QuestionFactory(quiz=quiz)
		r = await client.get(
			"/quizzes/", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result[-1]["quiz_code"]
		assert result[-1]["teacher_id"] == quiz.teacher_id
		assert result[-1]["questions"] == quiz.questions

	async def test_read_quizzes_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory()
		question_1 = QuestionFactory(quiz=quiz)
		choice_1 = ChoiceFactory(question=question_1)
		answer_1 = AnswerFactory(choice=choice_1, student=student)
		# student_link_in = QuizStudentLinkCreate(student_id=student.id, quiz_id=quiz.id)
		# crud.quiz_student_link.create(db, obj_in=student_link_in)

		quizzes_in_db = crud.quiz.get_multi_by_participant(
			# NOTE change to line below when feature is needed
			# db=db, participant=current_user, skip=skip, limit=limit
			db=db, student=student
		)

		r = await client.get(
			"/quizzes/", cookies=student_cookies
		)
		result = r.json()
		# assert r.status_code == 200
		# assert result[-1]["name"] == quiz.name
		# assert result[-1]["number_of_questions"] == quiz.number_of_questions
		# assert result[-1]["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		# assert result[-1]["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result[-1]["quiz_code"]
		# assert result[-1]["teacher_id"] == quiz.teacher_id
		# assert answer_1 in result[-1]["answers"]
		assert result == quizzes_in_db

@pytest.mark.anyio
class TestReadQuiz:
	async def test_read_quiz_teacher(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
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
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_quiz_teacher_code(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
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
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_quiz_student_code(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory()
		r = await client.get(
			f"/quizzes/{quiz.id}", cookies=student_cookies
		)
		result = r.json()
		attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=student.id)
		assert r.status_code == 200
		assert attempt
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

	async def test_read_quiz_student_quiz_already_closed(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(
			due_date=dt.datetime.utcnow() - dt.timedelta(seconds=10)
		)
		r = await client.get(
			f"/quizzes/{quiz.id}", cookies=student_cookies
		)
		result = r.json()
		assert r.status_code == 400

	async def test_read_quiz_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		superuser_cookies = await superuser_cookies
		r = await client.get(
			"/users/profile", cookies=superuser_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz = QuizFactory()
		r = await client.get(
			f"/quizzes/{quiz.id}", cookies=superuser_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

@pytest.mark.anyio
class TestCreateQuiz:
	async def test_create_quiz_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		superuser_cookies = await superuser_cookies
		r = await client.get(
			"/users/profile", cookies=superuser_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])
		quiz_in = QuizFactory.stub(schema_type="create", teacher=user)
		r = await client.post(
			f"/quizzes/", cookies=superuser_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz_in["name"]
		assert result["desc"] == quiz_in["desc"]
		assert result["number_of_questions"] == quiz_in["number_of_questions"]
		assert result["created_at"] == quiz_in["created_at"]
		assert result["due_date"] == quiz_in["due_date"]
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz_in["teacher_id"]

	async def test_create_quiz_teacher_is_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
		)
		result = r.json()
		user = crud.user.get(db, id=result['id'])
		quiz_in = QuizFactory.stub(schema_type="create", teacher=user)
		r = await client.post(
			f"/quizzes/", cookies=teacher_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz_in["name"]
		assert result["desc"] == quiz_in["desc"]
		assert result["number_of_questions"] == quiz_in["number_of_questions"]
		assert result["created_at"] == quiz_in["created_at"]
		assert result["due_date"] == quiz_in["due_date"]
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz_in["teacher_id"]

	async def test_create_quiz_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		student_cookies = await student_cookies
		r = await client.get(
			"/users/profile", cookies=student_cookies
		)
		result = r.json()
		student = crud.user.get(db, id=result['id'])
		quiz_in = QuizFactory.stub(schema_type="create", teacher=student)
		r = await client.post(
			f"/quizzes/", cookies=student_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 400

@pytest.mark.anyio
class TestUpdateQuiz:
	async def test_update_quiz_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		quiz_in = QuizFactory.stub(schema_type="update")
		r = await client.put(
			f"/quizzes/{quiz.id}", cookies=await superuser_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz_in["name"]
		assert result["desc"] == quiz_in["desc"]
		assert result["due_date"] == quiz_in["due_date"]
		assert result["number_of_questions"] == quiz_in["number_of_questions"]
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation? == quiz_in["quiz_code"]

	async def test_update_quiz_teacher_is_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
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
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation? == quiz_in["quiz_code"]

	async def test_update_quiz_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		quiz_in = QuizFactory.stub(schema_type="update")
		r = await client.put(
			f"/quizzes/{quiz.id}", cookies=await teacher_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 400

	async def test_update_quiz_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		quiz_in = QuizFactory.stub(schema_type="update")
		r = await client.put(
			f"/quizzes/{quiz.id}", cookies=await student_cookies, json=quiz_in
		)
		result = r.json()
		assert r.status_code == 400

@pytest.mark.anyio
class TestDeleteQuiz:
	async def test_delete_quiz_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.delete(
			f"/quizzes/{quiz.id}", cookies=await superuser_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result["name"] == quiz.name
		assert result["number_of_questions"] == quiz.number_of_questions
		assert result["created_at"] == dt.datetime.strftime(quiz.created_at, DT_FORMAT)
		assert result["due_date"] == dt.datetime.strftime(quiz.due_date, DT_FORMAT)
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

		quiz = crud.quiz.get(db, id=quiz.id)
		assert quiz is None

	async def test_delete_quiz_teacher_is_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
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
		# assert result["quiz_code"] NOTE pending issue, should the factory be able to dictate the quiz_code to be had upon quiz creation?
		assert result["teacher_id"] == quiz.teacher_id

		quiz = crud.quiz.get(db, id=quiz.id)
		assert quiz is None

	async def test_delete_quiz_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		quiz = QuizFactory()
		r = await client.delete(
			f"/quizzes/{quiz.id}", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 400

	async def test_delete_quiz_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.delete(
			f"/quizzes/{quiz.id}", cookies=await student_cookies
		)
		result = r.json()
		assert r.status_code == 400