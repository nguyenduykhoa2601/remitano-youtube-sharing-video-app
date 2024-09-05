from routes.index import routerAuth as router
from shared.status_code.index import STATUS_CODE

from entities.user import UserRegisterSchema
from handlers.auth import AuthHandler
from fastapi import Request

@router.post("/register")
async def register_user(params: UserRegisterSchema, request: Request):
    auth_handler = AuthHandler(request=request)
    response = auth_handler.register_user(params=params)
    return response
