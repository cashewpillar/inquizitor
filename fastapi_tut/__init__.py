from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from fastapi_tut import commands
from fastapi_tut.core.config import settings
from fastapi_tut.api.api_v1.api import api_router

def register_commands():
	"""Register Click commands."""
	commands.cli.add_command(commands.initial_data) 
	commands.cli.add_command(commands.test)


@AuthJWT.load_config
def get_config():
	return settings


# TODO: do we test exception handlers?
def register_exception_handlers(app):
	@app.exception_handler(AuthJWTException)
	def authjwt_exception_handler(request: Request, exc: AuthJWTException):
		return JSONResponse(
			status_code=exc.status_code,
			content={"detail": exc.message}
		)


def create_app():
	"""App for getting training data from exams"""
	app = FastAPI(title=settings.PROJECT_NAME, 
		version=settings.PROJECT_VERSION,
		description=settings.DESCRIPTION)
		# openapi_url=f"{settings.API_V1_STR}/openapi.json")

	app.include_router(api_router)

	# might remove staticfiles once vue is implemented
	app.mount("/static", StaticFiles(directory="fastapi_tut/static"), name="static")

	register_commands()
	register_exception_handlers(app)

	return app

