# TODO: other read methods depending on model, will do during endpoint creation

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from fastapi_tut import crud, models
from fastapi_tut.utils import (
	fake, 
	fake_answer, 
	fake_question, 
	fake_quiz, 
	random_str
)

class TestQuiz:
	def test_create_quiz(self, db: Session) -> None:
		data = fake_quiz()
		quiz_in = models.QuizCreate(**data)
		quiz = crud.quiz.create(db, obj_in=quiz_in)
		assert quiz.name == data["name"]
		assert quiz.desc == data["desc"]
		assert quiz.number_of_questions == data["number_of_questions"]
		assert quiz.time == data["time"]

	def test_get_quiz(self, db: Session, quiz: models.Quiz) -> None:
		quiz_2 = crud.quiz.get(db, id=quiz.id)
		assert quiz_2
		assert quiz.name == quiz_2.name
		assert jsonable_encoder(quiz) == jsonable_encoder(quiz_2)

	def test_update_quiz(self, db: Session, quiz: models.Quiz) -> None:
		data = fake_quiz()
		quiz_in_update = models.QuizUpdate(**data)
		crud.quiz.update(db, db_obj=quiz, obj_in=quiz_in_update)
		quiz_2 = crud.quiz.get(db, id=quiz.id)
		assert quiz_2
		assert quiz.name == quiz_2.name
		assert quiz.desc == quiz_2.desc
		assert quiz.number_of_questions == quiz_2.number_of_questions
		assert quiz.time == quiz_2.time


class TestQuestionType:
	def test_create_question_type(self, db: Session) -> None:
		name = random_str()
		question_type_in = models.QuestionTypeCreate(name=name)
		question_type = crud.question_type.create(db, obj_in=question_type_in)
		assert question_type.name == name

	def test_get_question_type(self, db: Session) -> None:
		question_type_in = models.QuestionType(name=random_str())
		question_type = crud.question_type.create(db, obj_in=question_type_in)
		question_type_2 = crud.question_type.get(db, id=question_type.id)
		assert question_type_2
		assert question_type.name == question_type_2.name
		assert jsonable_encoder(question_type) == jsonable_encoder(question_type_2)

	def test_update_question_type(self, db: Session, question_type: models.QuestionType) -> None:
		name = random_str()
		question_type_in_update = models.QuestionTypeUpdate(name=name)
		crud.question_type.update(db, db_obj=question_type, obj_in=question_type_in_update)
		question_type_2 = crud.question_type.get(db, id=question_type.id)
		assert question_type_2
		assert question_type.name == question_type_2.name


class TestQuestion:
	def test_create_question(self, db: Session, quiz: models.Quiz, question_type: models.QuestionType) -> None:
		data = fake_question(quiz.id, question_type.id)
		question_in = models.QuestionCreate(**data)
		question = crud.question.create(db, obj_in=question_in)
		assert question.content == question_in.content
		assert question.quiz_id == question_in.quiz_id
		assert question.question_type_id == question_in.question_type_id

	def test_get_question(self, db: Session, question: models.Question) -> None:
		db_obj = crud.question.get(db, id=question.id)
		assert db_obj
		assert question.content == db_obj.content
		assert jsonable_encoder(question) == jsonable_encoder(db_obj)

	def test_update_question(self, db: Session, question: models.Question, question_type: models.QuestionType, quiz: models.Quiz) -> None:
		data = fake_question(quiz.id, question_type.id)
		question_in_update = models.QuestionUpdate(**data)
		crud.question.update(db, db_obj=question, obj_in=question_in_update)
		question_updated = crud.question.get(db, id=question.id)
		assert question_updated
		assert question.content == question_updated.content
		assert question.quiz_id == question_updated.quiz_id
		assert question.question_type_id == question_updated.question_type_id


class TestAnswer:
	def test_create_question(self, db: Session, question: models.Question) -> None:
		data = fake_answer(question.id)
		answer_in = models.AnswerCreate(**data)
		answer = crud.answer.create(db, obj_in=answer_in)
		assert answer.content == answer_in.content
		assert answer.correct == answer_in.correct
		assert answer.question_id == answer_in.question_id

	def test_get_answer(self, db: Session, answer: models.Answer) -> None:
		db_obj = crud.answer.get(db, id=answer.id)
		assert db_obj
		assert answer.content == db_obj.content
		assert jsonable_encoder(answer) == jsonable_encoder(db_obj)

	def test_update_answer(self, db: Session, answer: models.Answer, question: models.Question) -> None:
		data = fake_answer(question.id)
		answer_in_update = models.AnswerUpdate(**data)
		crud.answer.update(db, db_obj=answer, obj_in=answer_in_update)
		answer_updated = crud.answer.get(db, id=answer.id)
		assert answer_updated
		assert answer.correct == answer_updated.correct
		assert answer.question_id == answer_updated.question_id
