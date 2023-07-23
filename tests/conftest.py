from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db, Base
from app.main import app

import pytest

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         return db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        return db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():

        try:
            return session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "Test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
