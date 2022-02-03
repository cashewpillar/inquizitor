from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints import admin, exams, login

api_router = APIRouter()
# api_router.include_router(admin.router)
# api_router.include_router(exams.router)
api_router.include_router(login.router)