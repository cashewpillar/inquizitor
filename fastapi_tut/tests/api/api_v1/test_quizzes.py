import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from typing import Dict

from fastapi_tut import crud
from fastapi_tut.tests.factories import QuizFactory

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
class TestGetQuiz:
	async def test_read_quiz_superuser(
		self, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		r = await client.get(
			"/quiz/", cookies=await superuser_cookies
		)
		result = r.json()
		logging.info(f"{pformat(result)}")
		assert r.status_code == 200
		# NOTE tests use asyncio and trio (each function is called twice)
		# so i used the index -1 to get the latest added quiz
		assert result[-1]["name"] == quiz.name
		assert result[-1]["number_of_questions"] == quiz.number_of_questions
		# assert result[-1]["created_at"] == quiz.created_at
		# assert result[-1]["due_date"] == quiz.due_date
		assert result[-1]["quiz_code"] == quiz.quiz_code
		assert result[-1]["teacher_id"] == quiz.teacher_id