from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest
# from app.database import get_db
# from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.config import settings
from app.database import Base, engine


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'welcome to my first FastAPI app'
    assert res.status_code == 200

def test_user_create(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password101", "phone_number": "123455"})
    newUser = schemas.UserOut(**res.json())
    assert newUser.email == "test@gmail.com"
    assert res.status_code == 201