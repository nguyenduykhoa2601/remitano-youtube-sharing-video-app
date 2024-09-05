from models.http_requests import HTTPRequest
from entities.user import UserRegisterSchema, UserLoginSchema
import os

ENDPOINT_AUTH_MIDDLEWARES = os.getenv("ENDPOINT_AUTH_MIDDLEWARES")


class AuthMiddlewares:
    def __init__(self, timeout=600) -> None:
        self.timeout = timeout

    def register(self, params: UserRegisterSchema):
        # Convert Pydantic model to dict to send in JSON format
        http_request = HTTPRequest(
            url=f"{ENDPOINT_AUTH_MIDDLEWARES}/register", method="POST"
        )
        print("Sending data:", params.dict())  # Better to log the dictionary
        response = http_request.send_request(
            data=params.dict())  # Use dict() here
        return response

    def login(self, params: UserLoginSchema):
        # Convert Pydantic model to dict to send in JSON format
        http_request = HTTPRequest(
            url=f"{ENDPOINT_AUTH_MIDDLEWARES}/login", method="POST"
        )
        print("Sending data:", params.dict())  # Better to log the dictionary
        response = http_request.send_request(
            data=params.dict())  # Use dict() here
        return response
