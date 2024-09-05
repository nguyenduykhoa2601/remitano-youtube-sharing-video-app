from entities.user import UserRegisterSchema, UserLoginSchema
import os
import re
from fastapi import Request
from fastapi import HTTPException
from shared.status_code.index import STATUS_CODE
from middlewares.auth.auth import AuthMiddlewares


class AuthHandler:
    def __init__(self, request: Request) -> None:
        self.request = request
    
    def process_login(self, params: UserLoginSchema):
        if self.validate_email(params.email) == False:
            return {
                "code": STATUS_CODE.invalid_params,
                "msg": "Validate email failed!"
            }

        if self.validate_password(params.password) == False:
            return {
                "code": STATUS_CODE.invalid_params,
                "msg": "Validate password failed!"
            }
        
        auth_middlewares = AuthMiddlewares()

        response = auth_middlewares.login(params=params)

        return response

    def process_register(self, params: UserRegisterSchema):
        if self.validate_email(params.email) == False:
            return {
                "code": STATUS_CODE.invalid_params,
                "msg": "Validate email failed!"
            }

        if self.validate_password(params.password) == False:
            return {
                "code": STATUS_CODE.invalid_params,
                "msg": "Validate password failed!"
            }

        auth_middlewares = AuthMiddlewares()

        response = auth_middlewares.register(params=params)

        return response

    def validate_password(self, password: str):
        """
        Validates if the given password meets the required criteria:
        - At least 8 characters long
        - Contains at least one letter
        - Contains at least one number
        - Contains at least one special character

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        # Check if the password length is at least 8 characters
        if len(password) < 8:
            return False

        # Check if the password contains at least one letter
        if not re.search(r'[A-Za-z]', password):
            return False

        # Check if the password contains at least one number
        if not re.search(r'\d', password):
            return False

        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*()_+={}\[\]:;\'"<>?,./\\-]', password):
            return False

        # If all checks pass, the password is valid
        return True

    def validate_email(self, email: str):
        """
        Validates if the given email address is in a proper format.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        # Regular expression pattern for a valid email address
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Use re.match to check if the email matches the pattern
        if re.match(email_pattern, email):
            return True

        # Return False if the email does not match the pattern
        return False
