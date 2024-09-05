from routes.index import routerAuth as router
from entities.user import UserRegisterSchema, UserLoginSchema
from handlers.auth import AuthHandler
from fastapi import Request


@router.post('/register')
async def register_account(params: UserRegisterSchema, request: Request):
    auth_handler = AuthHandler(request=request)

    response = auth_handler.process_register(params=params)
    return response

@router.post('/login')
async def login_account(params: UserLoginSchema, request: Request):
    auth_handler = AuthHandler(request=request)

    response = auth_handler.process_register(params=params)
    return response