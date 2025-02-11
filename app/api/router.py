from fastapi import APIRouter

from app.api.endpoints.chatbot.chat import chat_router
from app.api.endpoints.user.user import auth_router
from app.api.endpoints.user.user_profile import user_profile_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["User Auth"])
api_router.include_router(user_profile_router, tags=["User Profile"])
api_router.include_router(chat_router, tags=["Chat"])