from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_tut import commands
from fastapi_tut.core.config import settings
from fastapi_tut.api.api_v1.api import api_router

DESCRIPTION = """
FASTAPI_TUT helps you learn API STUFF AND FASTAPI. xD GG nc NC 🚀  

## Users 

You will be able to: 

* **Log In** (_not implemented_). 

* **Take an exam** (_not implemented_).
"""

def register_commands():
	commands.cli.add_command(commands.initial_data) 
	commands.cli.add_command(commands.test)

def create_app():
	"""App for getting training data from exams"""
	app = FastAPI(title=settings.PROJECT_NAME, 
		version=settings.PROJECT_VERSION,
		description=DESCRIPTION)
		# openapi_url=f"{settings.API_V1_STR}/openapi.json")

	app.include_router(api_router)
	# might remove staticfiles once vue is implemented
	app.mount("/static", StaticFiles(directory="fastapi_tut/static"), name="static")

	register_commands()

	return app
