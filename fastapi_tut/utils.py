from typing import Optional
from faker import Faker
import random
import string

from fastapi.templating import Jinja2Templates

# TODO might remove templates once vue app is developed
templates = Jinja2Templates(directory="fastapi_tut/templates")

# TODO fil_PH not working/ showing
fake = Faker("fil_PH")

def fake_user(password: Optional[str]=None, **attrs):
	"""return fake values for full-name, email, and password."""

	password = fake.password() if password is None else password
	return {
		**{"full_name": fake.name(),
		"email": fake.email(),
		"password": password},

		**attrs
	}

def fake_quiz():
	"""return fake values for name, desc, number_of_questions, and time."""

	return {
		# https://www.javatpoint.com/python-program-to-generate-a-random-string
		"name": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
		"desc": fake.text(),
		"number_of_questions": random.randrange(10, 100, 10),
		"time": random.randrange(30*60, 60*60, 5*60)
	}