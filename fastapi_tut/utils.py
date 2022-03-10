from faker import Faker
from typing import Optional
import random
import string

from fastapi.templating import Jinja2Templates

from fastapi_tut import models

# TODO might remove templates once vue app is developed
templates = Jinja2Templates(directory="fastapi_tut/templates")

fake = Faker()

def random_str():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))

def random_question_type():
	return ''.join(random.choices(["Identification", "Multiple-Choices"]))

def fake_answer(question_id):
	"""return fake answer"""

	return {"content": random_str(),
			"is_correct": False,
			"question_id": question_id}

def fake_marks_of_student(quiz_id, user_id):
	"""return fake score"""

	return {"score": random.randint(0,30),  # NOTE total items of quiz not considered
			"quiz_id": quiz_id,
			"user_id": user_id}

def fake_question(quiz_id, question_type_id, use_api=False):
	"""return fake question"""

	if use_api:
		import requests
		question_obj = requests.get("https://opentdb.com/api.php?amount=1").json()['results'][0]
		
		return question_obj['question']

	return {"content": fake.text(120)[:-1] + "?",
			"quiz_id": quiz_id,
			"question_type_id": question_type_id}

def fake_quiz(teacher_id):
	"""return fake values for name, desc, number_of_questions, and time."""

	return {
		# https://www.javatpoint.com/python-program-to-generate-a-random-string
		"name": random_str(),
		"desc": fake.text(),
		"number_of_questions": random.randrange(10, 100, 10),
		"time": random.randrange(30*60, 60*60, 5*60),
		"teacher_id": teacher_id
	}

# TODO: remove, currently uses faker through factory
def fake_user(password: Optional[str]=None, **attrs):
	"""return fake values for full-name, email, and password."""

	password = fake.password() if password is None else password
	return {
		**{"full_name": fake.name(),
		"email": fake.email(),
		"password": password},

		**attrs
	}

