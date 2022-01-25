import os, secrets
from pathlib import Path
from pydantic import EmailStr
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
	PROJECT_NAME:str = "FastAPI Tut"
	PROJECT_VERSION:str = "1.0.0"
	USE_SQLITE:bool = os.getenv("USE_SQLITE")

	API_V1_STR: str = "/api/v1"
	SECRET_KEY: str = secrets.token_urlsafe(32)
	ALGORITHM: str = "HS256"
	# default from ref: 60 minutes * 24 hours * 8 days = 8 days
	# ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

	POSTGRES_USER : str = os.getenv("POSTGRES_USER")
	POSTGRES_PASSWORD : str = os.getenv("POSTGRES_PASSWORD")
	POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER", "localhost")
	POSTGRES_PORT : str = os.getenv("POSTGRES_PORT", 5432)
	POSTGRES_DB : str = os.getenv("POSTGRES_db", "tdd")
	DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

	EMAIL_TEST_USER: EmailStr = "test@example.com" # type: ignore
	FIRST_SUPERUSER_EMAIL: EmailStr = "admin@admin.com"
	FIRST_SUPERUSER_FULLNAME: str = "admin"
	FIRST_SUPERUSER_PASSWORD: str = "superadmin"
	USERS_OPEN_REGISTRATION: bool = False

settings = Settings()