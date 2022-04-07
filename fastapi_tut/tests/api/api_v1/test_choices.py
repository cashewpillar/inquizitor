import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict

from fastapi.encoders import jsonable_encoder

from fastapi_tut import crud
from fastapi_tut.tests.factories import ChoiceFactory, QuestionFactory, QuizFactory, UserFactory

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
class TestCreateChoice:
	async def test_create_choice_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		question = QuestionFactory(quiz=quiz)
		choice_in = ChoiceFactory.stub(schema_type="create", question=question)
		r = await client.post(
			f"/quizzes/{quiz.id}/questions/{question.id}", 
			cookies=await student_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 400

	async def test_create_choice_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		quiz = QuizFactory()
		question = QuestionFactory(quiz=quiz)
		choice_in = ChoiceFactory.stub(schema_type="create", question=question)
		r = await client.post(
			f"/quizzes/{quiz.id}/questions/{question.id}", 
			cookies=await teacher_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 400

	async def test_create_choice_teacher_is_author(
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
		choice_in = ChoiceFactory.stub(schema_type="create", question=question)
		r = await client.post(
			f"/quizzes/{quiz.id}/questions/{question.id}", 
			cookies=teacher_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice_in["content"]
		assert result["is_correct"] == choice_in["is_correct"]
		assert result["question_id"] == choice_in["question_id"]

	async def test_create_choice_superuser(
		self, db:Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		teacher = UserFactory(is_teacher=True)
		quiz = QuizFactory(teacher=teacher)
		question = QuestionFactory(quiz=quiz)
		choice_in = ChoiceFactory.stub(schema_type="create", question=question)
		r = await client.post(
			f"/quizzes/{quiz.id}/questions/{question.id}", 
			cookies=await superuser_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice_in["content"]
		assert result["is_correct"] == choice_in["is_correct"]
		assert result["question_id"] == choice_in["question_id"]

@pytest.mark.anyio
class TestUpdateChoice:
	async def test_update_choice_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		choice_in = ChoiceFactory.stub(schema_type="update", is_correct=True)
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}", 
			cookies=await student_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 400

	async def test_update_choice_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		choice_in = ChoiceFactory.stub(schema_type="update", is_correct=True)
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}", 
			cookies=await teacher_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 400

	async def test_update_choice_teacher_is_author(
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
		choice = ChoiceFactory(question=question)
		choice_in = ChoiceFactory.stub(schema_type="update", question=question)
		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}", 
			cookies=teacher_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice_in["content"]
		assert result["is_correct"] == choice_in["is_correct"]
		assert result["question_id"] == choice_in["question_id"]

	async def test_update_choice_superuser(
		self, db:Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		choice_in = ChoiceFactory.stub(schema_type="update", question=question)
		r = await client.put(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}", 
			cookies=await superuser_cookies,
			json=choice_in
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice_in["content"]
		assert result["is_correct"] == choice_in["is_correct"]
		assert result["question_id"] == choice_in["question_id"]

@pytest.mark.anyio
class TestDeleteChoice:
	async def test_delete_choice_student(
		self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		r = await client.delete(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}",
			cookies=await student_cookies,
		)
		result = r.json()
		assert r.status_code == 400

	async def test_delete_choice_teacher_not_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		r = await client.delete(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}",
			cookies=await teacher_cookies,
		)
		result = r.json()
		assert r.status_code == 400

	async def test_delete_choice_teacher_is_author(
		self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
	) -> None:
		teacher_cookies = await teacher_cookies
		r = await client.get(
			"/users/profile", cookies=teacher_cookies
		)
		result = r.json()
		teacher = crud.user.get(db, id=result['id'])
		quiz = QuizFactory(teacher=teacher)
		repr(quiz) 

		quiz = QuizFactory(teacher=teacher)
		question = QuestionFactory(quiz=quiz)
		choice = ChoiceFactory(question=question)
		r = await client.delete(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}",
			cookies=teacher_cookies,
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice.content
		assert result["is_correct"] == choice.is_correct
		assert result["question_id"] == choice.question_id

		choice = crud.quiz_choice.get(db, id=choice.id)
		assert choice is None

	async def test_delete_choice_superuser(
		self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
	) -> None:
		choice = ChoiceFactory()
		question = crud.quiz_question.get(db, choice.question_id)
		quiz = crud.quiz.get(db, question.quiz_id)
		r = await client.delete(
			f"/quizzes/{quiz.id}/questions/{choice.question_id}/choices/{choice.id}",
			cookies=await superuser_cookies,
		)
		result = r.json()
		assert r.status_code == 200
		assert result["content"] == choice.content
		assert result["is_correct"] == choice.is_correct
		assert result["question_id"] == choice.question_id

		choice = crud.quiz_choice.get(db, id=choice.id)
		assert choice is None