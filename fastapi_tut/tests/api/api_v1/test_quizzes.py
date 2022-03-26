import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict

from fastapi_tut import crud
from fastapi_tut.models import QuizStudentLinkCreate
from fastapi_tut.tests.factories import QuizFactory

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
class TestGetQuiz:
	async def test_read_quizzes_superuser(
		self, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.get(
			"/quiz/", cookies=await superuser_cookies
		)
		result = r.json()
		assert r.status_code == 200
		# NOTE tests use asyncio and trio (each function is called twice)
		# so i used the index -1 to get the latest added quiz
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		# assert result[-1]["created_at"] == quiz.created_at
		# assert result[-1]["due_date"] == quiz.due_date
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
			"/quiz/", cookies=teacher_cookies
		)
		result = r.json()
		assert r.status_code == 200
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id

	# @pytest.mark.skip(reason="DOING")
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
		# DOING
		quiz = QuizFactory()
		student_link_in = QuizStudentLinkCreate(student_id=student.id, quiz_id=quiz.id)
		crud.quiz_student_link.create(db, obj_in=student_link_in)
		r = await client.get(
			"/quiz/", cookies=student_cookies
		)
		logging.info(f"{pformat(r.json())}")
		result = r.json()
		assert r.status_code == 200
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id