# auth-middleware/tests/test_services.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from services import register_user, login_user
from utils.password_utils import verify_password

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_register_user(db):
    user_data = {"email": "test@example.com",
                 "username": "testuser", "password": "testpass"}
    user = register_user(db, user_data)
    assert user.email == "test@example.com"
    assert verify_password("testpass", user.password)


def test_login_user(db):
    user_data = {"email": "test@example.com",
                 "username": "testuser", "password": "testpass"}
    register_user(db, user_data)
    result = login_user(
        db, {"email": "test@example.com", "password": "testpass"})
    assert "access_token" in result
