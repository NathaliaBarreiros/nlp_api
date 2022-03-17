from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    user,
    login_form,
    role,
    zeroshot_inference,
    text_inference,
)

api_router = APIRouter()
api_router.include_router(login_form.router, tags=["login_form"])
api_router.include_router(role.router, tags=["role"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(zeroshot_inference.router, tags=["zeroshot_inference"])
api_router.include_router(text_inference.router, tags=["text_inference"])
