import datetime as dt
import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict
from fastapi.encoders import jsonable_encoder

from inquizitor import crud
from inquizitor.models import QuizActions
from inquizitor.tests.factories import (
    ActionFactory, AttemptFactory, QuestionFactory, QuizFactory, UserFactory
)
logging.basicConfig(level=logging.INFO)

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
        assert result["time"] == action_in["time"]
        assert result["blur"] == action_in["blur"]
        assert result["focus"] == action_in["focus"]
        assert result["copy_"] == action_in["copy_"]
        assert result["paste"] == action_in["paste"]
        assert result["left_click"] == action_in["left_click"]
        assert result["right_click"] == action_in["right_click"]
        assert result["double_click"] == action_in["double_click"]



@pytest.mark.anyio
class TestReadQuestionActions:
    async def test_read_question_actions_students(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        student_cookies = await student_cookies
        PASSWORD = "test"
        question_actions = []
        quiz = QuizFactory()
        question = QuestionFactory(quiz=quiz)
        for i in range(3): # three students
            student = UserFactory(student=True, password=PASSWORD)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user)
            actions = []
            for j in range(5): # five question actions each
                action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
                action = crud.quiz_action.create(db, obj_in=action_in)
                actions.append(action_in)
            question_actions.append(
                {"student_id":user.id, "student_name":user.full_name, "actions":actions}
            )

        r = await client.get(
            f"/quizzes/{question.quiz_id}/questions/{question.id}/actions",
            cookies=student_cookies,
        )
        result = r.json()
        assert r.status_code == 400

    async def test_read_question_actions_teacher(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str]
    ) -> None:
        PASSWORD = "test"
        teacher_cookies = await teacher_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])
        quiz = QuizFactory(teacher=teacher)
        question = QuestionFactory(quiz=quiz)

        question_actions = []
        for i in range(3): # three students
            student = UserFactory(student=True, password=PASSWORD)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user)
            actions = []
            for j in range(5): # five question actions each
                action = ActionFactory(attempt=attempt, question=question)
                action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                actions.append(action)
            question_actions.append(
                {"actions":actions, "student_id":user.id, "student_name":user.full_name}
            )

        r = await client.get(
            f"/quizzes/{question.quiz_id}/questions/{question.id}/actions",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        student_ids = [student["student_id"] for student in question_actions]
        student_names = [student["student_name"] for student in question_actions]
        actions = {student["student_id"]: student["actions"] for student in question_actions}
        for student_in_db in result:
            assert student_in_db["student_id"] in student_ids
            assert student_in_db["student_name"] in student_names
            for action_in_db in student_in_db["actions"]:
                logging.info(f"{pformat(action_in_db)} IN {pformat(actions[student_in_db['student_id']])}")
                assert action_in_db in actions[student_in_db["student_id"]]

#     async def test_read_question_actions_superuser(
#         self, db:Session, client: AsyncClient, superuser_cookies: Dict[str, str]
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
#     async def test_read_question_actions_does_not_belong_to_quiz(
#         self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
#     ) -> None:
#         quiz = QuizFactory()
#         question = QuestionFactory()
#         r = await client.get(
#             f"/quizzes/{quiz.id}/questions/{question.id}",
#             cookies=await superuser_cookies,
#         )
#         result = r.json()
#         assert r.status_code == 404