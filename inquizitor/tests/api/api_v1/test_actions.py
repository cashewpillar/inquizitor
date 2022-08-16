import datetime as dt
import logging
import pytest
from httpx import AsyncClient
from sqlmodel import Session
from typing import Dict

from inquizitor import crud
from inquizitor.tests.factories import ActionFactory, AttemptFactory, QuestionFactory

logging.basicConfig(level=logging.INFO)

DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

@pytest.mark.anyio
class TestCreateAction:
    async def test_create_action_superuser(
        self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
    ) -> None:
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=superuser_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory()
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=superuser_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 400

    async def test_create_action_teacher(
        self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
    ) -> None:
        teacher_cookies = await teacher_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory()
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=teacher_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 400

    async def test_create_action_student(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        student_cookies = await student_cookies
        r = await client.get("/users/profile", cookies=student_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory(student=user)
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=student_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 200
        # assert result["time"] == dt.datetime.strftime(quiz.time, DT_FORMAT)
        assert result["time"] == action_in["time"]
        assert result["blur"] == action_in["blur"]
        assert result["focus"] == action_in["focus"]
        assert result["copy_"] == action_in["copy_"]
        assert result["paste"] == action_in["paste"]
        assert result["left_click"] == action_in["left_click"]
        assert result["right_click"] == action_in["right_click"]
        assert result["double_click"] == action_in["double_click"]



# @pytest.mark.anyio
# class TestReadQuestion:
#     async def test_read_question_student(
#         self, client: AsyncClient, student_cookies: Dict[str, str]
#     ) -> None:
#         question = QuestionFactory()
#         r = await client.get(
#             f"/quizzes/{question.quiz_id}/questions/{question.id}",
#             cookies=await student_cookies,
#         )
#         result = r.json()
#         assert r.status_code == 200
#         assert result["id"] == question.id
#         assert result["content"] == question.content
#         assert result["points"] == question.points
#         assert result["order"] == question.order
#         assert result["quiz_id"] == question.quiz_id

#     async def test_read_question_teacher(
#         self, client: AsyncClient, teacher_cookies: Dict[str, str]
#     ) -> None:
#         question = QuestionFactory()
#         r = await client.get(
#             f"/quizzes/{question.quiz_id}/questions/{question.id}",
#             cookies=await teacher_cookies,
#         )
#         result = r.json()
#         assert r.status_code == 200
#         assert result["id"] == question.id
#         assert result["content"] == question.content
#         assert result["points"] == question.points
#         assert result["order"] == question.order
#         assert result["quiz_id"] == question.quiz_id

#     async def test_read_question_superuser(
#         self, client: AsyncClient, superuser_cookies: Dict[str, str]
#     ) -> None:
#         question = QuestionFactory()
#         r = await client.get(
#             f"/quizzes/{question.quiz_id}/questions/{question.id}",
#             cookies=await superuser_cookies,
#         )
#         result = r.json()
#         assert r.status_code == 200
#         assert result["id"] == question.id
#         assert result["content"] == question.content
#         assert result["points"] == question.points
#         assert result["order"] == question.order
#         assert result["quiz_id"] == question.quiz_id

#     # NOTE supposedly on crud tests but seems therell be no crud tests
#     async def test_read_question_does_not_belong_to_quiz(
#         self, client: AsyncClient, superuser_cookies: Dict[str, str]
#     ) -> None:
#         quiz = QuizFactory()
#         question = QuestionFactory()
#         r = await client.get(
#             f"/quizzes/{quiz.id}/questions/{question.id}",
#             cookies=await superuser_cookies,
#         )
#         result = r.json()
#         assert r.status_code == 404