from faker import Faker

from fastapi.templating import Jinja2Templates

# might remove staticfiles once vue is implemented
templates = Jinja2Templates(directory="fastapi_tut/templates")

fake = Faker("fil_PH")

def fake_user(**additional):
	return {
		**{"full_name": fake.name(),
		"email": fake.email(),
		"password": fake.password()}, 
		
		**additional
	}