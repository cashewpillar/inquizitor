from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlmodel import Session

from fastapi_tut import commands
from fastapi_tut.models import RevokedToken
from fastapi_tut.db.session import SessionLocal
from fastapi_tut.core.config import settings
from fastapi_tut.api.api_v1.api import api_router

def register_commands():
	"""Register Click commands."""
	commands.cli.add_command(commands.initial_data) 
	commands.cli.add_command(commands.test)


def register_fastapi_jwt_auth(app: FastAPI, db: Session):
	# TODO: do we test exception handlers?
	@AuthJWT.load_config
	def get_config():
		return settings

	@app.exception_handler(AuthJWTException)
	def authjwt_exception_handler(request: Request, exc: AuthJWTException):
		return JSONResponse(
			status_code=exc.status_code,
			content={"detail": exc.message}
		)

	@AuthJWT.token_in_denylist_loader
	def check_if_token_in_denylist(decrypted_token):
		# NOTE: reference used Redis instead of an SQL DB
		# config below might produce errors in production
		# NOTE: tokens in denylist (in db) has no expiry,
		# will add in the future if time permits
		jti = decrypted_token['jti']
		entry = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
		return entry and entry.is_revoked == True


def create_app(db: Session = SessionLocal()):
	"""App for getting training data from exams"""
	app = FastAPI(title=settings.PROJECT_NAME, 
		version=settings.PROJECT_VERSION,
		description=settings.DESCRIPTION)
		# openapi_url=f"{settings.API_V1_STR}/openapi.json")

	app.include_router(api_router)

	# NOTE might remove staticfiles once vue app is developed
	app.mount("/static", StaticFiles(directory="fastapi_tut/static"), name="static")

	register_commands()
	register_fastapi_jwt_auth(app, db)

	return app

