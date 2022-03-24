import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from typing import Dict

from fastapi_tut import crud
from fastapi_tut.tests.factories import QuizFactory

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
async def test_read_quiz(
	db, client: AsyncClient, superuser_cookies: Dict[str, str]
) -> None:
	quiz = QuizFactory()
	repr(quiz)
	# crud.user.get(db, id=1).student_quizzes.append(quiz)
	r = await client.get(
		"/quiz/", cookies=await superuser_cookies
	)
	result = r.json()
	logging.info(f"{pformat(result)}")
	assert r.status_code == 200