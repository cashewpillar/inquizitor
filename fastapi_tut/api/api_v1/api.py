from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints import quiz, login, user

api_router = APIRouter()
api_router.include_router(login.router, prefix='/login', tags=['login'])
api_router.include_router(user.router, prefix='/users', tags=['users'])