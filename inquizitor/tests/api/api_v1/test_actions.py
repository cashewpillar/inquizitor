# import datetime as dt
import logging
import pytest
# from httpx import AsyncClient
# from pprint import pformat
# from sqlmodel import Session
# from typing import Dict

# from fastapi.encoders import jsonable_encoder

# from inquizitor import crud
# from inquizitor.tests.factories import QuestionFactory, QuizFactory

logging.basicConfig(level=logging.INFO)

# DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

# @pytest.mark.anyio
# class TestCreateQuiz:
#     async def test_create_quiz_superuser(
#         self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
#     ) -> None:
#         superuser_cookies = await superuser_cookies
#         r = await client.get("/users/profile", cookies=superuser_cookies)
#         result = r.json()
#         user = crud.user.get(db, id=result["id"])
#         quiz_in = QuizFactory.stub(schema_type="create", teacher=user)
#         r = await client.post(f"/quizzes/", cookies=superuser_cookies, json=quiz_in)
#         result = r.json()
#         assert r.status_code == 200
#         assert result["name"] == quiz_in["name"]
#         assert result["desc"] == quiz_in["desc"]
#         assert result["number_of_questions"] == quiz_in["number_of_questions"]
#         assert result["created_at"] == quiz_in["created_at"]
#         assert result["due_date"] == quiz_in["due_date"]
#         assert result["quiz_code"]
#         assert result["teacher_id"] == quiz_in["teacher_id"]

    # async def test_create_quiz_teacher(
    #     self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
    # ) -> None:
    #     teacher_cookies = await teacher_cookies
    #     r = await client.get("/users/profile", cookies=teacher_cookies)
    #     result = r.json()
    #     user = crud.user.get(db, id=result["id"])
    #     quiz_in = QuizFactory.stub(schema_type="create", teacher=user)
    #     r = await client.post(f"/quizzes/", cookies=teacher_cookies, json=quiz_in)
    #     result = r.json()
    #     assert r.status_code == 200
    #     assert result["name"] == quiz_in["name"]
    #     assert result["desc"] == quiz_in["desc"]
    #     assert result["number_of_questions"] == quiz_in["number_of_questions"]
    #     assert result["created_at"] == quiz_in["created_at"]
    #     assert result["due_date"] == quiz_in["due_date"]
    #     # assert result["quiz_code"]
    #     assert result["teacher_id"] == quiz_in["teacher_id"]

    # async def test_create_quiz_student(
    #     self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    # ) -> None:
    #     student_cookies = await student_cookies
    #     r = await client.get("/users/profile", cookies=student_cookies)
    #     result = r.json()
    #     student = crud.user.get(db, id=result["id"])
    #     quiz_in = QuizFactory.stub(schema_type="create", teacher=student)
    #     r = await client.post(f"/quizzes/", cookies=student_cookies, json=quiz_in)
    #     result = r.json()
    #     assert r.status_code == 400


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