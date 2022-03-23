# import logging
# import random
# import pprint
# from typing import List

# from fastapi.encoders import jsonable_encoder
# from sqlmodel import Session

# from fastapi_tut import crud, models
# from fastapi_tut.utils import (
# 	fake, 
# 	fake_answer, 
# 	fake_marks_of_user, 
# 	fake_question, 
# 	fake_quiz, 
# 	random_str
# )

# logging.basicConfig(
# 	level=logging.DEBUG,
# 	format="%(asctime)s -  %(levelname)s -  %(message)s"
# )
# logger = logging.getLogger(__name__)
# # logging.disable(logging.INFO)

# class TestQuiz:
# 	def test_create_quiz(self, db: Session) -> None:
# 		data = fake_quiz()
# 		quiz_in = models.QuizCreate(**data)
# 		quiz = crud.quiz.create(db, obj_in=quiz_in)
# 		assert quiz.name == data["name"]
# 		assert quiz.desc == data["desc"]
# 		assert quiz.number_of_questions == data["number_of_questions"]
# 		assert quiz.time == data["time"]

# 	def test_get_quiz(self, db: Session, quiz: models.Quiz) -> None:
# 		quiz_2 = crud.quiz.get(db, id=quiz.id)
# 		assert quiz_2
# 		assert quiz.name == quiz_2.name
# 		assert jsonable_encoder(quiz) == jsonable_encoder(quiz_2)

# 	def test_get_quiz_relations(
# 		self, 
# 		db: Session, 
# 		quiz: models.Quiz, 
# 		questions: List[models.Question],
# 		marks_of_users: List[models.MarksOfUser]
# 	) -> None:
# 		quiz = crud.quiz.get(db, id=quiz.id)

# 		assert quiz.questions == questions
# 		assert quiz.marks_of_users == marks_of_users

# 	def test_update_quiz(self, db: Session, quiz: models.Quiz) -> None:
# 		data = fake_quiz()
# 		quiz_in_update = models.QuizUpdate(**data)
# 		crud.quiz.update(db, db_obj=quiz, obj_in=quiz_in_update)
# 		quiz_2 = crud.quiz.get(db, id=quiz.id)
# 		assert quiz_2
# 		assert quiz.name == quiz_2.name
# 		assert quiz.desc == quiz_2.desc
# 		assert quiz.number_of_questions == quiz_2.number_of_questions
# 		assert quiz.time == quiz_2.time


# class TestQuestionType:
# 	def test_create_question_type(self, db: Session) -> None:
# 		name = random_str()
# 		question_type_in = models.QuestionTypeCreate(name=name)
# 		question_type = crud.question_type.create(db, obj_in=question_type_in)
# 		assert question_type.name == name

# 	def test_get_question_type(self, db: Session) -> None:
# 		question_type_in = models.QuestionType(name=random_str())
# 		question_type = crud.question_type.create(db, obj_in=question_type_in)
# 		question_type_2 = crud.question_type.get(db, id=question_type.id)
# 		assert question_type_2
# 		assert question_type.name == question_type_2.name
# 		assert jsonable_encoder(question_type) == jsonable_encoder(question_type_2)

# 	def test_update_question_type(self, db: Session, question_type: models.QuestionType) -> None:
# 		name = random_str()
# 		question_type_in_update = models.QuestionTypeUpdate(name=name)
# 		crud.question_type.update(db, db_obj=question_type, obj_in=question_type_in_update)
# 		question_type_2 = crud.question_type.get(db, id=question_type.id)
# 		assert question_type_2
# 		assert question_type.name == question_type_2.name


# class TestQuestion:
# 	def test_create_question(self, db: Session, quiz: models.Quiz, question_type: models.QuestionType) -> None:
# 		data = fake_question(quiz.id, question_type.id)
# 		question_in = models.QuestionCreate(**data)
# 		question = crud.question.create(db, obj_in=question_in)
# 		assert question.content == question_in.content
# 		assert question.quiz_id == question_in.quiz_id
# 		assert question.question_type_id == question_in.question_type_id

# 	def test_get_question(self, db: Session, question: models.Question) -> None:
# 		db_obj = crud.question.get(db, id=question.id)
# 		assert db_obj
# 		assert question.content == db_obj.content
# 		assert jsonable_encoder(question) == jsonable_encoder(db_obj)

# 	def test_get_question_relations(
# 		self, 
# 		db: Session, 
# 		answers: List[models.Answer],
# 		quiz: models.Quiz,
# 		question: models.Question,
# 		question_type: models.QuestionType
# 	) -> None:
# 		assert question.quiz == quiz
# 		assert question.question_type == question_type
# 		assert question.answers == answers

# 	def test_update_question(self, db: Session, question: models.Question, question_type: models.QuestionType, quiz: models.Quiz) -> None:
# 		data = fake_question(quiz.id, question_type.id)
# 		question_in_update = models.QuestionUpdate(**data)
# 		crud.question.update(db, db_obj=question, obj_in=question_in_update)
# 		question_updated = crud.question.get(db, id=question.id)
# 		assert question_updated
# 		assert question.content == question_updated.content
# 		assert question.quiz_id == question_updated.quiz_id
# 		assert question.question_type_id == question_updated.question_type_id


# class TestAnswer:
# 	def test_create_answer(self, db: Session, question: models.Question) -> None:
# 		data = fake_answer(question.id)
# 		answer_in = models.AnswerCreate(**data)
# 		answer = crud.answer.create(db, obj_in=answer_in)
# 		assert answer.content == answer_in.content
# 		assert answer.is_correct == answer_in.is_correct
# 		assert answer.question_id == answer_in.question_id

# 	def test_get_answer(self, db: Session, answer: models.Answer) -> None:
# 		db_obj = crud.answer.get(db, id=answer.id)
# 		assert db_obj
# 		assert answer.content == db_obj.content
# 		assert jsonable_encoder(answer) == jsonable_encoder(db_obj)

# 	def test_get_answer_relations(self, db: Session, answer: models.Answer, question: models.Question) -> None:
# 		assert answer.question == question

# 	def test_check_if_answer_is_correct(self, db: Session, answer: models.Answer) -> None:
# 		"""fixture answer is correct by default"""
# 		assert answer.is_correct is True

# 	def test_update_answer(self, db: Session, answer: models.Answer, question: models.Question) -> None:
# 		data = fake_answer(question.id)
# 		answer_in_update = models.AnswerUpdate(**data)
# 		crud.answer.update(db, db_obj=answer, obj_in=answer_in_update)
# 		answer_updated = crud.answer.get(db, id=answer.id)
# 		assert answer_updated
# 		assert answer.is_correct == answer_updated.is_correct
# 		assert answer.question_id == answer_updated.question_id


# class TestMarksOfUser:
# 	def test_create_marks_of_user(self, db: Session, user: models.User, quiz: models.Quiz) -> None:
# 		data = {"score": random.randint(0,30),  # NOTE total items of quiz not considered
# 				"quiz_id": quiz.id,
# 				"user_id": user.id}
# 		marks_of_user_in = models.MarksOfUserCreate(**data)
# 		marks_of_user = crud.marks_of_user.create(db, obj_in=marks_of_user_in)
# 		assert marks_of_user.score == marks_of_user_in.score
# 		assert marks_of_user.quiz_id == marks_of_user_in.quiz_id
# 		assert marks_of_user.user_id == marks_of_user_in.user_id

# 	def test_get_marks_of_user(self, db: Session, marks_of_users: models.MarksOfUser) -> None:
# 		marks_of_user = marks_of_users[0]
# 		db_obj = crud.marks_of_user.get(db, id=marks_of_user.id)
# 		assert db_obj
# 		assert marks_of_user.score == db_obj.score
# 		assert jsonable_encoder(marks_of_user) == jsonable_encoder(db_obj)

# 	def test_get_marks_of_user_relations(
# 		self, 
# 		db: Session, 
# 		marks_of_users: models.MarksOfUser,
# 		quiz: models.Quiz,
# 		user: models.User
# 	) -> None:
# 		marks_of_user = marks_of_users[0]
# 		assert marks_of_user.user == user
# 		assert marks_of_user.quiz == quiz

# 	def test_update_marks_of_user(
# 		self, 
# 		db: Session, 
# 		marks_of_users: models.MarksOfUser, 
# 		quiz: models.Quiz,
# 		user: models.User
# 	) -> None:
# 		marks_of_user = marks_of_users[0]
# 		data = fake_marks_of_user(quiz.id, user.id)
# 		marks_of_user_in_update = models.MarksOfUserUpdate(**data)
# 		crud.marks_of_user.update(db, db_obj=marks_of_user, obj_in=marks_of_user_in_update)
# 		marks_of_user_updated = crud.marks_of_user.get(db, id=marks_of_user.id)
# 		assert marks_of_user_updated
# 		assert marks_of_user.score == marks_of_user_updated.score
# 		assert marks_of_user.quiz_id == marks_of_user_updated.quiz_id
# 		assert marks_of_user.user_id == marks_of_user_updated.user_id
