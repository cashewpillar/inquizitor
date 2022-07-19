from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlmodel import Session

from inquizitor import commands
from inquizitor.models import RevokedToken
from inquizitor.db.session import SessionLocal
from inquizitor.core.config import settings
from inquizitor.api.api_v1.api import api_router


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
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @AuthJWT.token_in_denylist_loader
    def check_if_token_in_denylist(decrypted_token):
        # NOTE: reference used Redis instead of an SQL DB
        # config below might produce errors in production
        # NOTE: tokens in denylist (in db) has no expiry,
        # will add in the future if time permits

        jti = decrypted_token["jti"]
        entry = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
        return entry


def register_cors(app: FastAPI):
    origins = [
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app(db: Session = SessionLocal()):
    """App for getting training data from exams"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESC,
        version=settings.PROJECT_VERSION,
    )
    # openapi_url=f"{settings.API_V1_STR}/openapi.json")

    app.include_router(api_router)

    register_commands()
    register_cors(app)
    register_fastapi_jwt_auth(app, db)

    return app
