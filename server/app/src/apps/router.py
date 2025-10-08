from fastapi import APIRouter

from .api import chat, user

api_router = APIRouter()

# 라우터 등록
api_router.include_router(user.router, prefix="/api/users", tags=["사용자"])
api_router.include_router(chat.router, prefix="/api/chat", tags=["채팅"])
