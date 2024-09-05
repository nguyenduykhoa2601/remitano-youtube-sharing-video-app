from fastapi import Request, Depends
from sqlalchemy.orm import Session
from models.user import User
from entities.user import UserRegisterSchema, UserLoginSchema
import jwt
import datetime
from databases.postgre import pwd_context, get_db
from typing import Union
from datetime import datetime, timedelta
import os
from shared.status_code.index import STATUS_CODE

SECRET_KEY = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("HASH_ALGORITHM")


class AuthHandler:
    def __init__(self, request: Request) -> None:
        self.request = request

    def create_user(self, db: Session, email: str, hashed_password: str):
        db_user = User(email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def register_user(self, params: UserRegisterSchema, db: Session = Depends(get_db)):
        existing_user = self.get_user_by_email(db, params.email)
        if existing_user:
            return {
                "code": STATUS_CODE.not_unique,
                "msg": "Email has been existed"
            }

        hashed_password = self.hash_password(params.password)
        new_user = self.create_user(
            db, email=params.email, hashed_password=hashed_password)
        return {"code": STATUS_CODE.success_code, "email": new_user.email, "message": "User created successfully"}

    def login_user(self, user: UserLoginSchema, db: Session = Depends(get_db)):
        db_user = self.get_user_by_email(db, user.email)
        if not db_user or not self.verify_password(user.password, db_user.hashed_password):
            return {
                "code": STATUS_CODE.auth_failed,
                "msg": "Email or Password not correct"
            }

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"email": db_user.email},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(token: str) -> dict:
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_jwt
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_jwt
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
