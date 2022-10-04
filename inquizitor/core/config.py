import os, secrets
from pathlib import Path
from dotenv import load_dotenv

from pydantic import BaseSettings, EmailStr

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Inquizitor"
    PROJECT_DESC: str = """REST API for managing/ administering quizzes. 
	With refresh tokens and basic permission control. Use teacher:superteacher or student:superstudent to log in."""
    PROJECT_VERSION: str = "1.0.0"
    USE_SQLITE: bool = os.getenv("USE_SQLITE", 1)
    FASTAPI_ENV: str = os.getenv("FASTAPI_ENV", 'dev')

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    # Configure application to store and get JWT from cookies
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", 'sqlite:///inquizitor/data.db')

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@admin.com"
    FIRST_SUPERUSER_LASTNAME: str = "Add"
    FIRST_SUPERUSER_FIRSTNAME: str = "Mean"
    FIRST_SUPERUSER_PASSWORD: str = "superadmin"
    USERS_OPEN_REGISTRATION: bool = False

    FIRST_STUDENT_EMAIL: EmailStr = "student@student.com"
    FIRST_STUDENT_USERNAME: str = "student"
    FIRST_STUDENT_LASTNAME: str = "Stew"
    FIRST_STUDENT_FIRSTNAME: str = "Dent"
    FIRST_STUDENT_PASSWORD: str = "superstudent"

    FIRST_TEACHER_EMAIL: EmailStr = "teacher@teacher.com"
    FIRST_TEACHER_USERNAME: str = "teacher"
    FIRST_TEACHER_LASTNAME: str = "Tea"
    FIRST_TEACHER_FIRSTNAME: str = "Chair"
    FIRST_TEACHER_PASSWORD: str = "superteacher"

    authjwt_secret_key: str = os.getenv('SECRET_KEY', 'secret')
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}

    disable_signup: bool = False
    SUPERUSER_PASSWORD: str = os.getenv('SUPERUSER_PASSWORD', 'secret')

class DevelopmentSettings(Settings):
    # can be sent through HTTP
    authjwt_cookie_secure: bool = False

class ProductionSettings(Settings):
    # CORS
    authjwt_cookie_samesite: str = 'none'
    
    # HTTPS ONLY   
    authjwt_cookie_secure: bool = True

class StagingSettings(ProductionSettings):
    pass

class DataCollectionSettings(ProductionSettings):
    disable_signup: bool = True

def load_settings():
    if os.getenv('FASTAPI_ENV') == 'prod':
        return ProductionSettings()
    elif os.getenv('FASTAPI_ENV') == 'staging':
        return StagingSettings()
    elif os.getenv('FASTAPI_ENV') == 'data':
        return DataCollectionSettings()
    else:
        return DevelopmentSettings()



settings = load_settings()
