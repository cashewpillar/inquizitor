from typing import Optional
from faker import Faker

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