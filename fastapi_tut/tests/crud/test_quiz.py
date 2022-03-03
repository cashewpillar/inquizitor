from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from fastapi_tut import crud, models
from fastapi_tut.utils import fake, fake_question, fake_quiz, random_str

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


# TODO: apply quiz api or search for better api
class TestQuestion:
	def test_create_question(self, db: Session, quiz: models.Quiz, question_type: models.QuestionType) -> None:
		data = fake_question(quiz, question_type)
		question_in = models.QuestionCreate(**data)
		question = crud.question.create(db, obj_in=question_in)
		assert question.content == question_in.content
		assert question.quiz_id == question_in.quiz_id
		assert question.question_type_id == question_in.question_type_id

	# def test_get_question(self, db: Session) -> None:
	# 	question_in = models.Question(name=random_str())
	# 	question = crud.question.create(db, obj_in=question_in)
	# 	question_2 = crud.question.get(db, id=question.id)
	# 	assert question_2
	# 	assert question.name == question_2.name
	# 	assert jsonable_encoder(question) == jsonable_encoder(question_2)

	# def test_update_question(self, db: Session, quiz: models.QuestionType) -> None:
	# 	name = random_str()
	# 	question_type_in_update = models.QuestionTypeUpdate(name=name)
	# 	crud.quiz.update(db, db_obj=quiz, obj_in=question_type_in_update)
	# 	quiz_2 = crud.quiz.get(db, id=quiz.id)
	# 	assert quiz_2
	# 	assert quiz.name == quiz_2.name
