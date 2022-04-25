import os, secrets
from pathlib import Path
from dotenv import load_dotenv

from pydantic import BaseSettings, EmailStr

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
	PROJECT_NAME:str = "FastAPI Tut"
	PROJECT_VERSION:str = "1.0.0"
	USE_SQLITE:bool = os.getenv("USE_SQLITE")

	API_V1_STR: str = "/api/v1"
	SECRET_KEY: str = secrets.token_urlsafe(32)
	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 # 1 minute
	REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

	# Configure application to store and get JWT from cookies
	AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
	AUTHJWT_COOKIE_CSRF_PROTECT: bool = False

	POSTGRES_USER : str = os.getenv("POSTGRES_USER")
	POSTGRES_PASSWORD : str = os.getenv("POSTGRES_PASSWORD")
	POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER", "localhost")
	POSTGRES_PORT : str = os.getenv("POSTGRES_PORT", 5432)
	POSTGRES_DB : str = os.getenv("POSTGRES_db", "tdd")

	if USE_SQLITE:
		SQLALCHEMY_DATABASE_URI = "sqlite:///inquizitor/data.db"
	else:
		SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

	EMAIL_TEST_USER: EmailStr = "test@example.com" # type: ignore
	FIRST_SUPERUSER_USERNAME : str = "admin"
	FIRST_SUPERUSER_EMAIL: EmailStr = "admin@admin.com"
	FIRST_SUPERUSER_LASTNAME: str = "Add"
	FIRST_SUPERUSER_FIRSTNAME: str = "Mean"
	FIRST_SUPERUSER_PASSWORD: str = "superadmin"
	USERS_OPEN_REGISTRATION: bool = False

	FIRST_STUDENT_EMAIL: EmailStr = "student@student.com"
	FIRST_STUDENT_USERNAME : str = "student"
	FIRST_STUDENT_LASTNAME: str = "Stew"
	FIRST_STUDENT_FIRSTNAME: str = "Dent"
	FIRST_STUDENT_PASSWORD: str = "superstudent"

	FIRST_TEACHER_EMAIL: EmailStr = "teacher@teacher.com"
	FIRST_TEACHER_USERNAME : str = "teacher"
	FIRST_TEACHER_LASTNAME: str = "Tea"
	FIRST_TEACHER_FIRSTNAME: str = "Chair"
	FIRST_TEACHER_PASSWORD: str = "superteacher"

	authjwt_secret_key: str = SECRET_KEY
	authjwt_denylist_enabled: bool = True
	authjwt_denylist_token_checks: set = {"access", "refresh"}

settings = Settings()
