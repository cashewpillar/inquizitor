from faker import Faker
from typing import Optional
import random
import string

from inquizitor import models

fake = Faker()

def random_str():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))

def fake_question(quiz_id, question_type_id, use_api=False):
	"""return fake question (kept for reference: using api banks for dummy questions)"""

	if use_api:
		import requests
		question_obj = requests.get("https://opentdb.com/api.php?amount=1").json()['results'][0]
		
		return question_obj['question']

	return {"content": fake.text(120)[:-1] + "?",
			"quiz_id": quiz_id,
			"question_type_id": question_type_id}


